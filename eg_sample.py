#! /usr/bin/python3

import pandas as pd
from math import log, exp


class EmpiricalLanguageModel:

    def __init__ (self, exampleFile='./esp_eg.dict'):
        """ Incijalizuj to bydło """

        self.exampleFile = exampleFile
        self.getWordProbabilities (self.exampleFile)
        self.getWordProbabilities ()

        #  współczynnik hamowania zdania
        self.gamma = 0.1

    def wordsFrame (self):
        """ Zwróć dataframe ze słowami """
        return self.wordsFrame

    def stripSentence (self, s):
        """ Normalizuj zdanie, robiąc z niego listę pojawiających się w nim słów """
        tr = str.maketrans ('', '', '?¿!¡.,:;\"\'')
        return s.translate (tr) .lower () .strip () .split ()

    def getSentencePrbability (self, sentence):
        """ Zwróć prawdopodobieństwo losowego występowania zdanie s
        """

        words = stripSentence (sentence)
        wordsProb = map (lambda s : self.wordsDict [s], words)
        
        returnValue = 1.0
        for p in wordsProb:
            returnValue *= p

        return returnValue
        

    def getWordProbabilities (self, exampleFile = './esp_eg.dict'):
        """ Bierz przykłądy. Oblicz empiryczne prawdopodobienstwa. 
        Zwróć rezultat w postaci listy. 
        """

        egdf = pd.read_csv (exampleFile)
        egdf = egdf.iloc [:10]
        
        total_words = 0
        self.wordsDict = dict ()

        for s in egdf.iterrows ():
            l = self.stripSentence (s[1]['esp'])
            total_words += len (l)
            for w in l:
                if w in self.wordsDict.keys():
                    self.wordsDict[w] += 1
                else:
                    #  print ("New word found: {}".format (w))
                    self.wordsDict [w] = 1

        for k in self.wordsDict.keys ():
            self.wordsDict[k] = self.wordsDict [k] / total_words
        self.wordsDict = list (self.wordsDict.items ())
        self.wordsDict.sort (key = lambda p : p [1], reverse = True)

        self.wordsFrame = pd.DataFrame (self.wordsDict,
            columns = ['word', 'prob']
            )

        return self.wordsFrame

    def getExampleProbabilities (self, exampleFile = './esp_eg.dict'):
        """ Przypisz każdemu przykładowi prawdopodobieństwo """
        
        self.examplesData = pd.read_csv (self.exampleFile)

        self.examplesData['prob'] = self.examplesData['ang'].apply (
                self.getSentencePrbability
            )

        # skończ



def main ():
    lang = EmpiricalLanguageModel ()

if __name__ == '__main__':
    main ()
