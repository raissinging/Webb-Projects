# coding: utf-8
# textmodel.py
#
# TextModel project!
#
# Name: Jeffrey Zhong
#

from math import*
from string import*
from porter import create_stem

class TextModel(object):
    """A class supporting complex models of text."""

    def __init__(self):
        """Create an empty TextModel."""
        #
        # Create dictionaries for each characteristic
        #
        self.words = {}           # For counting words
        self.wordlengths = {}     # For counting word lengths
        self.stems = {}           # For counting stems
        self.sentencelengths = {} # For counting sentence lengths
        #
        # Create another of your own
        #
        self.gerund = {}     # For counting words with ing 
        self.text = ''

    def __repr__(self):
        """Display the contents of a TextModel."""
        s = 'Words:\n' + str(self.words) + '\n\n'
        s += 'Word lengths:\n' + str(self.wordlengths) + '\n\n'
        s += 'Stems:\n' + str(self.stems) + '\n\n'
        s += 'Sentence lengths:\n' + str(self.sentencelengths) + '\n\n'
        s += 'Gerunds:\n' + str(self.gerund)
        return s

    # Include other functions here.
    # In particular, you'll need functions that add to the model.

    def readTextFromFile(self, filename):
        """
        takes file and turns it into a str
        """
        f = open(filename, encoding = 'latin1')
        self.text = f.read()
        f.close()

    def makeSentenceLengths(self):
        """
        takes str from self.text and creats dict of sentence length freq.
        """
        count = 0
        LoW = self.text.split()
        list = []
        for x in range(len(LoW)): 
            if '.' in LoW[x] or '?' in LoW[x] or '!' in LoW[x] : 
                length = x
                list += [len(LoW[count: x+1])]
                count = length + 1
        for x in list:
            if x not in self.sentencelengths :
                self.sentencelengths[x] = 1
            else:
                self.sentencelengths[x] += 1
    
    def cleanString(self, s):
        """
        takes string s and remove all punctions and changes all caps to low
        """
        s = s.lower()
        for x in s: 
            if x in punctuation:
                s = s.replace(x, '')
        return s
    
    def makeWordLengths(self):
        """
        takes clean str from self.text and creats dict of word length freq.
        """
        clean_s = self.cleanString(self.text)
        LoW = clean_s.split() 
        for x in LoW: 
            if len(x) not in self.wordlengths: 
                self.wordlengths[len(x)] = 1
            else: 
                self.wordlengths[len(x)] += 1
        return self.wordlengths
    
    def makeWords(self): 
        """
        takes clean str from self.text and creats dict of word freq.
        """
        clean_s = self.cleanString(self.text)
        LoW = clean_s.split() 
        for x in LoW: 
            if x not in self.words: 
                self.words[x] = 1
            else: 
                self.words[x] += 1
        return self.words
    
    def makeStems(self):
        """
        takes clean str from self.text and creats dict of stem freq.
        """
        clean_s = self.cleanString(self.text)
        LoW = clean_s.split() 
        for x in LoW: 
            if create_stem(x) not in self.stems: 
                self.stems[create_stem(x)] = 1
            else: 
                self.stems[create_stem(x)] += 1
        return self.stems
    
    def makeGerund(self):
        """
        takes clean str from self.text and creats dict of gerund/present participle freq.
        """
        clean_s = self.cleanString(self.text)
        LoW = clean_s.split()
        for x in LoW: 
            if 'ing' in x and x not in self.gerund: 
                self.gerund[x] = 1
            elif 'ing' in x and x in self.gerund: 
                self.gerund[x] += 1
        return self.gerund
    
    def normalizeDictionary(self, d):
        """
        accept dictionary d and return a normalized version:
        one in which the values add up to 1.0
        """
        normalized = {}
        dimsum = sum(d.values())
        for x in d:
            normalized[x] = float(d[x])/float(dimsum)
        return normalized 
    
    def smallestValue(self, nd1, nd2): 
        """
        two  dictionaries nd1 and nd2 and  return the smallest positive value 
        """
        minnd1 = min(nd1.values())
        minnd2 = min(nd2.values())
        totalmin = min(minnd1,minnd2)
        return totalmin
    
    def compareDictionaries(self, d, nd1, nd2):
        """
        return log-probability that dictionary d came from the distribution of data in the normalized dictionary nd1 and nd2
        """ 
        normnd1 = self.normalizeDictionary(nd1)
        normnd2 = self.normalizeDictionary(nd2) 
        total_log_prob1 = 0.0
        total_log_prob2 = 0.0
        epsilon = self.smallestValue(normnd1,normnd2)/2
        for x in d:
            if x not in normnd1:
                total_log_prob1 += log(epsilon)
            else:
                total_log_prob1 += log(normnd1[x])*d[x]
        for x in d: 
            if x not in normnd2:
                total_log_prob2 += log(epsilon)
            else:
                total_log_prob2 += log(normnd2[x])*d[x]
        return [total_log_prob1, total_log_prob2]
    
    def createAllDictionaries(self):
        """
        creates all of the dictionaries from input string self.text
        """
        self.makeSentenceLengths()
        self.makeWords()
        self.makeStems()
        self.makeGerund()
        self.makeWordLengths()
    
    def compareTextWithTwoModels(self, model1, model2):
        """
        """
        print("Comparison: Model1; Model2")
        self.createAllDictionaries()
        model1.createAllDictionaries()
        model2.createAllDictionaries()
        m1score = 0
        m2score = 0

        dw = self.words; dw1 = model1.words; dw2 = model2.words 
        w1, w2 = self.compareDictionaries(dw, dw1, dw2)
        
        if w1 > w2:
            m1score += 1 
        elif w1 == w2: 
            m1score += 0
        elif w2 > w1:
            m2score += 1  
        print('words:', w1,w2)

        dsentlen = self.sentencelengths; dsentlen1 = model1.sentencelengths; dsentlen2 = model2.sentencelengths
        sentlen1, sentlen2 = self.compareDictionaries(dsentlen, dsentlen1, dsentlen2) 
        if sentlen1 > sentlen2:
            m1score += 1 
        elif sentlen1 == sentlen2: 
            m1score += 0
        elif sentlen2 > sentlen1:
            m2score += 1  
        print('sentence length:', sentlen1, sentlen2)

        dwlen = self.wordlengths; dwlen1 = model1.wordlengths; dwlen2 = model2.wordlengths
        wlen1 , wlen2 = self.compareDictionaries(dwlen, dwlen1, dwlen2)
        if wlen1 > wlen2:
            m1score += 1 
        elif wlen1 == wlen2: 
            m1score += 0
        elif wlen2 > wlen1:
            m2score += 1  
        print('word lengths:', wlen1, wlen2)

        ds = self.stems ; ds1 = model1.stems ; ds2 = model2.stems 
        s1, s2 = self.compareDictionaries(ds, ds1, ds2)
        if s1 > s2:
            m1score += 1 
        elif s1 == s2: 
            m1score += 0
        elif s2 > s1:
            m2score += 1  
        print('stems:',s1,s2)

        dg = self.gerund ; dg1 = model1.gerund ; dg2 = model2.gerund
        if dg == {} or dg1 == {} or dg2 == {}:
            print('gerunds cannot be compared')
        else: 
            g1 , g2 = self.compareDictionaries( dg, dg1, dg2)
            if g1 > g2:
                m1score += 1 
            elif g1 == g2: 
                m1score += 0
            elif g2 > g1:
                m2score += 1  
            print('gerunds:',g1,g2)
        print('Model1 wins on ', m1score, 'features')
        print('Model2 wins on ', m2score, 'features')
        if m1score > m2score: 
            print ("Model1 is the better match")
        elif m2score > m1score:
            print ("Model2 is the better match")
        else: 
            print ('Lolz they are the same')

        
#run

print('Shrek: beemovie vs the room')
TM1 = TextModel()
TM1.readTextFromFile("beemovie.txt")
TM2 = TextModel()
TM2.readTextFromFile("theroom.txt")
TM_Unk = TextModel()
TM_Unk.readTextFromFile("shrek.txt")
TM_Unk.compareTextWithTwoModels(TM1, TM2)
print('')
print('')
print('')
print('My own work: beemovie vs the room')
TM1 = TextModel()
TM1.readTextFromFile("beemovie.txt")
TM2 = TextModel()
TM2.readTextFromFile("theroom.txt")
TM_Unk = TextModel()
TM_Unk.readTextFromFile("jeffrey.txt")
TM_Unk.compareTextWithTwoModels(TM1, TM2)
print('')
print('')
print('')
print('My own work: beemovie vs my other own work')
TM1 = TextModel()
TM1.readTextFromFile("beemovie.txt")
TM2 = TextModel()
TM2.readTextFromFile("jeff2.txt")
TM_Unk = TextModel()
TM_Unk.readTextFromFile("jeffrey.txt")
TM_Unk.compareTextWithTwoModels(TM1, TM2)












