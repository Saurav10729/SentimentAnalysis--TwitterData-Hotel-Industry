from flask import Flask, render_template, request,url_for,redirect
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import numpy as np
# import tensorflow as tf
# from tensorflow import keras
import pandas as pd
import seaborn as sns
from pylab import rcParams
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib import rc
from pandas.plotting import register_matplotlib_converters
from sklearn.model_selection import train_test_split
# import tensorflow_hub as hub
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
from app import cleandatafunction,cleandatafunction2
import pickle

hoteldataset =pd.read_csv('hotel.csv')
dataset = hoteldataset
hoteldataset2 = hoteldataset
hoteldataset = hoteldataset.drop(columns=['Hotel_Address','Additional_Number_of_Scoring','Review_Date','Average_Score','Hotel_Name','Reviewer_Nationality','Review_Total_Negative_Word_Counts','Total_Number_of_Reviews','Review_Total_Positive_Word_Counts','Total_Number_of_Reviews_Reviewer_Has_Given','Tags','days_since_review','lat','lng'],inplace =True)
       
hoteldataset2["review"] = hoteldataset2["Negative_Review"] + hoteldataset2["Positive_Review"]

hoteldataset2["review_type"] = hoteldataset2["Reviewer_Score"].apply(
    lambda x: "bad" if x < 5 else("good" if x>7 else "neutral")
)

# hoteldataset2["review"]= hoteldataset2["review_type"].apply(
#     lambda x: hoteldataset2["Negative_Review"] if x== "bad" else (hoteldataset2["Positive_Review"] if x> )
# 
dataset = hoteldataset2[["review", "review_type"]]
good_reviews = dataset[dataset.review_type == "good"]
bad_reviews = dataset[dataset.review_type == "bad"]
    
   
RANDOM_SEED = 42

good_dataset = good_reviews.sample(n=len(bad_reviews), random_state=RANDOM_SEED)
bad_dataset = bad_reviews
    
review_dataset = good_dataset.append(bad_dataset).reset_index(drop=True)
    
cleandata1 = lambda x: cleandatafunction(x)
review_dataset['Cleaned_Review1'] =pd.DataFrame(review_dataset.review.apply(cleandata1))
cleandata2 = lambda x: cleandatafunction2(x)
review_dataset['Cleaned_Review2'] = pd.DataFrame(review_dataset['Cleaned_Review1'].apply(cleandata2))

    
    
Independent_var =review_dataset.Cleaned_Review2
Dependent_var =review_dataset.review_type
    
IV_train, IV_test, DV_train, DV_test = train_test_split(Independent_var, Dependent_var,random_state =5)
    
tvec = TfidfVectorizer()
clf = LogisticRegression(solver ='lbfgs')

model = Pipeline([('vectorizer',tvec),('classifier',clf)])
model.fit(IV_train,DV_train)
predictions = model.predict(IV_test)
confusion_matrix(predictions,DV_test)
accuracy_model= accuracy_score(predictions, DV_test)
print('!!!!!!!   training completed    !!!!!!!!!')

with open('model_pickle','wb') as f:
    pickle.dump(model,f)

print('Model saved')