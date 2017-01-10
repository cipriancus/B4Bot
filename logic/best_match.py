from __future__ import unicode_literals
from .logic_adapter import LogicAdapter

class BestMatch(LogicAdapter):
    """
    Returneaza un raspuns bazandu se pe cel mai apropiat raspuns care face
    match pe input ul dat
    """

    def get(self, input_statement):
        """
        Primeste un string statement si o lista de stringuri statement
        si returneaza cel mai apropiat raspuns ce face match
        """
        statement_list = self.chatbot.storage.get_response_statements()

        if not statement_list:
            if self.chatbot.storage.count():
                #nu exista raspuns, alegem random
                return 0, self.chatbot.storage.get_random()
            else:
                raise self.EmptyDatasetException()

        closest_match = input_statement
        max_confidence = 0

        # Folosind functia de distanta din logic_adapter se compara
        # input ul cu un raspuns
        for statement in statement_list:
            confidence = self.compare_statements(input_statement, statement)

            if confidence > max_confidence:
                max_confidence = confidence
                closest_match = statement

        return max_confidence, closest_match

    def can_process(self, statement):
        return self.chatbot.storage.count()

    def process(self, input_statement):

        # Selecteaza cel mai bun raspuns folosind fct get,
        # ce compara un input cu un statement
        confidence, closest_match = self.get(input_statement)

        # salvam update uri facute de adaptor
        self.chatbot.storage.update(closest_match)

        # primim toate raspunsurile la match ul gasit
        response_list = self.chatbot.storage.filter(
            in_response_to__contains=closest_match.text
        )

        if response_list:
            #selectam raspunsul din cele mai optime raspunsuri
            response = self.select_response(input_statement, response_list)
        else:
            #selectam unul random
            response = self.chatbot.storage.get_random()

            # Set confidence to zero because a random response is selected
            confidence = 0

        return confidence, response
