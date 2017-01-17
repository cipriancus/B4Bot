from __future__ import unicode_literals
from datetime import datetime
from .logic_adapter import LogicAdapter


class JokeLogicAdapter(LogicAdapter):
    """
    Adaptor logic pentru glume
    """

    def __init__(self, **kwargs):
        super(JokeLogicAdapter, self).__init__(**kwargs)
        from nltk import NaiveBayesClassifier

        self.positive = [
            'tell me a joke',
            'a joke',
            'something funny'
        ]

        self.negative = [
            'stop joking around',
            'jokes on you',
            'you are a joker',
            'what is',
            'how are you',
            'hello',
            'do you have a question',
            'stop joking',
            'make fun of'
        ]

        labeled_data = (
            [(name, 0) for name in self.negative] +
            [(name, 1) for name in self.positive]
        )

        train_set = [(self.joke_question_features(n), text) for (n, text) in labeled_data]

        self.classifier = NaiveBayesClassifier.train(train_set)

    def joke_question_features(self, text):
        features = {}

        all_words = " ".join(self.positive + self.negative).split()

        for word in text.split():
            features['contains({})'.format(word)] = (word in all_words)

        for letter in 'abcdefghijklmnopqrstuvwxyz':
            features['count({})'.format(letter)] = text.lower().count(letter)
            features['has({})'.format(letter)] = (letter in text.lower())

        return features

    def process(self, statement):
        from conversation.statement import Statement
        from storage.database_client import DatabaseClient
        import random

        joke_features = self.joke_question_features(statement.text.lower())
        confidence = abs(self.classifier.classify(joke_features))

        if confidence > 0.5:
            confidence = 0.6

        database = DatabaseClient()

        if random.randint(0, 10) % 2 == 0:
            response = database.get_db_responce('TELL ME A JOKE')
        else:
            response = database.get_db_responce('YO MAMA')

        return confidence, response
