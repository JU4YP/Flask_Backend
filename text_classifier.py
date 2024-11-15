import tensorflow as tf
import pickle
from keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

import numpy as np

max_length = 200
padding_type = 'post'
trunc_type = 'post'

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

model = tf.keras.models.load_model('accidents_classifier.h5')

# image_model = load_model('Model.h5')

def getRAPredictionFromTitle(title):
    lst = []
    lst.append (title)
    vs = tokenizer.texts_to_sequences (lst)
    vp = pad_sequences (vs, maxlen = max_length, padding = padding_type, truncating = trunc_type)
    predicted_label_seq = np.argmax(model.predict(vp), axis = 1)
    return predicted_label_seq[0]


# def getRAPredictionFromImage (images):
#     predictions = image_model.predict(images)
#     return predictions
print (getRAPredictionFromTitle('13 killed in west bengal road accident'))
