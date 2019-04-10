#! /usr/bin/env python3

import os
import sys
import select
import subprocess
import pandas as pd
import pyttsx3
from time import sleep

def say_examples (limit = 2, eng_repetitions= 1, esp_repetitions = 3, delay = 20):
    """ Wymów najpierw po angielsku, potem po hiszpańsku przykłady z esp_eg.dict

    limit - ile przykładów powiedzieć
    eng/esp_repetitions - ile razy powtarzać angielskie/hiszpańskie
    delay pausa między zdań
    """

    # załaduj przykłady
    if 'esp_eg.dict' not in os.listdir ():
        print ('Nie ma przykładów')
        return
    df = pd.read_csv ('./esp_eg.dict') 
    df = df [0:limit]

    # zincijalizuj silniki TTS
    eng_engine = pyttsx3.init ()
    eng_engine.setProperty ('voice', 'english-us')
    eng_engine.setProperty ('rate', 150)

    esp_engine = pyttsx3.init ()
    esp_engine.setProperty ('voice', 'english-us') # nie ma hiszpańskiego ???
    esp_engine.setProperty ('rate', 150)

    # odczytaj przykłady
    for (c,s) in df.iterrows ():
        print ('=' * 50)
        print (s.ang)
        print (s.esp)

        # na razie polegan na systemowe wywołanie espeak...
        # naprawić??
        for c in range (eng_repetitions):
            #  eng_engine.say (s.ang)
            #  eng_engine.runAndWait ()
            subprocess.call (['espeak', '-v', 'english-us', s.ang])
            sleep (delay)

        for c in range (esp_repetitions):
            #  esp_engine.say (s.esp)
            #  esp_engine.runAndWait ()
            subprocess.call (['espeak', '-v', 'spanish', s.esp])
            sleep (delay)

def heardEnter():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return True
    return False
