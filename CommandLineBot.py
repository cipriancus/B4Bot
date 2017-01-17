from __future__ import print_function
from B4Bot import B4Bot

chatbot = B4Bot()

while True:
    text = input("You: ")
    response = chatbot.get_response(text)
    print(response)
