from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path

ix = open_dir("indexdir")

# Faccio digitare la query dall'utente
userQuery = input("Inserire una parola o frase da cercare: ")

searcher = ix.searcher()
parser = QueryParser("contentData", schema=ix.schema)
query = parser.parse(userQuery)
results = searcher.search(query)
 

# Restituisco i primi topN risultati - se esistono
topN = int(10) # il 10 l'ho messo a caso
i=1

for r in results:
    if i > topN:
        break
    print(i, str(r.score), r['title'],r['author'])
    print(r['content'][:255]+"...\n\n")
    i+=1
