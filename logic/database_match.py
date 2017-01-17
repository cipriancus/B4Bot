from __future__ import unicode_literals
from .logic_adapter import LogicAdapter
from storage.database_client import DatabaseClient

class DatabaseMatch(LogicAdapter):
    """
    Returneaza un raspuns din baza de date
    """

    def can_process(self, statement):
        return True

    def process(self, input_statement):

        database=DatabaseClient()

        response=database.get_db_responce(input_statement.text)

        confidence =self.compare_statements(input_statement, response)

        return confidence, response
