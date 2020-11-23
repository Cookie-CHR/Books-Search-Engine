from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path

ix = open_dir("indexdir")

searcher = ix.searcher()
print(list(searcher.lexicon("content")))
parser = QueryParser("content", schema=ix.schema)
query = parser.parse("uno")
results = searcher.search(query)
 

# Top 'n' documents as result - if exist
topN = int(25)
i=1

for r in results:
    if i > topN:
        break
    print(i, r['title'], str(r.score), r['textdata'])
    i+=1
