import os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.writing import AsyncWriter
import sys

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
 
def tokenize(text):
    # tokenizzazione
    tokens = nltk.word_tokenize(text)
    
    #Eliminazione di stopwords e punteggiatura
    tokens2=[]
    for t in tokens:
        if t not in stopwords.words('italian') and t.isalnum():
            tokens2.append(t)
    return tokens2
    

def createSearchableData(root):   
    
    ana = analysis.StemmingAnalyzer()
    ## definisco lo schema del mio indice
    schema = Schema( title=TEXT(stored=True),\
                     author=TEXT(stored=True),\
                     genre=KEYWORD(stored=True), \
                     link=ID(stored=True), \
                     path=ID(stored=True), \
                     content=TEXT(stored=True),\
                     contentData=TEXT)
                         
    ## creo la directory indexdir
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    
    cwd = os.getcwd()
    print(cwd)
    
    ## Creo un indexWriter, che aggiunga i documenti secondo lo schema
    ix = create_in("indexdir",schema)
    writer = AsyncWriter(ix)
 
    ## Trovo i file nella directory, e ne salvo i percorsi
    filepaths = [os.path.join(root,i) for i in os.listdir(root)]
    
    num = 1
    # per ogni percorso trovato...
    for path in filepaths:
        #print(num)
        num+=1
    
        fp = open(path,'r', encoding="utf-8")
        #print(path)

        # Nella prima riga ho messo il titolo, nella seconda l'autore, nella terza il genere, nella quarta il link
        fileTitle = fp.readline()
        fileAuthor = fp.readline()
        fileGenre = fp.readline()
        fileLink = fp.readline()
        
        # Tutto il resto del file è occupato dalla trama
        filePlot = fp.read()
        
        # la sezione contentData è data dalle trame preprocessate
        fileData = tokenize(filePlot)
        
        ## Aggiungo un documento all'indice, con tutti i campi necessari
        writer.add_document( title = fileTitle,\
                             path = path,\
                             author = fileAuthor,\
                             genre = fileGenre,\
                             link = fileLink,\
                             content = filePlot,\
                             contentData = fileData)
        fp.close()
    writer.commit()
 
root = "C:\\Users\Seren\.spyder-py3\Books-Search-Engine\scraping"
createSearchableData(root)
