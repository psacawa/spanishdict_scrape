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

def get_polly_voices (limit= 10, eng_voice = 'Joanna', esp_voice = 'Mia'):
    """ Wyślij prósby o pliki do silnika TTS z AWS, Amazon Polly 
        i zapisz angiel/hispańskie ścieżki dwiękowe w ang/ i esp/
        limit - limit przykładów
        eng_voice = angielski głos sztuczny
        esp_voice = hiszpański głos sztuczny : możliwe 
             'Lucia' - kastyliański 
             'Mia' - meksykański
    """

    if 'esp_eg.dict' not in os.listdir ():
        print ('Utwórz plik przykładów csv')
        return

    df = pd.read_csv ('esp_eg.dict')

    # zrób katalogi w których będą się mieściły pliki głosowe
    # wybór regionu jeśli hiszpańskie
    eng_folder = '{0}_{1}'.format (eng_voice, 'en-US')
    esp_folder = '{0}_{1}'.format (esp_voice, 
        'es-MX' if esp_voice == 'Mia' else 'es-ES'
    )
    if not os.path.isdir (eng_folder):
        os.mkdir (eng_folder)
    if not os.path.isdir (esp_folder):
        os.mkdir (esp_folder)

    for c,s in df[:limit].iterrows ():

        eng_file = '{0}/{1}.mp3'.format (eng_folder, str(c).zfill (6))
        esp_file = '{0}/{1}.mp3'.format (esp_folder, str(c).zfill (6))

        if not os.path.isfile (eng_file):
            subprocess.call (
                ['aws', 'polly',  'synthesize-speech',
                    '--output-format', 'mp3',
                    '--voice-id', eng_voice,
                    '--text', s.ang,
                    eng_file]
            )

        if not os.path.isfile (esp_file):
            subprocess.call (
                ['aws', 'polly',  'synthesize-speech',
                    '--output-format', 'mp3',
                    '--voice-id', esp_voice,
                    '--text', s.esp,
                    esp_file]
            )




# można wdrożyć pollowanie klawiatury poprzez select, ale na razie nie wiadomo jak
def heardEnter():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return True
    return False
