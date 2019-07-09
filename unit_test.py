#! /usr/bin/python3

import unittest
import eg_sample

class LanguageTest (unittest.TestCase):

    def test_SentenceProbability (self):
        
        lang = eg_sample.EmpiricalLanguageModel ()


        sentence1 = "los"
        losProb = lang.wordsDict[sentence1]
        sentence1Prob = lang.getSentencePrbability (sentence1)
        print (sentence1Prob)
         
        sentence2 = 'batallón batallón batallón batallón batallón batallón'
        batalionProb = lang.wordsDict['batallón']
        sentence2Prob = lang.getExampleProbabilities (sentence2)
        
        sentence3 = "El batallón tomó la posición enemiga por asalto durante la noche."
        sentence3Prob  = lang.getSentencePrbability (sentence3)

        self.assertEqual (lang.gamma, 0.1)
        self.assertEqual (sentence1Prob, losProb * lang.gamma * (1.0  - lang.gamma))
        self.assertEqual (sentence2Prob, batalionProb** 6 * lang.gamma * (1.0  - lang.gamma)** 6)
        #  self.assertEqual (sentence1Prob, )


if __name__ == '__main__':
    unittest.main ()
