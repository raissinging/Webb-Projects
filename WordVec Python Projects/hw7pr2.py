# coding: utf-8
# Jeffrey Z 

#
# hw7 problem 2
#

## Problem 2: Analogies!
#


#
# run with m = read_word2vec_model()  or model = ...
#
def read_word2vec_model():  
    """ a function that reads a word2vec model from the file
        "word2vec_model.txt" and returns a model object that
        we will usually name m or model...
    """
    file_name = "word2vec_model.txt"
    # these are the pre-2018 lines to load a model:
    # from gensim.models.word2vec import Word2Vec
    # m = Word2Vec.load_word2vec_format(file_name, binary=False)
    
    # here are the post-2018 lines to load a model:
    from gensim.models import KeyedVectors
    print("Starting to load the model in ", file_name, "...")
    m = KeyedVectors.load_word2vec_format(file_name, binary=False)
    print("Model loaded.\n")

    print("The model built is", m, "\n")
    print("m.vocab has", len(m.vocab), "words")
    ## The above line should print
    ## m.vocab has 43981 words

    print("Each word is a vector of size", m.vector_size)
    ## which should tells us that each word is represented by a 300-dimensional vector

    print("\nTry m.get_vector('hello') to see one...!\n")
    ##   Once the model is built, it can't be changed without rebuilding it; we'll leave it.  

    return m

m = read_word2vec_model()
# A helper function - are all words in the model?
#
def all_words_in_model( wordlist, model ):
    """ returns True if all w in wordlist are in model
        and False otherwise
    """
    for w in wordlist:
        if w not in model:
            return False
    return True


# Here's a demonstration of the fundamental capability of word2vec on which
#   you'll be building:  most_similar
#
def test_most_similar(model):
    """ example of most_similar """
    print("Testing most_similar on the king - man + woman example...")
    LoM = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=10)
    # note that topn will be 100 below in check_analogy...
    return LoM


#
#
# Start of functions to write + test...
#
#


#
# Write your generate_analogy function
# 
#   you will want to base this on the example call made in test_most_similar, above
# 
#
def generate_analogy(word1, word2, word3, model):
    """ generate_analogy's docstring - be sure to include it!
    """
    LoM = model.most_similar(positive=[word2, word3], negative=[word1], topn=100)
    return LoM


#
# Write your check_analogy function
#
def check_analogy(word1, word2, word3, word4, model):
    """ check_analogy's docstring - be sure to include it!
    """
    LoM = model.most_similar(positive=[word2, word3], negative=[word1], topn=100)
    LoWords = []
    for x in LoM:
        LoWords += [x[0]]
    if word4 not in LoWords:
        return 0
    else:
        score = 100
        for x in LoWords:
            if x != word4:
                score += -1
            else:
                return score 
    


#
# Results and commentary...
#

#
# (1) Write generate_analogy and try it out on several examples of your own
#     choosing (be sure that all of the words are in the model --
#     use the all_words_in_model function to help here)
#
# (2) Report two analogies that you create (other than the ones we looked at in class)
#     that _do_ work reaonably well and report on two that _don't_ work well
#     Finding ones that _do_ work well is more difficult! Maybe in 2025, it'll be the opposite (?)

'''
check_analogy('water', 'drink', 'food', 'eat', m)
96

check_analogy('car', 'drive', 'chair', 'sit', m)
90
'''

"""

check_analogy('keyboard', 'type', 'knife', 'cut', m)
0

check_analogy('people', 'food', 'car', 'gas', m)
0
"""



#
#
# (3) Write check_analogy that should return a "score" on how well word2vec_model
#     does at solving the analogy given (for word4)
#     + it should determine where word4 appears in the top 100 (use topn=100) most-similar words
#     + if it _doens't_ appear in the top-100, it should give a score of 0
#     + if it _does_ appear, it should give a score between 1 and 100: the distance from the
#       _far_ end of the list. Thus, a score of 100 means a perfect score. A score of 1 means that
#       word4 was the 100th in the list (index 99)
#     + Try it out:   check_analogy( "man", "king", "woman", "queen", m ) -> 100
#                     check_analogy( "woman", "man", "bicycle", "fish", m ) -> 0
#                     check_analogy( "woman", "man", "bicycle", "pedestrian", m ) -> 96


"""
got the same scores
"""


#
#
# (4) Create at least five analogies that perform at varying levels of "goodness" based on the
#     check_analogy scoring criterion -- share those (and any additional analysis) with us here!
#
#

"""
check_analogy( "baby", "cute", "spider", "scary", m ) - 0
check_analogy( "chef", "food", "mechanic", "car", m ) - 36
check_analogy('camera', 'photos', 'printer', 'paper', m) - 74
check_analogy( "tree", "leaf", "bicycle", "wheels", m )- 85
check_analogy( "dog", "puppy", "cat", "kitten", m ) - 100
""" 
