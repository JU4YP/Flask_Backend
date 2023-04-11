import requests

url = "https://google-news-api1.p.rapidapi.com/search"

querystring = {"language":"en"}

headers = {
	"X-RapidAPI-Key": "2dc2de0e57msh9ae5a4dedc6f01bp1cbbbfjsnb19f2f806d00",
	"X-RapidAPI-Host": "google-news-api1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)




querystring = {"q":"West Bengal Road Accident","textFormat":"Raw","safeSearch":"Off"}
headers = {
	"X-BingApis-SDK": "true",
	"X-RapidAPI-Key": "65fe77868fmshbe3ee2d066d0354p1fc27ejsn668f405852c3",
	"X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com"
}
response = requests.request("GET", 	"https://bing-news-search1.p.rapidapi.com/news/search", headers=headers, params=querystring)

print(response.json())