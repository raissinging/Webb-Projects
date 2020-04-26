## Jeffrey Z
# # Import all of the libraries and data that we will need.
import nltk
import textblob
from nltk.corpus import names  # see the note on installing corpora
from nltk.corpus import opinion_lexicon
from nltk.corpus import movie_reviews

import random
import math

from sklearn.feature_extraction import DictVectorizer
import sklearn
import sklearn.tree
from sklearn.metrics import confusion_matrix





#####################
#
## Problem 4: Movie Review Sentiment starter code...
#
#####################

# a boolean to turn on/off the movie-review-sentiment portion of the code...
RUN_MOVIEREVIEW_CLASSIFIER = True
if RUN_MOVIEREVIEW_CLASSIFIER == True:

    ## Read all of the opinion words in from the nltk corpus.
    #
    pos=list(opinion_lexicon.words('positive-words.txt'))
    neg=list(opinion_lexicon.words('negative-words.txt'))

    ## Store them as a set (it'll make our feature extractor faster).
    # 
    pos_set = set(pos)
    neg_set = set(neg)



    ## Read all of the fileids in from the nltk corpus and shuffle them.
    #
    pos_ids = [(fileid, "pos") for fileid in movie_reviews.fileids('pos')]
    neg_ids = [(fileid, "neg") for fileid in movie_reviews.fileids('neg')]
    labeled_fileids = pos_ids + neg_ids

    ## Here, we "seed" the random number generator with 0 so that we'll all 
    ## get the same split, which will make it easier to compare results.
    random.seed(0)   # we'll use the seed for reproduceability... 
    random.shuffle(labeled_fileids)



    ## Define the feature function
    #  Problem 4's central challenge is to modify this to improve your classifier's performance...
    #
    def opinion_features(fileid):
        """ starter feature engineering for movie reviews... """
        # many features are counts!
        positive_count=0
        negative_count=0
        exclaim_count=0
        for word in movie_reviews.words(fileid):
            if word in pos_set: 
                positive_count += 1
            if word in neg_set: 
                negative_count += 1
        #'''
        for word in movie_reviews.words(fileid):
            for x in range(len(word)):
                if word[x] == '!':
                    exclaim_count += 1
        asum = 0
        aword = 0
        for word in movie_reviews.words(fileid):
            asum += len(word)
            aword += 1
        avgwordlen = asum/aword 
        subjectivity = 0
        rawtext = movie_reviews.raw(fileid)
        blob = textblob.TextBlob(rawtext)
        for x in blob.sentences:
            subjectivity += x.sentiment.subjectivity
        #'''

        # Note:  movie_reviews.raw(fileid) is the whole review!
        # these next two lines will create
        # a TextBlob with all of the text from the review:
        rawtext = movie_reviews.raw(fileid)
        TB = textblob.TextBlob( rawtext )
        # from here, you can use TB.words and TB.sentences...

        # here is the dictionary of features...
        features = {}   # we could also use a default dictionary!
        
        features['positive'] = positive_count
        features['negative'] = negative_count
        #'''
        features['exclaimation mark'] = exclaim_count
        features['average word length'] = avgwordlen
        features['number of words'] = aword
        features['subjectivity'] = subjectivity
        #'''
        return features


    #
    ## Ideas for improving this!
    #
    # count both positive and negative words...
    # is the ABSOLUTE count what matters?
    # 
    # other ideas:
    #
    # feature ideas from the TextBlob library:
    #   * part-of-speech, average sentence length, sentiment score, subjectivity...
    # feature ideas from TextBlob or NLTK (or just Python):
    # average word length
    # number of parentheses in review
    # number of certain punctuation marks in review
    # number of words in review
    # words near or next-to positive or negative words: "not excellent" ?
    # uniqueness
    #
    # many others are possible...


    ## Extract features for all of the movie reviews
    # 
    print("Creating features for all reviews... ")
    features = [opinion_features(fileid) for (fileid, opinion) in labeled_fileids]
    labels = [opinion for (fileid, opinion) in labeled_fileids]
    fileids = [fileid for (fileid, opinion) in labeled_fileids]
    print(" ... feature-creation done.")


    ## Change the dictionary of features into an array
    #
    print("Transforming from dictionaries of features to vectors...", end="", flush=True)
    v = DictVectorizer(sparse=False)
    X = v.fit_transform(features)
    print(" ... vectors completed.", flush=True)

    ## Split the data into train, devtest, and test

    X_test = X[:100,:]
    Y_test = labels[:100]
    fileids_test = fileids[:100]

    X_devtest = X[100:200,:]
    Y_devtest = labels[100:200]
    fileids_devtest = fileids[100:200]

    X_train = X[200:,:]
    Y_train = labels[200:]
    fileids_train = fileids[200:]

    ## Train the decision tree classifier - perhaps try others or add parameters
    #
    dt = sklearn.tree.DecisionTreeClassifier(max_depth=3)
    dt.fit(X_train,Y_train)

    ## Evaluate on the devtest set; report the accuracy and also
    ## show the confusion matrix.
    #
    print("Score on devtest set: ", dt.score(X_devtest, Y_devtest))
    Y_guess = dt.predict(X_devtest)
    CM = confusion_matrix(Y_guess, Y_devtest)
    print("Confusion Matrix:\n", CM)

    ## Get a list of errors to examine more closely.
    #
    errors = []

    for i in range(len(fileids_devtest)):
        this_fileid = fileids_devtest[i]
        this_features = X_devtest[i:i+1,:]
        this_label = Y_devtest[i]
        guess = dt.predict(this_features)[0]
        if guess != this_label:
            errors.append((this_label, guess, this_fileid))

    PRINT_ERRORS = True 
    if PRINT_ERRORS == True:
        num_to_print = 16    # in my run, #16 is "Back to the Future II"
        count = 0

        for actual, predicted, fileid in errors:
            print("Actual: ", actual, "Predicted: ", predicted, "fileid:", fileid)
            count += 1
            if count > num_to_print: break

    PRINT_REVIEW = True
    if PRINT_REVIEW == True:
        print("   ~ Printing the review with fileid", fileid)
        text = movie_reviews.raw(fileid)
        print(text)

    ## Finally, score on the test set:
    print("+++++++++++++++++++++")
    print("Prediction score on the test set: ", dt.score(X_test, Y_test))
    print("+++++++++++++++++++++")


    # 
    # ## Reflections/Analysis
    #
    # Include a short summary of
    #   (a) how well your final set of features did!
    #   (b) what other features you tried and which ones seemed to 
    #       help the most/least
    #

'''

+++++++++++++++++++++
Prediction score on the test set:  0.64
+++++++++++++++++++++

features:positive words, negative words, number of exclaimation marks, average word length, number of words, and subjectivity for each sentence 

adding the negative words feature seemed to do most of the work
w/o negative words the Prediction score on the test set:  0.56

''' 


