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
        f = open(filename)
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
        a = self.normalizeDictionary(model1.words)
        b = self.normalizeDictionary(model2.words)
        L1 = self.compareDictionaries(self.words,a,b)
        
        c = self.normalizeDictionary(model1.wordlengths)
        d = self.normalizeDictionary(model2.wordlengths)
        L2 = self.compareDictionaries(self.wordlengths,c,d)

        e = self.normalizeDictionary(model1.sentencelengths)
        f = self.normalizeDictionary(model2.sentencelengths)
        L3 = self.compareDictionaries(self.sentencelengths,e,f)

        g = self.normalizeDictionary(model1.stems)
        h = self.normalizeDictionary(model2.stems)
        L4 = self.compareDictionaries(self.stems,g,h)



      

        print("{0:15} {1:<15} {2:<15}".format("name","vsTM1","vsTM2"))
        print("{0:15} {1:<15} {2:<15}".format("----","-----","-----"))
        print("{0:15} {1:<15.2f} {2:<15.2f}".format("words",L1[0],L1[1]))
        print("{0:15} {1:<15.2f} {2:<15.2f}".format("wordlengths",L2[0],L2[1]))
        print("{0:10} {1:<15.2f} {2:<15.2f}".format("sentencelengths",L3[0],L3[1]))
        print("{0:15} {1:<15.2f} {2:<15.2f}".format("stems",L4[0],L4[1]))

        model1wins = 0
        model2wins = 0

        if L1[0] > L1[1]:
            model1wins += 1
        else: 
            model2wins +=1

        if L2[0] > L2[1]:
            model1wins += 1
        else: 
            model2wins +=1		
        
        if L3[0] > L3[1]:
            model1wins += 1
        else: 
            model2wins +=1		
        
        if L4[0] > L4[1]:
            model1wins += 1
        else: 
            model2wins +=1


        """
        print("\nModel1 - ",model1.name, "wins on", model1wins," features")
        print("Model2 - ",model2.name, "wins on", model2wins," features")
        if model1wins > model2wins:
            print("\n +++++      Model1 -", model1.name, "is the better match!      +++++\n")
        else:
            print("\n +++++      Model2 -", model2.name, "is the better match!      +++++\n")
"""



#test


"""
TM1 = TextModel()
TM1.readTextFromFile("test.txt")
TM1.createAllDictionaries()  # provided in hw description
print(TM1)
"""





print(" +++++++++++ Model1 +++++++++++ ")
TM1 = TextModel()
TM1.readTextFromFile("train1.txt")
TM1.createAllDictionaries()  # provided in hw description
print(TM1)

print(" +++++++++++ Model1 +++++++++++ ")
TM2 = TextModel()
TM2.readTextFromFile("train2.txt")
TM2.createAllDictionaries()  # provided in hw description
print(TM2)


print(" +++++++++++ Unknown text +++++++++++ ")
TM_Unk = TextModel()
TM_Unk.readTextFromFile("unknown.txt")
TM_Unk.createAllDictionaries()  # provided in hw description
print(TM_Unk)

TM_Unk.compareTextWithTwoModels(TM1, TM2)


