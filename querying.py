from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path

ix = open_dir("indexdir")

# Faccio digitare la query dall'utente
userQuery = input("Inserire una parola o frase da cercare: ")

searcher = ix.searcher()
parser = QueryParser("content", schema=ix.schema)
query = parser.parse(userQuery)
results = searcher.search(query)
 

# Restituisco i primi topN risultati - se esistono
topN = int(10) # il 10 l'ho messo a caso
i=1

for r in results:
    if i > topN:
        break
    print(i, r['title'], str(r.score), r['textdata'])
    i+=1
