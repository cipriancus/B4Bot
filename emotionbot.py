from __future__ import print_function
from B4Bot import B4Bot
from emotion.alchemyapi import AlchemyAPI
import numpy as np
import json
import time
import socket

chatbot = B4Bot()

alchemyapi = AlchemyAPI()

joy = np.zeros(2)
anger = np.zeros(2)
sadness = np.zeros(2)
disgust = np.zeros(2)
fear = np.zeros(2)

pos_count = 0;

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 8000))

while True:
    text = input("You: ")
    response = chatbot.get_response(text)
    print(response)
    s.send(text.encode("UTF-8"))
    data = s.recv(3000).decode("UTF-8")
    print(data)
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
        print(index)
    else:
        print('Error in concept tagging call: ', response['statusInfo'])

    response = alchemyapi.taxonomy('text', text)

    if response['status'] == 'OK':

        for category in response['taxonomy']:
            print(category['label'], ' : ', category['score'])
        print('')

    else:
        print('Error in taxonomy call: ', response['statusInfo'])

s.close()
