from datetime import datetime,timedelta
from newspaper import Article

import spacy

nlp = spacy.load('en_core_web_trf')

units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen","twenty"
]
weekdays = {
    "monday":0,
    "tuesday":1,
    "wednesday":2,
    "thursday":3,
    "friday":4,
    "saturday":5,
    "sunday":0
}


def getDate(str,date_str):
    dateobj=datetime.strptime(date_str,"%Y-%m-%dT%H:%M:%S")
    try:
      day_report=dateobj.weekday()
      arr=str.split(" ")
      day=-1
      for x in arr:
          x=x.lower()
          if x in weekdays:
              day=weekdays[x]
      sub=0
      if(day_report>=day):
          sub=day_report-day
      else:
          sub=day_report-day+7
      dateobj=dateobj-timedelta(days=sub)
      return dateobj
    except:
       return dateobj

def person_names(text):
  # Get the news article from web using url
  # https://indianexpress.com/article/explained/in-mistry-crash-tragedy-a-reminder-of-high-numbers-of-road-deaths-in-the-country-8131214/
  # https://indianexpress.com/article/cities/mumbai/mumbai-7-injured-in-freak-car-accident-8165019/
  persons = []
  try:

    doc = nlp(text)

    # Get the list of locations mentioned here
    for word in doc.ents:
    #   print(word.label_,word.text)
      if(word.label_ == 'PERSON'):
        persons.append(word.text)
    # Print location list4
  except:
      print("Error")
  return persons


def casualty_checker(text):
  # Get the news article from web using url
  numbers = []
  try:

    doc = nlp(text)

    # Get the list of locations mentioned here
    for word in doc.ents:
      if(word.label_ == 'CARDINAL'):
        numbers.append(word.text)
    # Print location list4
  except:
    print("Error")
  result=[]
  for n in numbers:
    if(n.isdigit()):
        result.append(int(n))
    else:
        result.append(text2int(n))
  if len(result) > 0:
    return result[0]
  else:
    return 0      

def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          return 0

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

print(text2int("one hundred twenty seven"))

# print(getDate("saturday","2023-03-29T14:52:30").date())
# print(casualty("as many as 40"))