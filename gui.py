# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 22:15:05 2021

@author: Serena
"""

import PySimpleGUI as sg
import re
import string
import subprocess, os, platform
from querying import searchWord

sg.theme('GreenTan')   #Aggiunge colore alla finestra

def replaced(s):
    # sostituisce alcuni caratteri di una stringa con altri.
    # serve per il passaggio da titolo/autore a parte del link
    s = s.translate(str.maketrans('', '', string.punctuation)) # tolgo la punteggiatura
    
    s = s.replace("\n","")
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
             
def updateField(i, r):
    # aggiorna un campo (rappresentato dall'index i) facendogli mostrare i dati di un risultato (r)
    window['-COLUMN'+str(i)+'-'].update(visible=True)
    
    # vuoto il contenuto precedente e lo ri-riempio
    window['-FIELD'+str(i)+'-'].update("")
    window['-FIELD'+str(i)+'-'].print(str(i+1)+"  "+r['title'].replace("\n", "")+", "+r['author'].replace("\n", ""), \
                                      background_color='#475841', text_color='white')
    window['-FIELD'+str(i)+'-'].print(r['genre']+r['content'][:255]+"...")

def hideField(i):
    # Ho finito i risultati da mostrare: il campo verrà nascosto e svuotato
    window['-COLUMN'+str(i)+'-'].update(visible=False)
    window['-FIELD'+str(i)+'-'].update("")



#un risultato, associato al suo bottone
def fieldSingle(i):
    return [[sg.Button("Vai alla pagina", key='-BUTTON'+str(i)+'-', size=(6,8)), 
            sg.MLine("", key='-FIELD'+str(i)+'-', size=(70,9), disabled=True, autoscroll = False)
           ]]
# tocca raggruppare questi puzzoni in una colonna, sennò non si allineano
def fieldCol(i):
    return [sg.Column(layout=fieldSingle(i), key='-COLUMN'+str(i)+'-', visible=False)]
# L'intera colonna dei risultati (inizializzata separatamente per essere scrollabile
resCol = [  fieldCol(i) for i in range(0,10)]



# Tutta la roba all'interno della finestra
layout = [  [sg.Text('Benvenuto/a nel nostro Search Engine!')],

            [sg.Text("Inserire una parola o frase da cercare: "), sg.InputText()],
            
            [sg.Text("In quale categoria cercare: "), sg.OptionMenu(('Tutte', 'Titolo', 'Autore', 'Genere', 'Trama'), size=(10,1))],
            [sg.Text("In quale sito cercare:  "), sg.OptionMenu(('Tutti', 'LibriMondadori', 'Piemme', 'Rizzoli'), size=(14,1))],
            
            [sg.Button('Search'), sg.Button('Cancel')],
            [sg.Image(filename="Separator.png")],
            [sg.Text("", key='-OutputStart-', size=(100,1))],
            [sg.Column(resCol, size=(610,400), scrollable=True, key='-COLUMN-', vertical_scroll_only = True)]
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
        for i in range(0,10):
            if i < len(results):
                updateField(i, results[i])
            else:
                hideField(i)
        window.refresh()                            # refresh required here
        window['-COLUMN-'].contents_changed()  
    elif re.match(r'-BUTTON.*', event):
        # ricavo il bottone
        i = int(event[7:-1])
        #ricavo il path del file corrispondente
        filepath = os.getcwd()+"/scraping/"+replaced(results[i]['title'])+".txt"
        # apro il file
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # linux variants
            subprocess.call(['xdg-open', filepath])
window.close()

