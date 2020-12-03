from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime


def replaced(str):
    # sostituisce alcuni caratteri di una stringa con altri.
    # serve per il passaggio da titolo/autore a parte del link
    str = str.replace(" ","-")
    str = str.replace("à","a")
    str = str.replace("è","e")
    str = str.replace("é","e")
    str = str.replace("ì","i")
    str = str.replace("ò","o")
    str = str.replace("ó","o")
    str = str.replace("ö","o")
    str = str.replace("ù","u")
    str = str.replace("ð","d")
    return str

## funzione che si occupa dell'output su file
def fileWrite(title, author, genre, link, plot):
    outF = open("scraping/"+replaced(title)+".txt", "w")
    outF.write(title+"\n")
    outF.write(author+"\n")
    outF.write(genre+"\n")
    outF.write(link+"\n")
    outF.write(plot)
    outF.close()

## Funzione che fa il web cscraping di titoli, autori, generi e link
#  separata dal resto per ragioni di leggibilità
def soupScraping(driver, titles, authors, genres, links, g):
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    ## Estraggo le info e le metto negli array appositi
    # non c'è bisogno di differenziare con un if sul sito, perché se soup non trova la classe giusta non avvierà neanche il for
    
    #qlibri
    for a in soup.findAll(class_='listItem'):
        title=a.find('a',href=True, attrs={'class':'jr_listingTitle'})
        author=a.find('div', attrs={'class':'fieldValue'})
        
        # piccolo controllo, se non interrompo il ciclo mi dà errore
        if title is None or author is None:
            break
        
        # Creo il link e salvo la formattazione del genere senza trattini o barre
        link = "https://www.qlibri.it/"+replaced(g)+"/"+replaced(title.text.replace("-","%11"))+"/"
        genre = g.replace("-"," ").replace("/"," ")
        
        titles.append(title.text)
        authors.append(author.text)
        genres.append(genre) 
        links.append(link)         
    #mondadorilibri 
    for a in soup.findAll(class_='product-info'):
        title= a.find('a', attrs={'href' : re.compile('https://www.librimondadori.it/libri/.*')})
        author=a.find('a', attrs={'href' : re.compile('https://www.librimondadori.it/autore/.*')})
        
        if title is None or author is None:
            break
          
        # Creo il link e salvo la formattazione del genere senza trattini o barre
        link="https://www.librimondadori.it/libri/"+replaced(title.text)+"-"+replaced(author.text)+"/"
        genre = g.replace("-"," ").replace("/"," ")
        
        titles.append(title.text)
        authors.append(author.text)
        genres.append(genre) 
        links.append(link)
            
    # Ritorno gli array per aggiornarli
    return titles, authors, genres, links

def loadingBar(X, maxX):
    # loading bar, per sapere quante trame ho scaricato in percentuale 
          
    if X > maxX:
        X = maxX
    if X < 0:
        X = 0
    percent = (int)((float)(X/maxX*100)) 
    loadState = ("#"*percent)+(" "*(100-percent))
    return str(percent) + "%	["+loadState+"]"



start_time = datetime.now()
numPlot = 1


driver = webdriver.Firefox('/usr/lib/firefox/')

# Array delle pagine da raschiare
# (La maggior parte del link è sempre uguale, ho solo memorizzato la parte saliente: 
# in librimondadori cambia solo il genere, in qlibri genere e categoria)

mGenres = ["gialli-e-thriller", "narrativa-contemporanea", "romanzi-storici-fantasy-e-fantascienza"] # generi di mondadorilibri
qGenres = ["romanzi", "gialli", "racconti", "romanzi-storici", "fantasy", "fantascienza", "classici"] # generi di qlibri
qCategories = ["straniera","italiana"]

# per ognuno dei due siti...
for site in ["qlibri", "mondadorilibri", ]:
    ### Per cominciare, definisco/vuoto gli array in cui mettere i risultati
    titles = []
    authors = []
    genres = []
    links = []
    plots = []
    
    ### In base al sito, trovo i link alle pagine generiche con le liste di titoli e autori
    genericLinks = []
    if site == "qlibri":
        for c in qCategories:
            for g in qGenres:
                ## seleziono il driver giusto
                genericLinks.append("https://www.qlibri.it/recensioni/"+g+"-narrativa-"+c+"/") 
    elif site == "mondadorilibri": 
        for g in mGenres:
            for pagenum in range(1,8): # numero di pagine
                genericLinks.append("https://www.librimondadori.it/genere/"+g+"/page/"+str(pagenum)+"/")
                print("https://www.librimondadori.it/genere/"+g+"/page/"+str(pagenum)+"/")
    
    ### Titolo, autore, genere, link
    # per ogni link generico trovato...
    for nextLink in genericLinks:
        driver.get(nextLink)
        ## Trovo il genere a cui mi sto riferendo
        g = nextLink.split("/")[4]
        if site == "qlibri": # qlibri ha bisogno di ulteriore formattazione
            splittedg= g.split("-")
            g = splittedg[len(splittedg)-2]+"-"+splittedg[len(splittedg)-1]+"/" # prima la categoria, poi una barra... 
            for i in range (len(splittedg)-2):
                g=g+splittedg[i]+"-" #poi il genere
            g = g[:-1] #tolgo l'ultimo trattino
        ##Estraggo titolo, autore e link alla trama estesa (vedi funzione apposita)
        titles, authors, genres, links = soupScraping(driver, titles, authors, genres, links, g)
    
    ### Trama
    for plotLink in links:
        driver.get(plotLink)    
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        if site == "qlibri":
            # Qlibri è più simpatico: ha direttamente una classe per la trama
            p = soup.find('div', attrs={'class':'contentFulltext'})
            plot = p.text[4:] # via quei brutti tab dall'inizio della trama!
            if plot is None:
                break
        elif site == "mondadorilibri":
            # Mondadorilibri, invece, definisce tutti i contenuti della pagina con la p di paragrafo.
            # Devo trovare, tra tutti i p, quelli della trama.
            # il primo è sempre il 17 (prima ci sono info varie), seguito da un numero variabile di altri paragrafi.
            # la trama finisce quando il paragrafo successivo descrive il genere
            n=17
            plot=""
            while n<30:
                p = soup.find_all('p')[n]
                if p is None or p.text.startswith("Genere: "): # Se la trama è nulla o se si è già passati al genere
                    break;
                else:
                    plot=plot+p.text+" "
                    n+=1
            plot.strip('\n')
            # piccolo controllo se la trama è nulla
            if plot is None:
                break
        
        # Una serie di print per dare un'idea della situazione
        # (questo programma ci mette 25 minuti a girare, diamogli almeno una barra di caricamento!)
        d = datetime.now()-start_time
        
        print("\nTrama n. "+str(numPlot)+"\tTempo passato= "+ str(d.seconds // 3600)+":"+str(d.seconds % 3600 // 60)+":"+str(d.seconds%60))
        print("qlibri:		"+loadingBar(numPlot, max(len(titles), 663)))
        print("mondadorilibri:	"+loadingBar(numPlot-663, min(len(titles), 245)))
        numPlot += 1

        plots.append(plot)
                    

    ### Output su file
    for i in range (0, len(titles)):
        fileWrite(titles[i], authors[i], genres[i], links[i], plots[i])

