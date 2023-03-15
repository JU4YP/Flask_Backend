# Import libraries
import torch
from transformers import BertTokenizer, BertForQuestionAnswering

# Define the text and the questions
#text = "A total of 11 people lost their lives while returning to Madhya Pradesh after offering prayers at Ramdevra temple in Rajasthan when their jeep reportedly collided with another vehicle in Nagaur’s Shribalaji town on Tuesday morning at around 7.45 a.m. Eight people died on the spot while 3 others took their last breath on their way to Nokha hospital. The deceased were from Ujjain and Dewas districts of Madhya Pradesh. Police officials are investigating reasons of accident as the injured were unable to share details. Rajasthan Chief Minister Ashok Gehlot has expressed his condolences for the bereaved families. “It is heart wrenching to know that 11 people passed away in an accident. My condolences to the bereaved families. May God give them strength to bear the loss.”"
questions = ["How many casualties were there in the accident?", "Where did the accident happen?", "When did the accident happen?", "What type of vehicles were involved in the accident?","What are the names of the casualties?","What are some information about the casulaties?","What are some information about the accident location?"]

# Load the tokenizer and the model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

def extract(text):
# Loop through each question
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
        result[question]=answer
    return result