from selenium import webdriver
from bs4 import BeautifulSoup
import re
import string

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
    
    str = str.replace("À","A")
    str = str.replace("È","E")
    str = str.replace("É","E")
    str = str.replace("Ì","I")
    str = str.replace("Ò","O")
    str = str.replace("Ù","U")
    
    str = str.replace("ð","d")
    str.strip('\n')
    return str
    
def somethingWrong(boolA, A, boolB, B, boolC, C, boolD, D, boolE, E):
    return bool((boolA and A is None) or (boolB and B is None) or (boolC and C is None) or (boolD and D is None) or (boolE and E is None))

class book: 
    ## Classe padre, generica

    # Funzioni per ritornare i vari attributi: saranno definite nelle classi figlie
    def findGenerics(self):
        pass 
        
    def findTitle(self, soup):
        pass
    def findAuthor(self, soup):
        pass
    def findLink(self, soup):
        pass
    def findGenre(self, soup):
        pass
    def findPlot(self, soup):
        pass
    def findPrice(self, soup):
        pass
        
    ### Queste piccole funzioni definiscono se eseguire o no lo scraping di una determinata categoria
    #   Servono per sapere quali categorie estrarre in soupScrapeGeneral e quali in soupScrapeDeep 
    def ifTitle(self, soup, titleBool):
        if titleBool:
            t = self.findTitle(soup)
            if t is not None:
                if not isinstance(t, str):
                    t = t.text
                return t
    def ifAuthor(self, soup, authorBool):
        if authorBool:
            a = self.findAuthor(soup)
            if a is not None:
                if not isinstance(a, str):
                    a = a.text
                return a
    def ifGenre(self, soup, genreBool):
        if genreBool:
            g = self.findGenre(soup)
            if g is not None:
                if not isinstance(g, str):
                    g = g.text
                return g
    def ifPrice(self, soup, priceBool):
        if priceBool:
            p = self.findPrice(soup)
            if p is not None:
                if not isinstance(p, str):
                    p = p.text
                return p
    def ifPlot(self, soup, plotBool):
        if plotBool:
            p = self.findPlot(soup)
            if p is not None:
                if not isinstance(p, str):
                    p = p.text
                return p
        
    def __init__(self):
        ## inizializzo tutti gli array che mi servono   
        self.genericClass = ""
    
        self.titles = []
        self.authors = []
        self.plots = []
        self.prices = []
        self.genres = []
        self.links = []
    
    
    def soupScrapeGeneral(self, driver, g, titleBool, authorBool, genreBool, priceBool, plotBool):
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')        
        
        ## Estraggo le info già deducibili dalla pagina principale
        for soup in soup.find_all(class_= self.genericClass):
            title = self.ifTitle(soup, titleBool)
            author = self.ifAuthor(soup, authorBool)
            genre = self.ifGenre(soup, genreBool)
            price = self.ifPrice(soup, priceBool)
            plot = self.ifPlot(soup, plotBool)
            
            # Creo il link (questo va fatto per forza nella pagina principale, un ifLink non avrebbe senso)
            link = self.findLink(soup).replace("\n","")
            
            ## Check che tutto sia sincronizzato
            if not somethingWrong(titleBool, title, authorBool, author, genreBool, genre, priceBool, price, plotBool, plot):
                if link is not None:
                    # appendo i risultati ai loro array
                    self.links.append(link)
                    if(titleBool): self.titles.append(title.replace("\n",""))
                    if(authorBool): self.authors.append(author.replace("\n",""))
                    if(genreBool): self.genres.append(genre.replace("\n",""))
                    if(priceBool): self.prices.append(price.replace("\n",""))
                    if(plotBool): self.plots.append(plot.replace("\n",""))
                
            
        
    def soupScrapeDeep(self, driver, g, titleBool, authorBool, genreBool, priceBool, plotBool):
        ## In differita, dalla pagina di ogni libro estraggo il resto
        #  itererò su una copia dell'array dei link, perché quello ufficiale può subire modifiche nel corso dello scraping
        plotLinks = self.links.copy()
        for plotLink in plotLinks:
            driver.get(plotLink)    
            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            
            #Estraggo le info richieste, e solo quelle
            title = self.ifTitle(soup, titleBool)
            author = self.ifAuthor(soup, authorBool)
            genre = self.ifGenre(soup, genreBool)
            price = self.ifPrice(soup, priceBool)
            plot = self.ifPlot(soup, plotBool)
            
            ## Check che tutto sia sincronizzato
            if somethingWrong(titleBool, title, authorBool, author, genreBool, genre, priceBool, price, plotBool, plot):
                # C'è un problema, trovo qual è l'index in cui si è verificato e quali sono gli array da modificare
                highs = [self.links]
                problematicIndex = None
                if (titleBool): problematicIndex = len(self.titles)
                else: highs.append(self.titles)
                if (authorBool): problematicIndex = len(self.authors)
                else: highs.append(self.authors)
                if (genreBool): problematicIndex = len(self.genres)
                else: highs.append(self.genres)
                if (priceBool): problematicIndex = len(self.prices)
                else: highs.append(self.prices)
                if (plotBool): problematicIndex = len(self.plots)
                else: highs.append(self.plots)
                    
                print("Errore, verrà tolto il libro di index ", problematicIndex, ",",self.titles[problematicIndex])
                
                # tolgo dagli array "grossi" il dato che crea problemi
                for array in highs:
                        array.pop(problematicIndex)
                        
                
            else: # se tutto è ok, appendo i risultati ai loro array
                if(titleBool): self.titles.append(title.replace("\n",""))
                if(authorBool): self.authors.append(author.replace("\n",""))
                if(genreBool): self.genres.append(genre.replace("\n",""))
                if(priceBool): self.prices.append(price.replace("\n",""))
                if(plotBool): self.plots.append(plot.replace("\n",""))
            
            print(len(self.plots), "/",len(self.titles), "	", self.titles[len(self.plots)-1])
        print ("Finito il soupscrape!")
class MondadoriBook(book):
    def __init__(self):
        super().__init__()
        self.genericClass = 'product-info'
    
    def findGenerics(self):
        genericLinks = []
        for g in ["gialli-e-thriller", "narrativa-contemporanea", "romanzi-storici-fantasy-e-fantascienza", "biografie-e-memoir"]:
            for pagenum in range(1,8): # numero di pagine
                pagenum = str(pagenum)
                genericLinks.append("https://www.librimondadori.it/genere/"+g+"/page/"+pagenum+"/")
        return genericLinks
    
    def findTitle(self, soup):
        return soup.find('a', attrs={'href' : re.compile('https://www.librimondadori.it/libri/.*')})
    def findAuthor(self, soup):
        return soup.find('a', attrs={'href' : re.compile('https://www.librimondadori.it/autore/.*')})
    def findLink(self, soup):
        return soup.find('a', attrs={'href' : re.compile('https://www.librimondadori.it/libri/.*')})['href']
    def findGenre(self, soup):
        for p in soup.find_all('p'):
            if p.text.startswith("Genere: "):
                return p.text[8:]
        
    def findPlot(self, soup):
        n=17
        pp=""
        while n<30:
            p = soup.find_all('p')[n]
            if p is None or p.text.startswith("Genere: "): # Se la trama è nulla o se si è già passati al genere
                break;
            else:
                pp=pp+p.text+" "
                n+=1
        pp.strip('\n')
        
        return pp
    def findPrice(self, soup):
        for p in soup.find_all('p'):
            if p.text.startswith("Prezzo: "):
                return p.text[8:]
        return None
        
    def soupScrapeGeneral(self, driver, g):
        super().soupScrapeGeneral(driver, g, True, True, False, False, False)
            
    def soupScrapeDeep(self, driver, g):
        super().soupScrapeDeep(driver,g, False, False, True, True, True)




class PiemmeBook(book):
    def piemmeReplaced(self, t):
        # Piemme, oltre agli altri criteri di replace, non ammette maiuscole e punteggiatura
        t = t.translate(str.maketrans('', '', string.punctuation))
        
        t = replaced(t)
        t = t.lower()
        return t
            
    def __init__(self):
        super().__init__()
        self.genericClass = 'col-sm-3'
    
    def findGenerics(self):
        genericLinks = []
        for g in ["fiction-thriller", "fiction-varia", "fiction-storici","non-fiction-memoir", "non-fiction-varia"]:
            for pagenum in range(1,11): # numero di pagine
                pagenum = str(pagenum)
                genericLinks.append("https://www.edizpiemme.it/catalogo/adulti-"+g+"/?page="+pagenum)
        return genericLinks
    
    def findTitle(self, soup):
        t = soup.find('div', attrs={'class': 'post-heading'})
        if t is not None:
            t = t.text[1:-1] # questioni di formattazione, tolgo un invio da inizio frase e uno dalla fine
        return t
    def findAuthor(self, soup):
        return  soup.find('a', attrs={'href' : re.compile('/autori/.*'), 'title': re.compile('Vai alla scheda dell\'autore .*')})
    def findLink(self, soup):
        link = soup.find('a', attrs={'href' : re.compile('/libri/.*')})
        if link is not None:
            link = "https://www.edizpiemme.it"+link['href']
        return link
    def findGenre(self, soup):
        g = ""
        for gen in soup.find_all('a', href=True, attrs={'title': re.compile('Vai al catalogo libri')}):
            g = g + gen.text + " "
        return g
    def findPlot(self, soup):
        p = soup.find('p')
        if p is not None:
            p = p.text
        return p
    def findPrice(self, soup):
        return soup.find('span', attrs={'class': ['pull-right']})
        
    def soupScrapeGeneral(self, driver, g):
        super().soupScrapeGeneral(driver, g, True, False, False, False, False,)
    def soupScrapeDeep(self, driver, g):
        super().soupScrapeDeep(driver,g, False, True, True, True, True)
               
        
class RizzoliBook(book):
    def __init__(self):
        super().__init__()
        self.genericClass = 'slider-ndnp-obj'
    
    def rizzoliReplaced(self, t):
        #Anche Rizzoli non vuole punteggiatura
        # Piemme, oltre agli altri criteri di replace, non ammette maiuscole e punteggiatura
        t = t.translate(str.maketrans('', '', string.punctuation))
        t = t.replace("’","")
        t = replaced(t)
        return t
        
    def findGenerics(self):
        genericLinks = []
        for g in ["san-valentino-storia-d-amore", "il-mondo-visto-dagli-animali", "giornata-mondiale-dellambiente-libri", \
        "nero-rizzoli", "halloween-24-libri", "bur-verdi", "gatti-blu", "libri-da-leggere-sotto-lombrellone-estate-2017", \
        "libri-ragazzi-estate-2017", "oltre-il-confine", "libri-da-regalare", "universi-paralleli", "narrativa-italiana-news", \
        "gialli-attraverso-litalia", "love-is-love", "merry-books-fiction"]:
            genericLinks.append("https://www.rizzolilibri.it/percorsi/"+g+"/")
        return genericLinks
    
    def findTitle(self, soup):
        title = soup.find('p', attrs={'class' : 'mt_20', 'class':'blue', 'class':'bold'})
        if title is not None:
            return title.text
    def findAuthor(self, soup):
        author = soup.find('p', attrs={'class' : 'page-subtitle', 'class':'mt_5'})
        if author is not None:
            return author.text[6:-4]+"\n" # tolgo i tab a inizio e fine riga
    def findLink(self, soup):
        link = soup.find('a', href=True, attrs={'class':'slider-ndnp-image'})
        if link is not None:        
            return link['href']
        return None
    def findGenre(self, soup):
        tempGen = None
        for li in soup.find_all('li'):
            if li.text.startswith("Marchio: "):
                tempGen = li.text.replace("Marchio: ", "").replace("	", "")
            if li.text.startswith("Collana: "):
                return li.text.replace("Collana: ", "").replace("	", "")
        return tempGen
                
    def findPlot(self, soup):
        plot = soup.find( attrs={'class' : 'gray', 'class':'mt_20', 'class':'min500'})
        if plot is not None:
            return plot.text.replace("\n","")
    def findPrice(self, soup):
        for li in soup.find_all('li'):
            if li.text.startswith("Prezzo: "):
                return li.text+"\n" 
        
    def soupScrapeGeneral(self, driver, g):
        super().soupScrapeGeneral(driver, g, True, False, False, False, False)
            
    def soupScrapeDeep(self, driver, g):
        super().soupScrapeDeep(driver,g, False, True, True, True, True)


