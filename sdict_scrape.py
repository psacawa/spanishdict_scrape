#! /usr/bin/env python3

import os, re
import requests
import pandas as pd
from bs4 import BeautifulSoup

class EspScrape ():

    #  self.df = pd.DataFrame ()
    #  self.eg = pd.DataFrame ()

    def __init__ (self, limit = 50000):
        """ Initialize by acquiring word frequencies 

        If esp.dict exists, use that, otherwise download.
        """

        if 'esp.dict' in os.listdir ():
            print ("Ładujac hiszpańskie słowa z pliku")
            self.df = pd.read_csv ('esp.dict')
        else:
            print ("Ściągając hiszpańskie słowa z Wikisłownika")
            selt.df = self.get_word_frequencies (limit)

    def get_examples (self, limit=1000):
        """ Pobierz przykładowe hiszpańskie zdania ang/esp z spanishdict.com

        Na kazdą stronę spanishdict.com/translate/* jest kilka definicji i dobrych 
        przykładów użycia. Pobiermy hiszpański wyraz wraz z angielskim przełożeniem
        i umieszczamy w datafrejmie pandas. Wyszukujemy jedynie do <limitu> z
        najczestszych hiszpańskich haseł, omijając powtórzone hasła.
        Listę słow wg. częstotliwość sporządzamy poprzez podrutynę get_word_frequencies
        """

        self.eg = pd.DataFrame (columns = ['ang', 'esp'])
        if not shasattr (self, 'df'):
            print ('Brak listę hiszpańskich słów')
            self.get_word_frequencies ()
        

        # wdróź 


    def get_page_examples (self, s):
        """ Ściągnij stronę ze spanishdict.com pod wyszukanym hasłem i 
            wydobądź wszystkie przykłady, zwracając ich w postaci dataframe z pandas
        """

        url =  'https://www.spanishdict.com/translate/' + s
        r = requests.get (url)
        
        if r.status_code != 200:
            print ('Błąd przy wczytywaniu witryny')
            return

        soup = BeautifulSoup (r.text, 'html.parser')
        links = soup.find_all ('div', class_= 'dictionary-neodict-example')

        col = ['ang', 'esp']
        df =  pd.DataFrame (columns = col)
        #  esp_words = set (get_word_frequencies (limit=100).word)
        #  print (esp_words) 

        for l in links:
            text1, text2 = l.contents[0].text, l.contents[2].text
            score1 = self.spanishness (text1)
            score2 = self.spanishness (text2)
            if score2 < score1:
                text1,text2 = text2, text1
            new_item = pd.Series ([text1, text2], index = col)
            df = df.append (new_item, ignore_index = True)

        return df

    def spanishness (self, s):
        """ Oblicz numeryczną ocenę hiszpańskości zdania.

        Korzystamy z listy słow z częstotliwościami.
        """
        s = s.lower ()
        s = re.sub (' +', ' ', s)
        s = re.sub ('[0-9!?¡¿.,;&%]', '', s)
        words = s.split (' ')
        #  print (words)
        if len (words) == 0:
            return 0

        score = 0
        for w in words:
            subdf = self.df [self.df.word == w]
            #  print (subdf)
            if not subdf.empty:
                print ('Znalezionę słowo {0} z frekwencją {1}'.format (
                    w, subdf.freq.iloc[0]))
                score += subdf.freq.iloc[0]
        return score / len (words)

    def get_word_frequencies (self, limit=50000):
        """ Pobierz listę słów hiszpańskich względem częstotliwości od M. Buchmeiera
            
        Pewien uzytkownik wiktionary pod adresem
        https://en.wiktionary.org/wiki/User:Matthias_Buchmeier
        umieścił odsyłacze do list hiszpańskich słow uporządkowanych  względem 
        czestotliwości. Ta funkcja znajduje te odsyłacze i powołuje podrutrynę
        pobierz_Buchmeier dla każdej z tych odosobnionych stron, zwracając wynik
        w  postaci datafrejmu pandas.
        Limit określa maksymalną ilość słow by pobrać
        """

        if (hasattr (self,'df')):
            return self.df

        domain  = 'https://en.wiktionary.org'
        url = 'https://en.wiktionary.org/wiki/User:Matthias_Buchmeier'
        r = requests.get (url)
        if r.status_code != 200:
            print ('Problem z ściąganiem danych')
            return
        soup = BeautifulSoup (r.text, 'html.parser')
        href_regex = re.compile ('Spanish_frequency.*000')
        
        find_esp_links = lambda t : (t.name == 'a' and t.hasattr ('href')
            and href_regex.search (t['href']) is not None)
        tags = soup.find_all (find_esp_links)
        #  print (tags)

        df = pd.DataFrame (columns = ['word', 'freq'])

        for t in tags:

            if int(re.findall ('\d+', t['href'])[0]) > limit:
                break

            suburl = domain + t['href']
            print ('Wcodząc do {0}'.format (suburl))
            df = df.append (get_page_words (suburl), ignore_index=True)

        df.to_csv ('esp.dict')
        return df

    def get_page_words (self, url):
        """ Pobierz listę słów hiszpańskich od podstrony profilu na wiktionary
        """

        r = requests.get (url)
        if r.status_code != 200:
            print ('Problem z ściąganiem danych')
            return
        soup  = BeautifulSoup (r.text, 'html.parser')

        entries = soup.find ('p').text.split ('\n') [:-1]
        df = pd.DataFrame ()

        for entry in entries:

            if len(entry.split (' ')) != 2:
                print ('Żle sformatowane dane: {0}'.format (entry))
                continue 

            freq, word = entry.split(' ')
            freq = int (freq)
            #  print ('{0} {1}'.format (word, freq))
            df = df.append (pd.Series ([word, freq]), ignore_index = True)

        df = df.rename ( columns={0: 'word',  1:'freq' })
        df['freq'] = df['freq'].astype (int)
        return df

