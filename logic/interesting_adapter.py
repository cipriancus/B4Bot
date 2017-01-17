from __future__ import unicode_literals
from datetime import datetime
from .logic_adapter import LogicAdapter


class InterestingLogicAdapter(LogicAdapter):
    """
    Adaptor logic pentru lucruri interesante
    """

    def __init__(self, **kwargs):
        super(InterestingLogicAdapter, self).__init__(**kwargs)
        from nltk import NaiveBayesClassifier

        self.positive = [
            'i am bored',
            'tell me something interesting',
            'entertain me',
            'blow my mind'
        ]

        self.negative = [
            'you are interesting',
            'she was sad',
            'he was sad'
            'he was bored',
            'i am not bored',
            'he was not entertaining',
            'it was mindblowing',
            'tell me a joke',
        ]

        labeled_data = (
            [(name, 0) for name in self.negative] +
            [(name, 1) for name in self.positive]
        )

        train_set = [(self.interesting_question_features(n), text) for (n, text) in labeled_data]

        self.classifier = NaiveBayesClassifier.train(train_set)

    def interesting_question_features(self, text):
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

        interesting_features = self.interesting_question_features(statement.text.lower())
        confidence = abs(self.classifier.classify(interesting_features))

        database = DatabaseClient()

        if random.randint(0, 10) % 2 == 0:

            if random.randint(0, 10) % 2 == 0:
                response = database.get_db_responce('TELL ME A JOKE')
            else:
                response = database.get_db_responce('YO MAMA')

        else:
            response = database.get_db_responce('MATHS FACT')
            response.text = 'Math Fact : ' + response.text

        if confidence > 0.5:
            confidence = 0.6

        return confidence, response
