# -*- coding: utf-8 -*-
from pprint import pprint
import requests
from datetime import datetime
import pymongo
import metadata
import traceback
from tensorflow import keras
import text_classifier
import helper


from newspaper import Article

# Modules required for Article
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("punkt")

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
		self.newscatcher_search_url = "https://newscatcher.p.rapidapi.com/v1/search_enterprise"
		self.news_search_url = "https://newsapi.org/v2/everything"
	def WebSearch(self,pg_no):
		querystring = {"q":self.query,"pageNumber":pg_no,"pageSize":"100","autoCorrect":"true"}
		headers = {
			"X-RapidAPI-Key": "65fe77868fmshbe3ee2d066d0354p1fc27ejsn668f405852c3",
			"X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
		}
		response = requests.request("GET", self.web_search_url, headers=headers, params=querystring)
		return response.json()
		
	def setup(self):
		mydb = self.myclient["metadata"]
		mycol = mydb["roadaccidents"]
		mycol.create_index('news_id',unique=True)
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
	def NewsCatcherSearch(self):
		querystring = {"q":self.query,"lang":"en","sort_by":"relevancy","page":"1","media":"True","from":"2023-04-25","to":"2023-05-01"}
		headers = {
			"content-type": "application/octet-stream",
			"X-RapidAPI-Key": "2dc2de0e57msh9ae5a4dedc6f01bp1cbbbfjsnb19f2f806d00",
			"X-RapidAPI-Host": "newscatcher.p.rapidapi.com"
		}
		response = requests.get(self.newscatcher_search_url, headers=headers, params=querystring)
		return response.json()
	def NewsAPISearch(self):
		url = "https://newsapi.org/v2/everything"
		querystring = {"q":self.query,"sort_by":"publishedAt","apiKey":"5f4eca6ce8414e4da7339556b2194d5b"}
		response = requests.get(self.news_search_url, params=querystring)
		return response.json()



def Summarizer(url,body):
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
  except Exception:
    traceback.print_exc()
    print("ERROR: Article cannot be processed by Spacy.")
  if(len(new_accident.text)==0):
      return body
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

def chngDateTimeFormat2(dt_str: str):
    from_format = "%Y-%m-%d %H:%M:%S"
    dt = datetime.strptime(dt_str, from_format)
    to_format = "%Y-%m-%dT%H:%M:%S"
    return dt.strftime(to_format)

def pushToDBMany(json_list : list, myclient):

  mydb = myclient["metadata"]
  mycol = mydb["roadaccidents2"]
  mycol.insert_many(json_list)

def pushToDBOne(data , myclient):
  mydb = myclient["metadata"]
  mycol = mydb["roadaccidents2"]
  mycol.insert_one(data)

def extractArticle(article):
  extract={}
  extract['news_id']="A"+getKey(article,"id")
  extract['url'] = getKey(article,'url')
  extract['title'] = getKey(article,'title')
  extract['body'] = Summarizer(extract['url'],getKey(article,'body'))
  extract['date'] = getKey(article,'datePublished')
  extract['language'] = getKey(article,'language')
#   extract['metadata']=metadata.extract(extract['body'][:1000],extract['date'])
  extract['casualty']=metadata.extractFromTitle(extract['title'])
#   extract['geolocation']=helper.getLatLong(extract['metadata']['city']+','+extract['metadata']['state'])
  if('image' in article.keys()):
    extract['image'] = getKey(article['image'],'url') 
  return extract

def extractBingArticle(article):
	extract={}
	extract['news_id']="B"+getKey(article,"id")
	extract['url'] = getKey(article,'url')
	extract['title'] = getKey(article,'name')
	extract['body'] = Summarizer(extract['url'],getKey(article,'body'))
	extract['date'] = getKey(article,'datePublished')
	#   extract['metadata']=metadata.extract(extract['body'][:1000],extract['date'][:19])
	extract['casualty']=metadata.extractFromTitle(extract['title'])
	#   extract['geolocation']=helper.getLatLong(extract['metadata']['city']+','+extract['metadata']['state'])
	if('image' in article.keys() and 'thumbnail' in article['image'].keys()):
		extract['image'] = getKey(article['image']['thumbnail'],'contentUrl')
	return extract
def extractNewsAPIArticle(article):
	extract={}
	extract['url'] = getKey(article,'url')
	extract['title'] = getKey(article,'title')
	extract['body'] = Summarizer(extract['url'],getKey(article,'description'))
	extract['date'] = getKey(article,'publishedAt')
	#   extract['metadata']=metadata.extract(extract['body'][:1000],extract['date'][:19])
	extract['casualty']=metadata.extractFromTitle(extract['title'])
	#   extract['geolocation']=helper.getLatLong(extract['metadata']['city']+','+extract['metadata']['state'])
	if('urlToImage' in article.keys()):
		extract['image'] = getKey(article,'urlToImage')
	return extract

def extractGoogleArticle(article):
	extract={}
	extract['url'] = getKey(article,'link')
	extract['title'] = getKey(article,'title')
	extract['date'] = chngDateTimeFormat(getKey(article,'published'))
	extract['body']=Summarizer(extract['url'],getKey(article,'body'))
	extract['metadata']=metadata.extract(extract['body'][:500],extract['date'])
	return extract

def extractNewsCatcherArticle(article):
	extract={}
	extract['news_id']="E"+getKey(article,"_id")
	extract['url'] = getKey(article,'link')
	extract['title'] = getKey(article,'title')
	extract['body'] = Summarizer(extract['url'],getKey(article,'summary'))
	extract['date'] = chngDateTimeFormat2(getKey(article,'published_date'))
	extract['metadata']=metadata.extract(extract['body'][:1000],extract['date'][:19])
	extract['casualty']=metadata.extractFromTitle(extract['title'])
	extract['geolocation']=helper.getLatLong(extract['metadata']['city']+','+extract['metadata']['state'])
	return extract


sapi=SearchAPI('Road Accident in India')
sapi.setup()

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

# article = sapi.WebSearch()['value'][5]
# extracted_article = extractArticle(article)
# pushToDB([extracted_article],sapi.myclient)

# article = sapi.BingSearch()['value'][0]
# print(article)
# extracted_article = extractBingArticle(article)
# pushToDB([extracted_article],sapi.myclient)

# pushToDB([extractArticle(article) for article in sapi.WebSearch()['value']], sapi.myclient)


# for ind in range(1):
# 	for article in sapi.WebSearch(ind+1)['value']:
# 		extracted_article=extractArticle(article)
# 		flag=text_classifier.getRAPredictionFromTitle(extracted_article['title'])
# 		if(flag==2):
# 			try:
# 				pushToDBOne(extracted_article,sapi.myclient)
# 			except Exception:
# 				traceback.print_exc()
# 			break

# for article in sapi.BingSearch()['value']:
# 	extracted_article=extractBingArticle(article)
# 	flag=text_classifier.getRAPredictionFromTitle(extracted_article['title'])
# 	if(flag==2):
# 		print(article)
# 		try:
# 			pushToDBOne(extracted_article,sapi.myclient)
# 		except Exception:
# 			traceback.print_exc()

# for article in sapi.NewsAPISearch()['articles']:
# 	extracted_article=extractNewsAPIArticle(article)
# 	flag=text_classifier.getRAPredictionFromTitle(extracted_article['title'])
# 	if(flag==2):
# 		print(article)
# 		try:
# 			pushToDBOne(extracted_article,sapi.myclient)
# 		except Exception:
# 			traceback.print_exc()
# 		break

for article in sapi.NewsCatcherSearch()['articles']:
	flag=text_classifier.getRAPredictionFromTitle(article['title'])
	if(flag==2):
		extracted_article=extractNewsCatcherArticle(article)
		try:
			pushToDBOne(extracted_article,sapi.myclient)
		except Exception:
			traceback.print_exc()
		break




# pushToDB([extractBingArticle(article) for article in sapi.BingSearch()['value']], sapi.myclient)

# pushToDB([extractGoogleArticle(article) for article in sapi.GoogleNewsSearch()['articles']], sapi.myclient)

# chngDateTimeFormat("2023-11-21T12:23:52.001Z")