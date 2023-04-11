from flask import Flask, render_template, request
from keras.models import load_model
import tensorflow as tf
from fileinput import filename
import test
import os
import numpy as np
from PIL import Image
import json
from bson import json_util
from datetime import datetime,timedelta
import metadata

app = Flask(__name__)

from pymongo import MongoClient

cluster = MongoClient("mongodb://Rishi:HDST12345@ac-fhuqmjw-shard-00-00.cwz7qiq.mongodb.net:27017,ac-fhuqmjw-shard-00-01.cwz7qiq.mongodb.net:27017,ac-fhuqmjw-shard-00-02.cwz7qiq.mongodb.net:27017/?ssl=true&replicaSet=atlas-i0sq4k-shard-0&authSource=admin&retryWrites=true&w=majority")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = '/home/hrishikesh-ubuntu/Downloads/flask_app/images'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/fetchAll',methods=['GET'])
def getAllData():
    db = cluster["metadata"]
    collection = db["roadaccidents"]
    docs=list(collection.find({}))
    dateobj=datetime.strptime(docs[0]['date'],"%Y-%m-%dT%H:%M:%S")
    dateobj=dateobj-timedelta(days=1)
    print(dateobj.weekday())
    return {"result":json.dumps(docs, default=json_util.default)}

@app.route('/getRAPrediction', methods = ['GET'])
def home():
    data = request.json
    text = data['text']
    print(text)
    return {"result" : int(test.getRAPredictionFromTitle(text))}
    #return {"result" : str(text)}

@app.route('/getRAPredictionFromImage', methods = ['POST'])
def success():
    if request.method == 'POST':
        # f = request.files['file']
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        # img0 = Image.open(f)
        testing_ds = tf.keras.preprocessing.image_dataset_from_directory(
                        '/home/hrishikesh-ubuntu/Downloads/flask_app/images/test',
                        seed=42,
                        image_size=(250, 250),
                        batch_size=100)
        class_names = ['Accident', 'Non Accident']
        pred_labels = []
        # testing_ds.
        for images, labels in testing_ds.take(1):
            predictions = test.getRAPredictionFromImage(images)
            predlabel = []
            print(labels.numpy())
            print(predictions)
            for mem in predictions:
                predlabel.append(class_names[np.argmax(mem)])
                pred_labels.append(np.argmax(mem))
        print (np.array(pred_labels)) 
        # testing_ds = tf.keras.preprocessing.image_dataset_from_directory('/home/fist/Desktop/flask_app/images',
        # seed = 42,
        # image_size = (250, 250),
        # batch_size=100)
        # class_names = testing_ds.class_names
        # pred_labels = []
        # for images, labels in testing_ds.take(1):
        #     y_labels = labels
        #     predictions = test.getRAPredictionFromImage(images)
        #     predlabel = []
        #     for mem in predictions:
        #         predlabel.append(class_names[np.argmax(mem)])
        #         pred_labels.append(np.argmax(mem))
        
        return {"result" : "success"} 
    
@app.route('/getData',methods=['GET'])
def fetch():
    db = cluster["metadata"]
    collection = db["roadaccidents"]
    docs=collection.find({})
    for data in docs:
        print(data)
    return {"result":"success"}


@app.route('/getFilteredData',methods=['POST'])
def findData():
    db = cluster["metadata"]
    collection = db["roadaccidents"]
    date1=request.form.get("date1")
    date2=request.form.get("date2")
    state=request.form.get("state")
    city=request.form.get("city")
    print(date1,date2,state,city)
    datetime1=datetime.strptime(date1, "%Y-%m-%d")
    datetime2=datetime.strptime(date2, "%Y-%m-%d")
    data=list(collection.find({"metadata.state":state,"metadata.city":city,"metadata.date":{"$gte":datetime1,"$lte":datetime2}}))
    return {"result":json.dumps(data, default=json_util.default)}

@app.route('/extraction',methods=['POST'])
def extract():
    db = cluster["metadata"]
    collection = db["roadaccidents"]
    text=request.form.get("text")
    metadataExtracted=metadata.extract(text)
    return {"result":metadataExtracted}
    

@app.route("/year",methods=['GET'])
def  findYearWiseData():
    db = cluster["metadata"]
    collection = db["roadaccidents"]
    data=collection.aggregate([{"$group": {"_id":{"$year":"$metadata.date"},"count": {"$count": {}}}}])
    result=[]
    for x in data:
        result.append(x)
    return result