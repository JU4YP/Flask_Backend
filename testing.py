import requests

url = "https://google-news-api1.p.rapidapi.com/search"

querystring = {"language":"en"}

headers = {
	"X-RapidAPI-Key": "2dc2de0e57msh9ae5a4dedc6f01bp1cbbbfjsnb19f2f806d00",
	"X-RapidAPI-Host": "google-news-api1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.json())