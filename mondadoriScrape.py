from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import re


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

driver = webdriver.Firefox('/usr/lib/firefox/')

## Array in cui mettere i risultati
titles=[]
authors=[]
plots=[]

# Array delle pagine di qlibri da raschiare
# (La maggior parte del link è sempre uguale, ho solo memorizzato la parte saliente)

genres=["gialli-e-thriller", "narrativa-contemporanea", "romanzi-storici-fantasy-e-fantascienza"]

# Per ognuno dei generi...
for g in genres:
    # e per ognuna delle prime 7 pagine...
    for pagenum in range(1,8):
        ## seleziono il driver giusto
        currentLink = "https://www.librimondadori.it/genere/"+g+"/page/"+str(pagenum)+"/"
        driver.get(currentLink)    
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
         
        ## Estraggo le info su titolo e autore e le metto negli array appositi
        for a in soup.findAll(class_='product-info'):
            title= a.find('a', attrs={'href' : re.compile('https://www.librimondadori.it/libri/.*')})
            author=a.find('a', attrs={'href' : re.compile('https://www.librimondadori.it/autore/.*')})
            if title is None or author is None:
                break
            titles.append(title.text)
            authors.append(author.text)
        
## in differita, mi occupo delle trame  e del salvataggio in file
for quel in range(0, len(titles)):
              
    nextLink="https://www.librimondadori.it/libri/"+replaced(titles[quel])+"-"+replaced(authors[quel])+"/"
            
    driver.get(nextLink)    
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # trovo, tra tutti i p, quelli della trama.
    # il primo è sempre il 17, seguito da un numero variabile di altri paragrafi.
    # la trama finisce quando il paragrafo successivo descrive il genere
    n=17
    plot=""
    while n<30:
        p = soup.find_all('p')[n]
        if p is None or p.text.startswith("Genere: "):
            break;
        if p.text.startswith('\n'):
            plot=""
        else:
            plot=plot+p.text+" "
            n+=1
    # piccolo controllo se la trama è nulla
    if plot is None:
        break
    plots.append(plot) 
    
    # Metto i dati del libro selezionato su un file
    # open a (new) file to write
    outF = open("scraping/"+replaced(titles[quel])+".txt", "w")
    outF.write(titles[quel]+"\n")
    outF.write(authors[quel]+"\n")
    outF.write(plot)
    outF.close()
    
# Ho raschiato tutti i link
   



