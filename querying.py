from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser, MultifieldParser
import os, os.path
from whoosh import qparser, scoring
from nltk.corpus import wordnet as wn
import nltk
import enchant
import operator

#roba che serve per far funzionare i sinonimi in italiano
nltk.download('wordnet')
nltk.download('omw')

ix = open_dir("indexdir")

def catTranslate(category):
    # Uno switch per identificare le categorie in cui effettuare la ricerca.
    # category è la categoria scelta dall'utente tramite l'apposito menu a tendina
    switcher={
        "Tutte":["contentData", "title", "author", "genre", "content"],
        "Titolo":["title"],
        "Autore":["author"],
        "Genere":["genre"],
        "Trama":["contentData", "content"]
    }
    return switcher.get(category)
    
def siteTranslate(site):
    # Uno switch per identificare le il sito in cui effettuare la ricerca.
    # site è il sito scelto dall'utente tramite l'apposito menu a tendina
    switcher={
        "Tutti":"https://.*",
        "LibriMondadori":"https://www.librimondadori.it/.*",
        "Piemme":"https://www.edizpiemme.it/.*",
        "Rizzoli":"https://.*.rizzolilibri.it/.*",
    }
    return switcher.get(site)    


def searchWord(userQuery, category="tutte", site="tutti", minPrice="0.0", maxPrice="100.0"):
    # d = enchant.Dict()
    # d.check(userQuery)
    #creo la lista dei sinonimi
    synonyms = [userQuery]
    
    # Query expansion: aggiungo anche i sinonimi alla query
    for syn in wn.synsets(userQuery, lang = "ita"):
        for l in syn.lemmas(lang = "ita"):
            if l.name() != userQuery:
                synonyms.append(l.name())        

    searcher = ix.searcher()
    #searcher = ix.searcher(weighting=scoring.TF_IDF())
    #searcher = ix.searcher(weighting=scoring.BM25F(B=0.75, content_B=1.0, K1=1.5))
    #searcher = ix.searcher(weighting=scoring.Frequency)
    
    #implementa la ricerca anche per titolo, autore o genere, a seconda della scelta dell'utente
    parser = MultifieldParser(catTranslate(category), schema=ix.schema) 


    siteChoice = siteTranslate(site)

    # Creo l'array dei risultati da restituire all'interfaccia
    resultsTot = [];
    for syn in synonyms:
        query = parser.parse(syn)
        # # Try correcting the query
        # with ix.searcher() as s:
        #     corrected = s.correct_query(query, syn)
        #     if corrected.query != query:
        #         print("Did you mean:", corrected.string)
    

        results = searcher.search(query)
    
        if len(results) > 0:       
            for r in results:  
                if re.match(siteChoice, r['link']) :
                    price = r['price'].replace("€","").replace("\n","").replace(" ","")
                    if price == '':
                        price = '0.00'
                    if minPrice <= float(price) <= maxPrice:
                        if r not in resultsTot:
                            resultsTot.append(r) # aggiungo r ai risultati
    # Ri-ordino i risultati in base all'affinità
    resultsTot.sort(key=operator.attrgetter('score'), reverse=True)
    return resultsTot[0:min(len(resultsTot),10)]




