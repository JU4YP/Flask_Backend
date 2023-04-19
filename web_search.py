# -*- coding: utf-8 -*-
from pprint import pprint
import requests
from datetime import datetime
import pymongo
import metadata
from tensorflow import keras


from newspaper import Article

# Modules required for Article
import nltk
nltk.download('punkt')

# Import spaCy
import spacy

# Load spaCy module for nlp
nlp = spacy.load('en_core_web_trf')



class SearchAPI:
	def __init__(self,search_query):
		self.myclient = pymongo.MongoClient("mongodb://Rishi:HDST12345@ac-fhuqmjw-shard-00-00.cwz7qiq.mongodb.net:27017,ac-fhuqmjw-shard-00-01.cwz7qiq.mongodb.net:27017,ac-fhuqmjw-shard-00-02.cwz7qiq.mongodb.net:27017/?ssl=true&replicaSet=atlas-i0sq4k-shard-0&authSource=admin&retryWrites=true&w=majority")
		self.query = search_query
		self.web_search_url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/WebSearchAPI"
		self.bing_search_url = "https://bing-news-search1.p.rapidapi.com/news/search"
		self.google_search_url = "https://google-news-api1.p.rapidapi.com/search"
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
		querystring = {"q":self.query,"language":"en"}

		headers = {
			"X-RapidAPI-Key": "2dc2de0e57msh9ae5a4dedc6f01bp1cbbbfjsnb19f2f806d00",
			"X-RapidAPI-Host": "google-news-api1.p.rapidapi.com"
		}

		response = requests.request("GET", self.google_search_url, headers=headers, params=querystring)
		print(response)
		return (response.json())

def Summarizer(url):
  # Get the news article from web using url
  # https://indianexpress.com/article/explained/in-mistry-crash-tragedy-a-reminder-of-high-numbers-of-road-deaths-in-the-country-8131214/
  # https://indianexpress.com/article/cities/mumbai/mumbai-7-injured-in-freak-car-accident-8165019/
  location_list = []
  try:
    new_accident = Article(url)

    # Do the necessary processings of a newspaper article (download, parse and apply nlp)
    new_accident.build()

    # Get different parameters from article
    # print(new_accident.text)


    doc = nlp(new_accident.text)

    # Get the list of locations mentioned here
    for word in doc.ents:
      if(word.label_ == 'GPE' or word.label_ == 'FAC' or word.label_ == 'LOC'):
        location_list.append(word.text)

    # Print location list4
  except:
      print("Error")
  return new_accident.text

def getKey(article,key):
  if (key in article.keys()):
    return article[key]
  else:
    return ""

def chngDateTimeFormat(dt_str: str):
    from_format = "%Y-%m-%dT%H:%M:%S"
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
  extract['body'] = Summarizer(extract['url'])
  extract['date'] = getKey(article,'datePublished')
  extract['language'] = getKey(article,'language')
  extract['metadata']=metadata.extract(extract['body'][:1000],extract['date'])
  extract['casualty']=metadata.extractFromTitle(extract['title'])
  if('image' in article.keys()):
    extract['image'] = getKey(article['image'],'url') 
  return extract

def extractBingArticle(article):
  extract={}
  extract['url'] = getKey(article,'url')
  extract['title'] = getKey(article,'name')
  extract['body'] = Summarizer(extract['url'])
  extract['date'] = getKey(article,'datePublished')
  if('image' in article.keys() and 'thumbnail' in article['image'].keys()):
    extract['image'] = getKey(article['image']['thumbnail'],'contentUrl')
  return extract

def extractGoogleArticle(article):
  extract={}
  extract['url'] = getKey(article,'link')
  extract['title'] = getKey(article,'title')
  extract['date'] = chngDateTimeFormat(getKey(article,'published'))
  extract['body']=Summarizer(extract['url'])
  extract['metadata']=metadata.extract(extract['body'][:500],extract['date'])
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

# article = sapi.GoogleNewsSearch()['news']['news'][0]

article = sapi.WebSearch()['value'][1]
extracted_article = extractArticle(article)
print(extracted_article["metadata"])

# pushToDB([extracted_article],sapi.myclient)

# pushToDB([extractArticle(article) for article in sapi.WebSearch()['value']], sapi.myclient)

# pushToDB([extractBingArticle(article) for article in sapi.BingSearch()['value']], sapi.myclient)

# pushToDB([extractGoogleArticle(article) for article in sapi.GoogleNewsSearch()['articles']], sapi.myclient)

# chngDateTimeFormat("2023-11-21T12:23:52.001Z")