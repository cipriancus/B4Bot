from flask import request
from flask import Flask, jsonify

from B4Bot import B4Bot
from emotion.alchemyapi import AlchemyAPI
import numpy as np

app = Flask(__name__)
alchemyapi = AlchemyAPI()

chatbot = B4Bot()


@app.route('/api/bot', methods=['POST'])
def get_response():
    if not request.json or not 'statement' in request.json:
        return

    statement = request.json['statement']
    responseToStatement = chatbot.get_response(statement)

    response = alchemyapi.emotion('text', statement)
    if response['status'] == 'OK':
        emotions = response['docEmotions']
        maxim=0
        emotie=''
        for iterator in emotions.keys():
            if float(emotions[iterator])>maxim:
                maxim=float(emotions[iterator])
                emotie=iterator

    jsonSend=jsonify({'response': responseToStatement.text, 'emotion': emotie})

    return jsonSend

if __name__ == '__main__':
    app.run(debug=True)