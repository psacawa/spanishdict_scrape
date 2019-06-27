import pandas as pd

class Sentence:
    """ Reprezentacja zdania zwyodrębnionymi słowami"""

    def __init__ (s):
    self.sentence = s
    tr = str.maketrans ('', '', '?!.,:;')
    self.internal = s.translate (tr)
                     .lower ()
                     .strip ()
                     .split ()


def main ():


    freqdf = pd.read_csv ('./esp.dict')
    freqdf['empirical_freq'] = 0

    egdf = pd.read_csv ('./esp_eg.dict')
    
    # skończ
