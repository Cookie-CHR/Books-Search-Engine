from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from scrapeStruct import book, MondadoriBook, PiemmeBook, RizzoliBook
import string


def replaced(s):
    # sostituisce alcuni caratteri di una stringa con altri.
    # serve per il passaggio da titolo/autore a parte del link
    s = s.translate(str.maketrans('', '', string.punctuation)) # tolgo la punteggiatura
    
    s = s.replace(" ","-")
    s = s.replace("à","a")
    s = s.replace("è","e")
    s = s.replace("é","e")
    s = s.replace("é","e")
    s = s.replace("ì","i")
    s = s.replace("ò","o")
    s = s.replace("ó","o")
    s = s.replace("ö","o")
    s = s.replace("ù","u")
    s = s.replace("ð","d")
    
    return s

## funzione che si occupa dell'output su file
def fileWrite(title, author, genre, link, price, plot):
    outF = open("scraping/"+replaced(title)+".txt", "w")
    outF.write(title+"\n")
    outF.write(author+"\n")
    outF.write(genre+"\n")
    outF.write(link+"\n")
    outF.write(price+"\n")
    outF.write(plot)
    outF.close()


# Options
options = Options()
# Specify custom geckodriver path
service = Service('/usr/lib/firefox/geckodriver')

driver = webdriver.Firefox(options=options, service=service)

# per ognuno dei siti...
for b in [PiemmeBook(), RizzoliBook(), MondadoriBook()]:
    
    ### In base al sito, trovo i link alle pagine generiche con le liste di titoli e autori
    genericLinks = b.findGenerics()
    
    ### Titolo, autore, genere, link
    # per ogni link generico trovato...
    for nextLink in genericLinks:
        driver.get(nextLink)
        ## Trovo il genere a cui mi sto riferendo
        g = nextLink.split("/")[4]

        ##Estraggo titolo, autore e link alla trama estesa (vedi funzione apposita)
        b.soupScrapeGeneral(driver, g)
    b.soupScrapeDeep(driver, g)

    ### Output su file
    for i in range (0, len(b.titles)):
        fileWrite(b.titles[i], b.authors[i], b.genres[i], b.links[i], b.prices[i], b.plots[i])



