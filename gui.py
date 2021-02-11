# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 22:15:05 2021

@author: Serena
"""

import PySimpleGUI as sg
from querying import searchWord

sg.theme('GreenTan')   #Aggiunge colore alla finestra

# Tutta la roba all'interno della finestra
layout = [  [sg.Text('Benvenuto/a nel nostro Search Engine!')],
            
            [sg.Text("Inserire una parola o frase da cercare: "), sg.InputText()],
            
            [sg.Text("In quale categoria cercare: "), sg.OptionMenu(('Tutte', 'Titolo   ', 'Autore', 'Genere', 'Trama'))],
            [sg.Text("In quale sito cercare: "), sg.OptionMenu(('Tutti', 'LibriMondadori', 'Piemme', 'Rizzoli'))],
            
            [sg.Button('Search'), sg.Button('Cancel')],
            [sg.Image(filename="Separator.png")]
         ]

# Creazione della finestra
window = sg.Window('Search Engine', layout, element_justification= 'l')
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # Se l'utente chiude la finestra oppure clicca "Cancel"
        break
    elif event == 'Search':
        print("Hai cercato", values[0])
        results = searchWord(values[0], values[1])
        for r in results:
            print(str(r.score), r['title'],r['author'], r['genre'])
            print(r['content'][:255]+"...\n\n")

window.close()
