from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd

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


## Funzione che fa effettivamente lo scraping, separata dal resto per leggibilità
def soupScraping(driver, titles, authors, plots):
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    ## Estraggo le info e le metto negli array appositi
    for a in soup.findAll(class_='listItem'):
        title=a.find('a',href=True, attrs={'class':'jr_listingTitle'})
        author=a.find('div', attrs={'class':'fieldValue'})
        plot=a.find('div', attrs={'class':'contentIntrotext'})
    
        # piccolo controllo, se non interrompo il ciclo mi dà errore
        if title is None or author is None or plot is None:
            break
        titles.append(title.text)
        authors.append(author.text)
        plots.append(plot.text) 
    # Ritorno gli array per aggiornarli
    return titles, authors, plots
    


### Roba per far andare via il warning e caricare la pagina in fretta
# options = Options()
# options.headless = False
# service = Service('/usr/lib/firefox/geckodriver')

# driver = webdriver.Firefox(options=options, service=service)

driver = webdriver.Firefox('/usr/lib/firefox/')

## Array in cui mettere i risultati
titles=[]
authors=[]
plots=[]

# Array delle pagine di qlibri da raschiare
# (La maggior parte del link è sempre uguale, ho solo memorizzato la parte saliente)
categories=["straniera","italiana"]
genres=["romanzi", "gialli", "racconti", "romanzi-storici", "fantasy", "fantascienza", "classici"]


# Per ognuna delle due categorie...
for c in categories:
    # Per ognuno dei generi...
    for g in genres:
        ## seleziono il driver giusto
        driver.get("https://www.qlibri.it/recensioni/"+g+"-narrativa-"+c+"/")    
        ##Estraggo le info (vedi funzione apposita)
        titles, authors, plots = soupScraping(driver, titles, authors, plots)

# Ho raschiato tutti i link     
# Metto i risultati in tanti file diversi
for i in range(len(plots)):
    outF = open("scraping/"+replaced(titles[i])+".txt", "w")
    outF.write(titles[i]+"\n")
    outF.write(authors[i]+"\n")
    outF.write(plots[i])
    outF.close()





