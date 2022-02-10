from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfile
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
from tkinter import scrolledtext

TextS=Tk()
TextS.geometry("1300x600")
TextS.title("Automatic Text Summarsization")



f1 = Frame(TextS, width="1250", height="600", bd=6,bg='#b85b56', relief='raised')
f1.pack()
e1e= StringVar()
e1e.set= ""

e1 = Label(f1, bd=8, width=26, justify='left', font='arial 16 bold', text="Enter File name")
e1.place(x=50, y=20)

e1 = Entry(f1, bd=8, width=36, justify='left', font='arial 16 bold',textvariable = e1e)
e1.place(x=450, y=20)

e2 = Label(f1, bd=8, width=36, justify='left', font='arial 10 bold', text="Indexes of top ranked sentences are:-")
e2.place(x=50, y=120)

T = scrolledtext.ScrolledText(f1, height=5, width=98)
T.place(x=450,y=80)
T.insert(END," ")

e3 = Label(f1, bd=8, width=36, justify='left', font='arial 10 bold', text="Summarize Text:")
e3.place(x=50, y=240)


T2 = scrolledtext.ScrolledText(f1, height=15, width=96)
T2.place(x=450,y=200)
T2.insert(END,"")

# Main code for summarization
def read_data(file_name):
    with open(file_name, 'r') as f:
        filedata = f.readlines()
    document = filedata[0].split(". ") # for splitting the sentence
    sentences = [] # Sentences will be stored in a list
   
    for sentence in document:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))# appending the text
        
    sentences.pop()
    
    return sentences 

def sentence_similarity(s1, s2, stopwords=None): #calculating similarity between two sentences
    if stopwords is None:
        stopwords = []
 
    s1 = [w.lower() for w in s1]
    s2 = [w.lower() for w in s2]
 
    all_words = list(set(s1 + s2)) # we will get only the unique words of character in s1 and s2
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # the vector for the first sentence
    for w in s1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    # the vector for the second sentence
    for w in s2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words): # Similarity matirx
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: # It will ignore if both sentences are same
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix

def generate_summary(top_n=3):
	file_name = e1e.get()
	stop_words = stopwords.words('english')
	summarize_text = []

	sentences =  read_data(file_name)
    # Aggregating all the methods above
    # Generate Similary Martix across sentences
	sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Rank sentences in similarity martix
	sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
	scores = nx.pagerank(sentence_similarity_graph)
  

    # Sort the rank and pick top sentences
	ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
	T.insert(END,ranked_sentence) 

	for i in range(top_n):
		summarize_text.append(" ".join(ranked_sentence[i][1]))

    # The output as the summarize texr
	T2.insert(END,summarize_text) 


btn =Button(f1, text="  Summarize  ", bg="#b85b56", font="lucid 30 bold", relief=RAISED, bd=10, command=lambda: generate_summary())
btn.place(x=450,y=500)



TextS.mainloop()