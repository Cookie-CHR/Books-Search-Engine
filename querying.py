from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser, MultifieldParser
import os, os.path
from whoosh import qparser
from nltk.corpus import wordnet as wn

import nltk
#roba che serve per far funzionare i sinonimi in italiano
nltk.download('wordnet')
nltk.download('omw')

ix = open_dir("indexdir")

# Faccio digitare la query dall'utente
userQuery = input("Inserire una parola o frase da cercare: ")
#creo la lista dei sinonimi
synonyms = [userQuery]

for syn in wn.synsets(userQuery, lang = "ita"):
    for l in syn.lemmas(lang = "ita"):
        if l.name() != userQuery:
            synonyms.append(l.name())

searcher = ix.searcher()

#implementa la ricerca anche per titolo, autore o genere
parser = MultifieldParser(["contentData", "title", "author", "genre", "content"], schema=ix.schema) 

for s in synonyms:
    query = parser.parse(s)
    results = searcher.search(query)
    
    if len(results) > 0:
        print(s)
        # Restituisco i primi topN risultati - se esistono
        topN = int(5) # primi 3 sennò viene un casino
        i=1
        
        for r in results:
            if i > topN:
                break
            
            print(i, str(r.score), r['title'],r['author'], r['genre'])
            print(r['content'][:255]+"...\n\n")
            i+=1




