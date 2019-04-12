#! /usr/bin/env python3

import os
import re
from time import sleep
import requests
import pandas as pd
from bs4 import BeautifulSoup
import subprocess

# zbagowane, self.freqlist jest przepisane jakoś przez get_examples ()

class EspScrape ():

    #  self.freqlist = pd.DataFrame ()
    #  self.eglist = pd.DataFrame ()

    def __init__ (self, word_limit = 50000, eg_limit = 1000):
        """ Initialize by acquiring word frequencies 

        If esp.dict exists, use that, otherwise download.
        """

        if 'esp.dict' in os.listdir ():
            print ('Ładujac hiszpańskie słowa z pliku')
            self.freqlist = pd.read_csv ('esp.dict')
        else:
            print ('Ściągając hiszpańskie słowa z Wikisłownika')
            self.get_word_frequencies (word_limit)

        if 'esp_eg.dict' in os.listdir ():
            print ('Ładując przykłądy z pliku')
            self.eg = pd.read_csv ('esp_eg.dict')
        else:
            print ('Ściągajać przykłądy  z spanishdict.com')
            self.get_examples (eg_limit)

        
    def get_examples (self, limit=1000, delay=3):
        """ Pobierz przykładowe hiszpańskie zdania ang/esp z spanishdict.com

        Na kazdą stronę spanishdict.com/translate/* jest kilka definicji i dobrych 
        przykładów użycia. Pobiermy hiszpański wyraz wraz z angielskim przełożeniem
        i umieszczamy w datafrejmie pandas. Wyszukujemy jedynie do <limitu> z
        najczestszych hiszpańskich haseł, omijając powtórzone hasła.
        Listę słow wg. częstotliwość sporządzamy poprzez podrutynę get_word_frequencies
        """

        self.eg = pd.DataFrame (columns = ['ang', 'esp'])
        if not hasattr (self, 'freqlist'):
            print ('Brak listę hiszpańskich słów')
            self.get_word_frequencies ()

        # znajdź miejsce w którym ostałeś
        #  if hasattr (self, 'eg'):

        
        words = self.freqlist['word'].iloc [0:limit]
        seen = set ()

        for (n,w) in enumerate(words):

            # ściągnij przykłady ze strony
            print ('Ściągając przykłądy dla #{0}: {1}'.format (n,w))
            ret = self.get_page_examples (w, mode='online')

            # iteruj przez przykłady ze strony; jeśli którakolwiek będzie powtórzony,
            # przechodzimy do nastepnego słowa...
            for c,s in ret.iterrows ():
                if s.ang not in seen:
                    seen |= { s.ang }
                    self.eg = self.eg.append (s,ignore_index=True)
                else:
                    print ('Powtórka znalezonia: {}'.format (w))
                    break

            #  self.eg = self.eg.append (self.get_page_examples (w), ignore_index =True)

            # usypia program przez kilka sek.
            # bez tego, bo kilkuset pomyślnych próśb http witrynia
            # odmawia dalszej usługi
            sleep (delay)

        self.eg.to_csv ('esp_eg.dict',index=False)

        return self.eg
    
    def get_local_examples (self, limit = 0):
        """ Zbuduj dataframe lokalnych przykładów i zapisz rezulujący dataframe
            limit - limit wpisów do przetwarzania. Kolejność losowa...
            Jeśli nie ma limitu, za przetwórz cały catalog
        """
        
        # może odrębna zmienna ??
        self.eg = pd.DataFrame (columns = ['ang', 'esp'])
        prog = re.compile ('^(.*)\.html$')
        seen = set ()

        files = os.listdir ('./www.spanishdict.com/translate')
        if limit == 0:
            limit = len (files)

        for f in files[:limit]:
            
            # wydobądź  wpis on nazwy pliku
            match = prog.search (f)
            if not match:
                print ('Błąd przy parsowaniu pliku {}'.format (f))
                break
            entry = match.groups ()[0]

            print ('Ładując przykłądy dla {0}'.format (entry))
            ret = self.get_page_examples (entry, mode='local')

            # iteruj przez przykłady ze strony; jeśli którakolwiek będzie powtórzony,
            # przechodzimy do nastepnego słowa...
            for c,s in ret.iterrows ():
                if s.ang not in seen:
                    seen |= { s.ang }
                    self.eg = self.eg.append (s,ignore_index=True)
                else:
                    print ('Powtórka znalezonia: {}'.format (entry))
                    break

        # zapisz
        self.eg.to_csv ('esp_eg.dict', index=False)
        return self.eg
        


    def get_page_examples (self, s, mode = 'online'):
        """ Ściągnij stronę ze spanishdict.com pod wyszukanym hasłem i 
            wydobądź wszystkie przykłady, zwracając ich w postaci dataframe z pandas
            możliwe wartości mode:  'onine', 'local'
        """
        if mode == 'online':
            # ściąganie z sieci
            url =  'https://www.spanishdict.com/translate/' + s
            r = requests.get (url)
            if r.status_code != 200:
                print ('Błąd przy wczytywaniu witryny')
                return
            page_html = r.text

        elif mode == 'local':
            # ładowanie z pliku
            filename =  'www.spanishdict.com/translate/{}.html'.format (s)
            page_html = open (filename).read ()

        else:
            print ('Możliwe wartości mode to "online", "local"')

        soup = BeautifulSoup (page_html, 'html.parser')
        links = soup.find_all ('div', class_= 'dictionary-neodict-example')

        col = ['ang', 'esp']
        df =  pd.DataFrame (columns = col)

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
            subdf = self.freqlist [self.freqlist['word'] == w]
            #  print (subdf)
            if not subdf.empty:
                #  print ('Znalezionę słowo {0} z frekwencją {1}'.format (
                #      w, subdf.freq.iloc[0]))
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

        if (hasattr (self,'freqlist')):
            return self.freqlist

        domain  = 'https://en.wiktionary.org'
        url = 'https://en.wiktionary.org/wiki/User:Matthias_Buchmeier'
        r = requests.get (url)
        if r.status_code != 200:
            print ('Problem z ściąganiem danych')
            return
        soup = BeautifulSoup (r.text, 'html.parser')

        
        href_regex = re.compile ('Spanish_frequency.*000')
        find_esp_links = lambda t : (t.name == 'a' 
                and t.has_attr ('href')
            and href_regex.search (t['href']) is not None)
        tags = soup.find_all (find_esp_links)
        #  print (tags)

        df = pd.DataFrame (columns = ['word', 'freq'])

        for t in tags:

            if int(re.findall ('\d+', t['href'])[0]) > limit:
                break

            suburl = domain + t['href']
            print ('Wcodząc do {0}'.format (suburl))
            df = df.append (self.get_page_words (suburl), ignore_index=True)

        self.freqlist = df
        df.to_csv ('esp.dict', index=False)
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

def wget_pages (lim = 3, lang_dict = './esp.dict' ):
    """ Pobierz przez wget przez limit stron tłumaczeń z spanishdict
    """

    base_url = 'https://www.spanishdict.com/translate/'
    args = ['--no-clobber', '--page-requisites',
            '--html-extension', '--convert-links',
            '--no-parent']    
    dict_file = open (lang_dict, 'r')


    # pomiń pierwszy wiersz, bo zawiera tylko nazw kolumn
    dict_file.readline ()
    for c in range (lim):

        word = dict_file.readline ().split (',')[0]
        url = base_url + word
        cmd = ['wget'] + args + [url]

        # ściągamy
        print ("Pobierając z {}".format (url))
        subprocess.call (cmd)



