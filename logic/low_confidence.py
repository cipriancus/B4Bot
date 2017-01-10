from __future__ import unicode_literals
from conversation.statement import Statement
from .best_match import BestMatch


class LowConfidenceAdapter(BestMatch):
    '''
    Daca nu se stie un raspuns cu grad de incredere mare
    '''

    def __init__(self, **kwargs):
        super(LowConfidenceAdapter, self).__init__(**kwargs)

        self.confidence_threshold = kwargs.get('threshold', 0.65)
        self.default_response = kwargs.get(
            'default_response',
            "I'm sorry, I do not understand."
        )

    def process(self, input_statement):

        # Se ia cel mai bun match
        confidence, closest_match = self.get(input_statement)

        # Daca este sub valoarea minima ii dam un
        # raspuns cu valoarea de threshold mai mare si
        # acesta va raspunde
        if confidence < self.confidence_threshold:
            confidence = 1
        else:
            confidence = 0

        return confidence, Statement(self.default_response)
