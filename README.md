![](https://github.com/Cookie-CHR/Books-Search-Engine/blob/main/Titolo.png)

Search Engine verticale a tema libri.

Realizzato in collaborazione tra [@SerenaPassini](https://github.com/SerenaPassini) e [@Cookie-CHR](https://github.com/Cookie-CHR) per l'esame di Gestione dell'Informazione dell'[Unimore](https://www.unimore.it/).

### Com'è andata?

**Errori riscontrati:**
- dimensione della text repository non eccezionale, ma non è stato contato come grande errore perché è comunque un progetto ben scalabile;
- nella presentazione, occorreva dare più spazio alla grammatica del query language e del suo utilizzo;
- servivano più test, abbiamo solo testato il modello di ranking mentre potevamo fare più roba;
- più spazio al thesaurus: test a lui dedicati, magari un toggle o una maniera per attivarlo "a comando" - soprattutto dato che la query expansion coi sinonimi aumenta la recall ma diminuisce la precision, includendo anche significati meno usati del termine (vedi il famoso esempio di "barca" che ha come sinonimo "mucchio").

**Voto ottenuto:** 
28

# Installazione e preparazione
Per cominciare, **scaricare i moduli Python necessari** che abbiamo elencato in [requirements.txt](https://github.com/Cookie-CHR/Books-Search-Engine/blob/main/requirements.txt). Ciò si può fare con un unico comando da shell:

``pip install -r requirements.txt``

Assicurarsi, prima di avviare il programma, di avere nella repository desiderata la directory **Scraping**, e che essa sia popolata da un certo numero di file in formato txt. Se ciò non è avvenuto, o se semplicemente volete ri-eseguire lo scraping in autonomia, eseguite il programma in Python dedicato:

``python3 genericScrape.py``

*Avviso: il programma richiede molto tempo per completare lo scraping, almeno mezz'ora.*

Se avete eseguito lo scraping, dovrete poi **indicizzare** il risultato:

``python3 indexing.py``

# Avviamento

Per avviare il search engine, basta eseguire il main:

``python3 main.py``

![](https://github.com/Cookie-CHR/Books-Search-Engine/blob/main/Separator.png)
