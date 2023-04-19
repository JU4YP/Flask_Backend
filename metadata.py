# Import libraries
import torch
from transformers import BertTokenizer, BertForQuestionAnswering

import helper

# Define the text and the questions
#text = "A total of 11 people lost their lives while returning to Madhya Pradesh after offering prayers at Ramdevra temple in Rajasthan when their jeep reportedly collided with another vehicle in Nagaur’s Shribalaji town on Tuesday morning at around 7.45 a.m. Eight people died on the spot while 3 others took their last breath on their way to Nokha hospital. The deceased were from Ujjain and Dewas districts of Madhya Pradesh. Police officials are investigating reasons of accident as the injured were unable to share details. Rajasthan Chief Minister Ashok Gehlot has expressed his condolences for the bereaved families. “It is heart wrenching to know that 11 people passed away in an accident. My condolences to the bereaved families. May God give them strength to bear the loss.”"
questions = ["Which state did the accident happen?","Which city did the accident happen?","Which district did the accident happen?" , "What date did the accident happen?", "What type of vehicles were involved in the accident?","What are the names of the casualties?","What are some information about the casulaties?","What are some information about the accident location?"]
keys = ["state","city","district","date","vehicles","names","Info on casulaties","Info on location"]
# Load the tokenizer and the model
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

def extract(text,date):
# Loop through each question
    ind=0
    result={}
    for question in questions:
        # Tokenize the input
        input_ids = tokenizer.encode(question, text)
        tokens = tokenizer.convert_ids_to_tokens(input_ids)

        # Identify the segments (question and text)
        sep_index = input_ids.index(tokenizer.sep_token_id)
        num_seg_a = sep_index + 1
        num_seg_b = len(input_ids) - num_seg_a
        segment_ids = [0]*num_seg_a + [1]*num_seg_b

        # Run the model
        outputs = model(torch.tensor([input_ids]), # The tokens representing our input text.
                                    token_type_ids=torch.tensor([segment_ids])) # The segment IDs to differentiate question from text

        start_scores = outputs.start_logits
        end_scores = outputs.end_logits

        # Find the tokens with the highest start and end scores
        answer_start = torch.argmax(start_scores)
        answer_end = torch.argmax(end_scores)

        # Get the answer span
        answer = tokens[answer_start:answer_end+1]

        # Convert tokens back to string
        answer = tokenizer.convert_tokens_to_string(answer)

        # Print the question and the answer
        print(question)
        print(answer)
        if(keys[ind]=="date"):
            result[keys[ind]]=helper.getDate(answer,date)
        elif(keys[ind]=="names"):
            result[keys[ind]]=helper.person_names(answer)
        else:
            result[keys[ind]]=answer.lower()
        # result[question]=answer
        ind+=1
    return result

title_questions=["How many people died?","How many people are injured?"]
title_keys=["dead","injured"]
def extractFromTitle(text):
    result={}
    ind=0
    for question in title_questions:
        # Tokenize the input
        input_ids = tokenizer.encode(question, text)
        tokens = tokenizer.convert_ids_to_tokens(input_ids)

        # Identify the segments (question and text)
        sep_index = input_ids.index(tokenizer.sep_token_id)
        num_seg_a = sep_index + 1
        num_seg_b = len(input_ids) - num_seg_a
        segment_ids = [0]*num_seg_a + [1]*num_seg_b

        # Run the model
        outputs = model(torch.tensor([input_ids]), # The tokens representing our input text.
                                    token_type_ids=torch.tensor([segment_ids])) # The segment IDs to differentiate question from text

        start_scores = outputs.start_logits
        end_scores = outputs.end_logits

        # Find the tokens with the highest start and end scores
        answer_start = torch.argmax(start_scores)
        answer_end = torch.argmax(end_scores)

        # Get the answer span
        answer = tokens[answer_start:answer_end+1]

        # Convert tokens back to string
        answer = tokenizer.convert_tokens_to_string(answer)

        # Print the question and the answer
        print(question)
        print(answer)
        result[title_keys[ind]]=answer
        ind+=1

extractFromTitle("at least one person was killed and as many as 40 were inured")

