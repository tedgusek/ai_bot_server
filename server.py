from flask import Flask, request, jsonify, session
from flask_cors import CORS
# from transformers import GPT2LMHeadModel, GPT2Tokenize
from dotenv import load_dotenv
import os
import torch
import secrets
import time
import random

#app instance
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

# Load Pretrained model and tokenizer
# model_name = 'gpt2'
# model = GPT2LMHeadModel.from_pretrained(model_name)
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)


def generate_response(prompt):
    # inputs = tokenizer.encode(prompt, return_tensors='pt')
    
    # input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']
    # print('input_ids : ', input_ids)
    # print('attention_mask : ', attention_mask)
    # print('inputs : ', inputs)

    # outputs = model.generate(inputs, max_length= 150, num_return_sequences=1)
    outputs = model.generate(inputs['input_ids'], max_length= 150, num_return_sequences=1)
    # print('outputs[0][0] : ', outputs[0][0])
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Create App Route /api/home
@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        'message': "Hello world!"
    })

@app.route("/botresponse",methods=['POST'])
def bot_response():
    # Get the JSON Payload from REQUEST
    request_data = request.get_json()

    # print(request_data)
    # extract the user message
    user_message = request_data.get('user_message')
    print('user_message : ', user_message)

    # Initialize session if its the first request
    if 'conversation' not in session:
        session['conversation'] = []

    # Add current user message
    session['conversation'].append({'user_message': user_message})

    # Logic to get the AI response
    bot_response = generate_response(user_message)
    # print(bot_response)
    # Add Bot Response to session
    session['conversation'].append({'bot_response': bot_response})
    
    # To simulate a response
    # time.sleep(random.randint(1,5))

    # bot_response = user_message 
    return jsonify({'bot_response': bot_response})

@app.route("/conversation", methods=['GET'])
def get_conversation():
    if 'conversation' in session:
        return jsonify(session['conversation'])
    else:
        return jsonify({'message': 'Non conversation history'})


if __name__ == "__main__":
    app.run(debug=True, port=8080)