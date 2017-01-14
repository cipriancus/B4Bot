from flask import request
from flask import Flask, jsonify

from B4Bot import B4Bot
from emotion.alchemyapi import AlchemyAPI
import numpy as np

app = Flask(__name__)
alchemyapi = AlchemyAPI()

chatbot = B4Bot()

"""
    Request:
        {
            'statement':'Hello'
        }
    Response:
        {
            'response':'Hi there',
            'emotion': 'joy'
        }
"""
@app.route('/api/bot', methods=['POST'])
def get_response():
    print ('aici',request,  request.json, 'statement' in request.json )
    if not request.json or not 'statement' in request.json:
        print('aaaaaaaaaaaaaaaaaaaaaaa')
        return
        #abort(400)

    statement = request.json['statement']
    responseToStatement = chatbot.get_response(statement)
    joy = np.zeros(2)
    anger = np.zeros(2)
    sadness = np.zeros(2)
    disgust = np.zeros(2)
    fear = np.zeros(2)

    pos_count = 0;
    response = alchemyapi.emotion('text', statement)
    if response['status'] == 'OK':
        emotions = response['docEmotions']
        emotions[0]="joy"
        emotions[1]="anger"
        emotions[2]="sadness"
        emotions[3]="disgust"
        emotions[4]="fear"
        index = np.argmax([np.sum(joy), np.sum(anger), np.sum(sadness), np.sum(disgust), np.sum(fear)])

    responseTXT=responseToStatement.text
    jsonSend=jsonify({'response': responseTXT, 'emotion': emotions[index]})

    return jsonSend

if __name__ == '__main__':
    app.run(debug=True)

def getEmotion(text):
    joy = np.zeros(2)
    anger = np.zeros(2)
    sadness = np.zeros(2)
    disgust = np.zeros(2)
    fear = np.zeros(2)

    pos_count = 0;
    response = alchemyapi.emotion('text', text)
    if response['status'] == 'OK':
        emotions = response['docEmotions']
        joy[pos_count] = emotions["joy"]
        anger[pos_count] = emotions["anger"]
        sadness[pos_count] = emotions["sadness"]
        disgust[pos_count] = emotions["disgust"]
        fear[pos_count] = emotions["fear"]
        pos_count = (pos_count + 1) % 2
        index = np.argmax([np.sum(joy), np.sum(anger), np.sum(sadness), np.sum(disgust), np.sum(fear)])
        return index
    return None




