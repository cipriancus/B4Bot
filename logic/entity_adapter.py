from __future__ import unicode_literals
from datetime import datetime
from .logic_adapter import LogicAdapter


class EntityLogicAdapter(LogicAdapter):
    """
    Adaptor logic pentru entitati

    Ex: "Do you know something about Google?"
    """

    def __init__(self, **kwargs):
        super(EntityLogicAdapter, self).__init__(**kwargs)
        from nltk import NaiveBayesClassifier

        self.positive = [
            'what do you know about',
            'what is',
            'where is',
            'something about'
        ]

        self.negative = [
            'i am bored',
            'knowledge'
        ]

        labeled_data = (
            [(name, 0) for name in self.negative] +
            [(name, 1) for name in self.positive]
        )

        train_set = [(self.entity_question_features(n), text) for (n, text) in labeled_data]

        self.classifier = NaiveBayesClassifier.train(train_set)

    def entity_question_features(self, text):
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
        from model.utils import get_entity

        entity_features = self.entity_question_features(statement.text.lower())
        confidence = abs(self.classifier.classify(entity_features))

        list_of_entities=get_entity(statement.text)
        response=Statement('')

        if len(list_of_entities)==0:
            return 0.5,Statement('Sorry, I do not have any information about that')

        for iterator in list_of_entities:
            database = DatabaseClient()
            response_db=str()
            response_db=database.get_db_responce('something about: '+iterator)
            response.text=response.text+"\n\n"+response_db.text

        if len(response.text) <10:
            return 1,Statement("Sorry but I do not know anything yet")

        return 1, response