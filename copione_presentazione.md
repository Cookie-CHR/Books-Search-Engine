Il nostro progetto è un search engine a tema libri. È un tema piuttosto generico, i libri hanno tante caratteristiche che avremmo potuto prendere con lo scraping, e abbiamo optato per: titolo, trama, genere (estratto a braccio in base alla pagina da cui è stato prelevato il libro), link alla pagina e prezzo.

Abbiamo cercato dei siti che descrivessero i libri usando queste caratteristiche, e siamo finite nei siti delle case editrici, e nello specifico in tre siti piuttosto forniti: Rizzoli, Piemme e Mondadori.

Lo scraping avviene in due fasi:
- nella prima fase, il programma va nelle pagine più “generiche”, quelle quindi in cui si può trovare una lista di molti libri, ma non dettagliati, con dei link che vanno alla pagina di ogni libro. Da qui veniva appunto ricavato un array di link (più qualche altra informazione già estraibile, come ad esempio il titolo dei libri).

- Nella seconda fase, quella “approfondita”, il programma apre invece la pagina di ogni singolo libro, che ne contiene una descrizione dettagliata, e da lì vengono estratte le caratteristiche di cui sopra. Una volta terminata anche questa fase, ciascun libro finisce in un file txt, che verrà indicizzato in una fase successiva.

Un problema che abbiamo dovuto affrontare è stato: “che fare se lo scraping di un libro è incompleto?” ad esempio se un link è rotto e manda a una pagina inesistente. Avevamo due opzioni: tenere i libri estratti male, e assegnare ai campi falliti valori di default, che avrebbero portato alla costruzione di una lista più lunga ma “spuria”, e invece cancellare suddetti titoli dallo scraping e passare oltre, ottenendo una lista breve ma completa di tutte le informazioni. Abbiamo preferito questa seconda opzione.

Finito lo scraping, la seconda fase da affrontare è l’indexing. Bla bla bla questo campo l’abbiamo rappresentato così e quello colà.

La trama viene anche sottoposta a pre-processing: è stata infatti tokenizzata, le stopwords eliminate e non mi ricordo se è stato pure effettuato lo stemming o no.

Parliamo ora delle query: Di base abbiamo utilizzato whoosh, e abbiamo deciso di lasciare come modello di ranking il bm25 predefinito [allungare il brodo qui]. 

Abbiamo deciso di fare scegliere all’utente la categoria in cui effettuare lo scraping: potrebbe cercare fra i soli titoli, o le trame, o altro ancora, o fra tutti i dati indicizzati. Inoltre l’utente può scegliere la fascia di prezzo a lui più congeniale e il sito da cui è stato prelevato il libro (quindi, in senso lato, anche la casa editrice). Queste ultime due scelte sono state messe a punto tramite post-processing dei risultati, escludendo quelli che non soddisfacevano i requisiti.

È qui che entra in scena, inoltre, il thesaurus: i libri affrontano un range di argomenti vastissimo quindi un thesaurus specializzato sarebbe stato inutilizzabile, abbiamo quindi optato per il più generico wordnet, con il dizionario in italiano installato non so come, Sere ti prego trova qualcosa da scrivere qui.

Il thesaurus è stato principalmente usato per la query expansion tramite sinonimi: infatti, quando viene cercata una singola parola, vengono inclusi anche i risultati per i suoi sinonimi, opportunamente ordinati.

Infine, la gui. È stato utilizzato pysimplegui. [descrizione dei vari campi con esempio pratico, magari anche inserzione di un non-float nei prezzi così si vede che è stato gestito l’errore]
Veniamo ora alla fase di testing: Abbiamo pensato a queste query [query con descrizione del perché ogni query è particolare]

Abbiamo provato a confrontare il bm25 predefinito di Whoosh, il modello tf-idf e un altro bm25 ma con i parametri scelti da noi. [risultati e grafichetto relativo in 2-3 slide]
