from __future__ import unicode_literals
from .logic_adapter import LogicAdapter


class NoKnowledgeAdapter(LogicAdapter):
    """
    Atunci cand nu exista un raspuns
    Se pune in lista de raspunsuri ca fiind primul
    """

    def process(self, statement):

        if self.chatbot.storage.count():
            return 0, statement

        return 1, statement
