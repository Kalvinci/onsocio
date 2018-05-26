import nltk
import pandas as pd
import pickle
import string
import copy
from nltk.stem import WordNetLemmatizer


def bag_of_filtered_words(words):
    return {
        word: 1 for word in words
    }


def operation(username):
    file = open('skpolarity.pickle', 'rb')
    Sentiment_Classifier = pickle.load(file)
    file.close()
    #test = pd.read_csv('App_Data/%s_tweets.csv' % (username))
    file = open('App_Data/%s_tweets.pickle' % (username),'rb')
    tweet = pickle.load(file)
    file.close()
    tokenized_tweets = []
    for t in tweet:
        tokenized_tweets.append(nltk.wordpunct_tokenize(t.lower()))
    if len(tokenized_tweets)!=0:
        '''length = copy.deepcopy(tokenized_tweets)
        for i in length:
            if i[0] == "@": #or i[1] == "\"@":
                tokenized_tweets.remove(i)'''

        lemma = WordNetLemmatizer()
        lemmatized_tweets = []
        for t in tokenized_tweets:
            str = ""
            for k in t:
                str += lemma.lemmatize(k)+" "
            lemmatized_tweets.append(str)
        file = open('pnvectorizer.pickle', 'rb')
        pnvectorizer = pickle.load(file)
        file.close()
        #print(lemmatized_tweets[1])
        t = pnvectorizer.transform(lemmatized_tweets)
        result = Sentiment_Classifier.predict(t)
        print(result)
        pos, neg, neut = 0, 0, 0
        for r in result:
            if r == '1':
                pos+=1
            elif r == '0':
                neg+=1
            elif r == 'n':
                neut += 1

        pos = (pos / len(result) * 100)
        neg = (neg / len(result) * 100)
        neut = (neut / len(result) * 100)
        print(pos)
        print(neg)
        return pos, neg, neut
    else:
        return 0,0,0