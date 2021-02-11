# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 22:15:05 2021

@author: Serena
"""

import PySimpleGUI as sg
from querying import searchWord

sg.theme('GreenTan')   #Aggiunge colore alla finestra

def updateField(field, r):
    # aggiorna un campo (field) facendogli mostrare i dati di un risultato (r)
    field.update(visible=True)
    # vuoto il contenuto precedente e lo ri-riempio
    field.update("")
    field.print(str(i)+"  "+r['title'].replace("\n", "")+", "+r['author'].replace("\n", "")+"\n", \
                 background_color='sea green', text_color='white', )
    field.print(r['genre']+r['content'][:255]+"...")
    print(str(r.score), r['title'],r['author'], r['genre'])

def hideField(field):
    # Ho finito i risultati da mostrare: il campo field verrà nascosto e svuotato
    field.update(visible=False)
    field.update("")

# L'intera colonna dei risultati (inizializzata separatamente per essere scrollabile
resCol = [  [sg.MLine("", key='-FIELD1-', size=(80,9), visible=False)],
            [sg.MLine("", key='-FIELD2-', size=(80,9), visible=False)],
            [sg.MLine("", key='-FIELD3-', size=(80,9), visible=False)],
            [sg.MLine("", key='-FIELD4-', size=(80,9), visible=False)],
            [sg.MLine("", key='-FIELD5-', size=(80,9), visible=False)],
            [sg.MLine("", key='-FIELD6-', size=(80,9), visible=False)],
            [sg.MLine("", key='-FIELD7-', size=(80,9), visible=False)],
            [sg.MLine("", key='-FIELD8-', size=(80,9), visible=False)],
            [sg.MLine("", key='-FIELD9-', size=(80,9), visible=False)],
            [sg.MLine("", key='-FIELD10-', size=(80,9), visible=False)],
         ]



# Tutta la roba all'interno della finestra
layout = [  [sg.Text('Benvenuto/a nel nostro Search Engine!')],
            
            [sg.Text("Inserire una parola o frase da cercare: "), sg.InputText()],
            
            [sg.Text("In quale categoria cercare: "), sg.OptionMenu(('Tutte', 'Titolo   ', 'Autore', 'Genere', 'Trama'))],
            [sg.Text("In quale sito cercare: "), sg.OptionMenu(('Tutti', 'LibriMondadori', 'Piemme', 'Rizzoli'))],
            
            [sg.Button('Search'), sg.Button('Cancel')],
            [sg.Image(filename="Separator.png")],
            [sg.Text("", key='-OutputStart-', size=(100,1))],
            [sg.Column(resCol, size=(600,400), scrollable=True, key='-COLUMN-')]
         ]
         
# Creazione della finestra
window = sg.Window('Search Engine', layout, element_justification ='l', size=(700,700))


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == 'Cancel': # Se l'utente chiude la finestra oppure clicca "Cancel"
        break
    elif event == 'Search':
        # eseguo la query
        results = searchWord(values[0], values[1])
        
        #Risultati! Iniziamo dalla riga di intestazione
        window['-OutputStart-'].update("Hai cercato "+values[0]+": Sono stati ritrovati "+str(len(results))+" risultati.") 
        
        #Poi mostriamo i risultati effettivi uno a uno
        i=1
        for r in results:
            updateField(window['-FIELD'+str(i)+'-'], r)
            i+=1
        for j in range (i, 10+1):
            hideField(window['-FIELD'+str(j)+'-'])
            j+=1
        window.refresh()                            # refresh required here
        window['-COLUMN-'].contents_changed()  
window.close()

