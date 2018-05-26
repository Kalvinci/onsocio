from flask import Flask, render_template, request, redirect, url_for, make_response, sessions, session
import pandas as pd
import tweetCollector as tc
import sqlite3
import classify as cla
import pnclassify as pncla
import prac as ch
import sklearn
import os
from flask import Flask, render_template, request, redirect, url_for, make_response
import nltk
from nltk.corpus import stopwords
import pickle
app=Flask(__name__)
app.secret_key = "rahil"
notfound=0
@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")
@app.route("/signin",methods=["GET","POST"])
def signin():
    if request.method=='POST':
        user=request.form['username']
        passd=request.form['password']
        con=sqlite3.connect("onsocio.db")
        a=con.execute("SELECT * FROM HR WHERE USERNAME=? AND PASSWORD=?",(user,passd))
        if len(a.fetchall()) == 1:
            a=con.execute("SELECT * FROM HR WHERE USERNAME=? AND PASSWORD=?",(user,passd))
            for i in a:
                name=i[3]
                company=i[4]
                position=i[5]
                education=i[6]
                email=i[7]
                image=i[8]
            session['Logged_in']=True
            session.pop('Logged_in', None)
            resp = make_response(render_template("login.html", name=name, company=company, position=position ,education=education, email=email ,image=image))
            resp.set_cookie('name', name)
            resp.set_cookie('company', company)
            resp.set_cookie('position',position)
            resp.set_cookie('education', education)
            resp.set_cookie('email', email)
            resp.set_cookie('image', image)
            return resp
        else:
            notfound=1
            return render_template('index.html',notfound=notfound)

@app.route("/result",methods=["GET","POST"])
def result():
    username=request.form['twitterid']
    name=request.cookies.get('name')
    company = request.cookies.get('company')
    position = request.cookies.get('position')
    education = request.cookies.get('education')
    email = request.cookies.get('email')
    image = request.cookies.get('image')
    try:
        tc.get_all_tweets(username)
        file = open('App_Data/%s_tweets.pickle' % username, 'rb')
        tweet = pickle.load(file)
        file.close()
        print('tweet downloaded and opened')
        #face = tweet['text']
        res=cla.operation(username)
        print('category classification done')
        pnres=pncla.operation(username)
        print('pn classification done')
        extra=tc.get_followings(username)
        print('auxillary data retrieved')
        twittername=extra[0]
        location=extra[1]
        follower = ch.change(extra[3])
        following = ch.change(extra[2])
        totaltweets = ch.change(extra[4])
        followings_classified = extra[6]
        print(followings_classified)
        print('following classsification done')
        return render_template("result.html",pnres=pnres,res=res,extra=extra,twittername=twittername,location=location,follower=follower,following=following,totaltweets=totaltweets,tweet=tweet,username=username,name=name,company=company,position=position,education=education,email=email,image=image,followings_classified=followings_classified)
    except Exception as e:
        a=str(e)
        b="[{'code': 34, 'message': 'Sorry, that page does not exist.'}]"
        print(len(a))
        print(a)
        print(len(b))
        print(b)
        if a==b:
            print('in right location')
            error=1
            return render_template("login.html",error=error)
        else:
            print ('in hell')
    finally:
        os.remove('App_Data/%s_tweets.pickle' % username)
@app.route("/logout",methods=["GET","POST"])
def logout():

    return render_template("index.html")
if __name__=="__main__" :
    app.run(debug=True)
