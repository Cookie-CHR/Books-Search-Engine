![](https://github.com/Cookie-CHR/Books-Search-Engine/blob/main/Titolo.png)

Search Engine verticale a tema libri.

Realizzato in collaborazione tra [@SerenaPassini](https://github.com/SerenaPassini) e [@Cookie-CHR](https://github.com/Cookie-CHR) per l'esame di Gestione dell'Informazione dell'[Unimore](https://www.unimore.it/).

# Installazione e preparazione
Prima di tutto, **clonare questa repo** ed estrarne i contenuti, tramite l'apposito pulsante o digitando sulla vostra shell il comando

``git clone https://github.com/Cookie-CHR/Books-Search-Engine``

Dopodiché, **scaricare gli import necessari**, che abbiamo elencato in [requirements.txt](https://github.com/Cookie-CHR/Books-Search-Engine/blob/main/requirements.txt). Ciò si può fare con un unico comando da shell:

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

