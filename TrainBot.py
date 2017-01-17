from __future__ import print_function
from B4Bot import B4Bot

chatbot = B4Bot(trainer='storage.trainers.BotCorpusTrainer')

chatbot.train('corpus.data.english')
