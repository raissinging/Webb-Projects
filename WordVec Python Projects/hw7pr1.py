# coding: utf-8

#
# Lab problem -- first, make sure everything's installed and working!
#

## Before you go any further, make sure that you can load these libraries...

import nltk
import textblob



#
# Then, from this week's problem 0 (http://nlp.stanford.edu/sentiment/index.html)
#
example_text = """
The underlying technology of this demo is based on a new type of 
Recursive Neural Network that builds on top of grammatical structures. 
You can also browse the Stanford Sentiment Treebank, the dataset on
which this model was trained. The model and dataset are described
in an upcoming EMNLP paper. Of course, no model is perfect. You can
help the model learn even more by labeling sentences we think would
help the model or those you try in the live demo.
"""

def textblob_examples(example_text=example_text):
    """ showing off the textblob and nltk libraries,
        first, to check if they work at all...
    """
    # tokenize with NLTK
    print("Here is the tokenized list-of-words from example_text:")
    LoW = nltk.word_tokenize(example_text.lower())
    print(LoW)
    print()

    print("And a list-of-sentences from example_text:")
    LoS = nltk.sent_tokenize(example_text.lower())
    print(LoS)
    print()

    # tokenize with textblob - first create a blob...
    blob = textblob.TextBlob( example_text )
    print("Tokenizing example with textblob:")
    print("Words:")
    print( blob.words )
    print("Sentences:")
    print( blob.sentences )


#
# Lab problem, Part 1:  Try the TextBlob QuickStart Tutorial for about 1/2 an hour
#
# here (actually, inside OR outside the above function), try out some examples from the 
# TextBlob QuickStart Tutorial, at https://textblob.readthedocs.io/en/dev/quickstart.html
#
# OR, feel free to do this at the Python prompt, instead!
#

# 
blob = textblob.TextBlob( example_text )
# print("blob.tags are", blob.tags)

# cool!

#
# What are those part-of-speech tags?  They are here:
#    http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# 



#
# Lab problem, Part 2:  Try Run with the wordvecs!
#

#
# Try this, for example, with 
#
#     m = read_word2vec_model()  # see function below
#     visualize_wordvecs(["breakfast", "lunch", "cereal", "dinner"], m)
#
def visualize_wordvecs(wordlist, model):
    """ example of finding an outlier with word2vec and graphically """
    # 
    # Are all of the works in the model?
    #

    for w in wordlist:
        if w not in model:
            print("Aargh - the model does not contain", w)
            print("Stopping...")
            return
    # 
    # First, find word2vec's outlier:
    #
    outlier = model.doesnt_match(wordlist)
    print("{0} is not like the others.".format(outlier))

    #
    # Next, we use PCA, Principal Components Analysis, to reduce dimensionality
    # and create a scatterplot of the words...
    #
    from sklearn.decomposition import PCA
    import matplotlib.pyplot as plt
    import numpy

    pca = PCA(n_components=2)   # 2 dimensions
    pca_model = pca.fit(model.syn0)  # all 43,981 words with 300 numbers each!

    LoM = [model[w] for w in wordlist]   # list of models for each word w
    word_vectors = numpy.vstack(LoM)     # vstack creates a vertical column from a list
    transformed_words = pca_model.transform(word_vectors)  # transform to our 2d space

    # scatterplot
    plt.scatter(transformed_words[:,0],transformed_words[:,1])
    
    # This is matplotlib's code for _annotating_ graphs (yay!)
    for i, word in enumerate(wordlist):
        plt.annotate(word, (transformed_words[i,0], transformed_words[i,1]), size='large')
        # it's possible to be more sophisticated, but this is ok for now

    plt.show()
    return


#
# Your tasks for the THIRD part of this hw6pr1 lab:
#
#   (1) Find two lists of four-or-more words (all in the model) where visualize_wordvecs
#       does a _good_ job of identifying an outlier - note them and the results here:
#
#   (2) Find two lists of four-or-more words (all in the model) where it's possible
#       to see that visualize_wordvecs has _missed_ the outlier (in some sense - you choose)
#       Note these and the results here:




#
#   (3) Include your four plots as screenshots or saved as images using matplotlib
#       please save them as outlier1.png outlier2.png outlier3.png and outlier4.png
#











#
# Now, setting up for problem 2  (also used a bit in this lab's part 2 and 3!)
#
# Try this function (and import statement it contains):
#

# Try this call   m = read_word2vec_model() 
#
## If the import statement fails, make sure that you have run 
## conda install gensim
## in your terminal.

# m = read_word2vec_model() 


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

# here's an example of "not matching" - used in the last part of lab
#
def doesnt_match_example(m):
    """ showing off doesnt_match """
    LoW = "breakfast cereal dinner lunch".split()
    print("Testing doesnt_match on the example with LoW =")
    print(LoW)
    nonmatcher = m.doesnt_match(LoW)
    return nonmatcher


# Here's a demonstration of the fundamental capability of word2vec on which
#   you'll be building:  most_similar
# 
# This is used in problem 2
#
def test_most_similar(m):
    """ example of most_similar """
    print("Testing most_similar on the king - man + woman example...")
    LoM = m.most_similar(positive=['woman', 'king'], negative=['man'], topn=10)
    # note that topn, above, is the number of words to return...
    return LoM


# outlier 1
#     m = read_word2vec_model()  # see function below
#     visualize_wordvecs(["computer", "phone", "book", "tablet"], m)
#     books is not like the others

# outlier 2 
#     visualize_wordvecs(["pig", "cow", "chicken", "beef"], m)  
#     beef is not like the others 

# outlier 3
#     visualize_wordvecs(["keyboard", "piano", "mouse", "monitor"], m)
#     was supposed to be piano but monitor was not like the others 

# outlier 4
#     visualize_wordvecs(["python", "rattle", "snake", "baby"], m)
#     was supposed to be baby but rattle was not like the others 
