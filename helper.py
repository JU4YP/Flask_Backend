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
def casualty_checker(str):
    dead=0
    arr=str.split(" ")
    casualty=[]
    for x in arr:
        if x.isdigit():
            casualty.append(int(x))
        else:
            y=x.lower()
            for i in range(0,len(units)):
                if y==units[i]:
                    casualty.append(int(i))
    if len(casualty)==1:
        casualty.append(0)
    return casualty
print(casualty_checker("five killed, 752 injured in punjab road accidents"))

def getDate(str,date_str):
    dateobj=datetime.strptime(date_str,"%Y-%m-%dT%H:%M:%S")
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

def persons(text):
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

# print(getDate("saturday","2023-03-29T14:52:30").date())
# print(persons("The occupants were returning from a wedding in Jharkhand's Dhanbad district to their home at Panagarh in West Bengal when a speeding truck rammed into the car in which they were travelling. Asansol (West Bengal): In a tragic road accident, two people were killed and several others were severely injured after a speeding truck rammed into their car following which the car lost control and hit a divider on the National Highway 2 at Kalla More in Asansol of West Bengal's Paschim Bardhaman district, police said on Tuesday.According to the police, the occupants were returning from a wedding in Jharkhand's Dhanbad district to their home at Panagarh in West Bengal when a speeding truck rammed into the car in which they were travelling after which all the occupants, including the driver of the car, suffered serious injuries. The car was severely damaged, the police said.The police rushed to the spot and admitted the injured to Asansol District Hospital. Two have been declared brought dead whereas the others are undergoing treatment. The deceased have been identified as Anil Pandey (65), the groom's father, and Santosh Biswakarma (45), the driver of the car. The bodies will be handed over to the family after the post-mortem."))