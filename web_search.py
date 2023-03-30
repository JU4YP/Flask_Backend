# -*- coding: utf-8 -*-
from pprint import pprint
import requests
from datetime import datetime
import pymongo

from newspaper import Article

# Modules required for Article
import nltk
nltk.download('punkt')

# Import spaCy
import spacy
import spacy_transformers

# Load spaCy module for nlp
nlp = spacy.load('en_core_web_trf')

class SearchAPI:
	def __init__(self,search_query):
		self.myclient = pymongo.MongoClient("mongodb+srv://007Trishit:8Tu39xBo5OQZ0OsS@cluster0.cwz7qiq.mongodb.net/?retryWrites=true&w=majority")
		self.query = search_query
		self.web_search_url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/WebSearchAPI"
		self.bing_search_url = "https://bing-news-search1.p.rapidapi.com/news/search"
		self.google_search_url = "https://google-news.p.rapidapi.com/v1/search"
	def WebSearch(self):
		querystring = {"q":self.query,"pageNumber":"1","pageSize":"100","autoCorrect":"true"}
		headers = {
			"X-RapidAPI-Key": "65fe77868fmshbe3ee2d066d0354p1fc27ejsn668f405852c3",
			"X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
		}
		response = requests.request("GET", self.web_search_url, headers=headers, params=querystring)
		return response.json()
		
	def BingSearch(self):
		querystring = {"q":self.query,"textFormat":"Raw","safeSearch":"Off"}
		headers = {
			"X-BingApis-SDK": "true",
			"X-RapidAPI-Key": "65fe77868fmshbe3ee2d066d0354p1fc27ejsn668f405852c3",
			"X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com"
		}
		response = requests.request("GET", 	self.bing_search_url, headers=headers, params=querystring)
		return response.json()
	def GoogleNewsSearch(self):
		querystring = {"q":self.query,"lang":"en","country":"US"}

		headers = {
			"X-RapidAPI-Key": "65fe77868fmshbe3ee2d066d0354p1fc27ejsn668f405852c3",
			"X-RapidAPI-Host": "google-news.p.rapidapi.com"
		}

		response = requests.request("GET", self.google_search_url, headers=headers, params=querystring)
		return (response.json())

def Summarizer(url):
  # Get the news article from web using url
  # https://indianexpress.com/article/explained/in-mistry-crash-tragedy-a-reminder-of-high-numbers-of-road-deaths-in-the-country-8131214/
  # https://indianexpress.com/article/cities/mumbai/mumbai-7-injured-in-freak-car-accident-8165019/
  new_accident = Article(url)

  # Do the necessary processings of a newspaper article (download, parse and apply nlp)
  new_accident.build()

  # Get different parameters from article
  print('Report Date : ')
  # print(new_accident.meta_data['og']['publish_date'])
  print('\n\n----------\n\n')
  print('Report Summary : ')
  print(new_accident.summary)
  print(new_accident.keywords)


  doc = nlp(new_accident.text)

  # Get the list of locations mentioned here
  location_list = []
  for word in doc.ents:
    print(word.text+" -> "+word.label_)
    if(word.label_ == 'GPE' or word.label_ == 'FAC' or word.label_ == 'LOC'):
      location_list.append(word.text)

  # Print location list
  return location_list

def getKey(article,key):
  if (key in article.keys()):
    return article[key]
  else:
    return ""

def chngDateTimeFormat(dt_str: str):
    from_format = "%a, %d %b %Y %H:%M:%S %Z"
    dt = datetime.strptime(dt_str, from_format)
    to_format = "%Y-%m-%dT%H:%M:%S"
    return dt.strftime(to_format)

def pushToDB(json_list : list, myclient):

  mydb = myclient["metadata"]
  mycol = mydb["roadaccidents"]

  mycol.insert_many(json_list)

def extractArticle(article):
  extract={}
  extract['url'] = getKey(article,'url')
  extract['title'] = getKey(article,'title')
  extract['body'] = getKey(article,'body')
  extract['date'] = getKey(article,'datePublished')
  extract['location']=Summarizer(extract['url'])
  extract['language'] = getKey(article,'language')
  if('image' in article.keys()):
    extract['image'] = getKey(article['image'],'url') 
  return extract

def extractBingArticle(article):
    extract={}
    extract['url'] = getKey(article,'url')
    extract['title'] = getKey(article,'name')
    extract['body'] = getKey(article,'description')
    extract['date'] = getKey(article,'datePublished')
    extract['location']=Summarizer(extract['url'])
    if('image' in article.keys() and 'thumbnail' in article['image'].keys()):
      extract['image'] = getKey(article['image']['thumbnail'],'contentUrl')
    return extract

def extractGoogleArticle(article):
    extract={}
    extract['url'] = getKey(article,'link')
    extract['title'] = getKey(article,'title')
    extract['date'] = chngDateTimeFormat(getKey(article,'published'))
    extract['location']=Summarizer(extract['url'])
    return extract

sapi=SearchAPI('West Bengal road accident')

# for article in sapi.WebSearch()['value']:
#   extract = extractArticle(article)
#   print(extract)
#   #print()
  
# for article in sapi.BingSearch()['value']:
#   extract = extractBingArticle(article)
#   #print(extract)
#   #print()

# for article in sapi.GoogleNewsSearch()['articles']:
#     extract = extractGoogleArticle(article)
#     print(extract)
#     print()

pushToDB([extractArticle(article) for article in sapi.WebSearch()['value']], sapi.myclient)

pushToDB([extractBingArticle(article) for article in sapi.BingSearch()['value']], sapi.myclient)

pushToDB([extractGoogleArticle(article) for article in sapi.GoogleNewsSearch()['articles']], sapi.myclient)

