import nltk
import pandas as pd
import pickle
import string
import copy
import re
from nltk.stem import WordNetLemmatizer


def bag_of_filtered_words(words):
    return {
        word: 1 for word in words
    }


file = open('skcategory.pickle', 'rb')
categorical_Classifier = pickle.load(file)
file.close()

file = open('vectorizer.pickle', 'rb')
vectorizer = pickle.load(file)
file.close()


def operation(username):
    file = open('App_Data/%s_tweets.pickle' % (username), 'rb')
    tweet = pickle.load(file)
    file.close()
    tokenized_tweets = []
    for t in tweet:
        tokenized_tweets.append(nltk.wordpunct_tokenize(t.lower()))
    length = copy.deepcopy(tokenized_tweets)
    if len(length) != 0:
        ''' for i in length:
             if i[0] == "@": #or i[0] == "@":
                 tokenized_tweets.remove(i)'''
        lemma = WordNetLemmatizer()
        lemmatized_tweets = []
        for t in tokenized_tweets:
            str = ""
            for k in t:
                str += lemma.lemmatize(k) + " "
            lemmatized_tweets.append(str)

        t = vectorizer.transform(lemmatized_tweets)
        result = categorical_Classifier.predict(t)
        ent, env, tech, spo, pol, ot = 0, 0, 0, 0, 0, 0
        for r in result:
            if r == 'ent':
                ent += 1
            if r == 'env':
                env += 1
            if r == 'pol':
                pol += 1
            if r == 'tech':
                tech += 1
            if r == 'spo':
                spo += 1
            if r == 'other':
                ot += 1

        ent = (ent / len(result) * 100)
        env = (env / len(result) * 100)
        pol = (pol / len(result) * 100)
        spo = (spo / len(result) * 100)
        tech = (tech / len(result) * 100)
        ot = (ot / len(result) * 100)
        return ent, env, pol, spo, tech, ot

    else:
        return 0, 0, 0, 0, 0, 0


def get_followings_classified(following):
    stripped = []
    for t in following:
        stripped.append(nltk.wordpunct_tokenize(t))

    temp = copy.deepcopy(stripped)

    pattern = re.compile(
        '^http|^:|^[\']|^["]|^[@]|^[\\]|^[/)(]|^x[a-z0-9]+|^[0-9]+|^[?]|^[.-[]]|^[#]|^[!]|^[\'@]|^[\"@]|^[,]|^[:]|^[;]')

    for i in range(0, len(temp)):
        for j in temp[i]:
            if pattern.match(j):
                stripped[i].remove(j)
            elif len(j) < 3:
                stripped[i].remove(j)

    lemma = WordNetLemmatizer()
    lemmatized_tweets = []
    for t in stripped:
        str = ""
        for k in t:
            str += lemma.lemmatize(k) + " "
        lemmatized_tweets.append(str)

    perfect_lemmatized = []
    for f in lemmatized_tweets:
        if len(f) > 0:
            perfect_lemmatized.append(f)

    t = vectorizer.transform(perfect_lemmatized)

    result = categorical_Classifier.predict(t)

    s, t, e, p = 0, 0, 0, 0
    for f in result:
        if f == 'spo':
            s += 1
        elif f == 'tech':
            t += 1
        elif f == 'pol':
            p += 1
        elif f == 'ent':
            e += 1
        elif f == 'other':
            e += 1
        elif f == 'env':
            p += 1

    total = s + p + t + e

    s = s / total * 100
    p = p / total * 100
    t = t / total * 100
    e = e / total * 100

    return s, p, t, e
