from webscraping import hotelinfoscraper
from flask import Flask, render_template, request,url_for,redirect
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import numpy as np

import pandas as pd
import seaborn as sns
from pylab import rcParams
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib import rc
from pandas.plotting import register_matplotlib_converters
from sklearn.model_selection import train_test_split
from os import path
from PIL import Image
import warnings
from textblob import TextBlob
import sys, tweepy
import re
import string 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score 
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import os

from twitterextract import twitterdata
from webscraping import hotelinfoscraper
from bargraph import barchartgenerator

# locationstopwords =set()
# locationdataset =pd.read_csv('us-city-place-names.csv')
# locationdataset = hoteldataset.drop(columns=['state_id'],inplace =True)
# for state_name in hoteldatas 

warnings.filterwarnings('ignore')

def convert_list_to_string(list1, seperator=' '):
    return seperator.join(list1)

# Cleaning the data by converting it into lowercase, removing brackets, numbers and punctuations
def cleandatafunction(text):
    text = text.lower()
    text = re.sub('\[.*?\]','',text)
    text = re.sub('[%s]'% re.escape(string.punctuation),'',text)
    text = re.sub('\w*\d\w*','',text)
    return text

# further cleaning the data
def cleandatafunction2(text):
    text = re.sub('[''""...]','',text)
    text = re.sub('\n','',text)
    return text

# def show_word_cloud(cloud, title):
#   plt.imshow(cloud, interpolation='bilinear')
#   plt.title(title)
#   plt.axis("off")
#   plt.show()

def clean(tweet):
    tweet = re.sub(r'^RT[\s]+', '', tweet)    #remove Retweets
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)  #remove links
    tweet = re.sub(r'#', '', tweet) #remove Hashtags
    tweet = re.sub(r'@[A-Za-z0–9]+', '', tweet)  #remove mentions
    tweet = tweet.lower() #lower case
    tweet = re.sub('\[.*?\]','',tweet)
    tweet = re.sub('[%s]'% re.escape(string.punctuation),'',tweet)
    tweet = re.sub('\w*\d\w*','',tweet)
    tweet = re.sub('[''""...]','',tweet)
    tweet = re.sub('\n','',tweet)
    return tweet

def read_tweets(file_name):
    with open(file_name, 'r') as f:
        tweets = [clean(line.strip()) for line in f]
    f.close()
    return tweets

def green_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return("hsl(113,40%%, %d%%)" % np.random.randint(49,51))

def red_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return("hsl(353, 82%%, %d%%)" % np.random.randint(49,51))
      
def wordcloudgenerate(text,hotel,title,c):
    filename ='wc_'+ hotel +' '+ title +'.png'
    path = os.path.abspath(os.curdir)+'/static/images/'+ filename
    stopwords = set(STOPWORDS)
    stopwords.add(hotel)
    stopwords.add('hotel')
    stopwords.add('Hotel')
    stopwords.add('HOTEL')
    stopwords.add('austin')
    stopwords.add('bhyatt')
    stopwords.add('hotels')
    stopwords.add('hotels')
    stopwords.add('hotels')
    stopwords.add('resort')
    stopwords.add('new york')
    stopwords.add('amp')
    stopwords.add('resorts')
    stopwords.add('bhost')
    
    stoplist =hotel.split()
    stoplist2=hotel.split('-')
    for r in stoplist:
        stopwords.add(r.upper())
        stopwords.add(r.lower()) 
    for r in stoplist2:
        stopwords.add(r.upper())
        stopwords.add(r.lower()) 
    # print(stopwords)
    custom_mask = np.array(Image.open('cloud.png') )
    wordcloud = WordCloud(background_color='white',stopwords=stopwords ,mask=custom_mask, max_font_size=150 ,max_words=1000,width=800,height=646)
    wordcloud.generate(text)
    if(c ==1):
        wordcloud.recolor(color_func=green_color_func)
    else:
        wordcloud.recolor(color_func=red_color_func)
    wordcloud.to_file(path)
    return filename

def calculatereviewscore():
    tweets = read_tweets('tweets.txt')
    asum = 0
    review_score = 0.0
    positweet =['']
    negatweet =['']
    reviewresult= model.predict(tweets)
    count=0
    for r in reviewresult:
    #     print(score*10)
        if r == 'good':
            asum = asum + 1
            positweet.append(tweets[count])
        else:
            negatweet.append(tweets[count])
        count=count +1
    print("total tweets analyzed:",len(tweets))
    print("positive tweets",asum)
    review_score =float(asum/len(tweets))*5
    print("Score",review_score)

    return (review_score,positweet,negatweet,asum)


    
import pickle

with open('model_pickle','rb') as f:
    model = pickle.load(f)

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', the_title='Home Page')

@app.route('/results.html', methods =['GET','POST'] )
def result():
    hotel = request.form['hotels']
    filename,tweetcount = twitterdata(hotel)
    
    score,posi,negi,posinum=calculatereviewscore()
    negisum =tweetcount-posinum
    positext = convert_list_to_string(posi,' ')
    negatext = convert_list_to_string(posi,' ')
    filename_posi= wordcloudgenerate(positext,hotel,'positive',1)
    print('positive wordcloud generated!')
    filename_nega= wordcloudgenerate(negatext,hotel,'negative',2)        
    print('negative wordcloud generated!')  
    score = round(score,1)
    description1, imagelinkf,hotelnameforresult,urlforhotel = hotelinfoscraper(hotel)
    print(description1)

    print("length",len(description1))
    print("imagelink:",imagelinkf)
    description1 = description1[:175] +'...'
    neginum =tweetcount-posinum
    bargraphimg = barchartgenerator(posinum,neginum,hotel)
    top5positive =posi[1:6]
    top5negative =negi[1:6]
    print(top5positive)
    print(top5negative)
    
    return render_template('results.html', top5pos=top5positive, top5neg = top5negative, f1=filename_posi, f2=filename_nega, positweet=posi,neitweet=negi, psum=posinum, nsum=negisum, search = hotel, file1=filename, rscore = score, tweet1=tweetcount, desc = description1, the_title='Results', imagel =imagelinkf,barimg=bargraphimg,hotelnamedesc=hotelnameforresult,url =urlforhotel )


@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html')

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)