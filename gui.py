# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 22:15:05 2021

@author: Serena
"""

import PySimpleGUI as sg

sg.theme('Dark Blue 3')   #Aggiunge colore alla finestra

# Tutta la roba all'interno della finestra
layout = [  [sg.Text('Benvenuto/a nel nostro Search Engine!')],
            [sg.Text("Inserire una parola o frase da cercare: "), sg.InputText()],
            [sg.Button('Search'), sg.Button('Cancel')] ]

# Creazione della finestra
window = sg.Window('Search Engine', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # Se l'utente chiude la finestra oppure clicca "Cancel"
        break
   # print('You entered ', values[0])

window.close()