from __future__ import unicode_literals
from adapters.adapters import Adapter


class InputAdapter(Adapter):
    """
    Clasa abstracta pentru input adapter
    """

    def process_input(self, *args, **kwargs):
        """
        Returneaza un statement bazandu se pe sursa de inout
        """
        raise self.AdapterMethodNotImplementedError()

    def process_input_statement(self, *args, **kwargs):
        """
        returneaza un statement deja existent
        """
        input_statement = self.process_input(*args, **kwargs)
        
        existing_statement = self.chatbot.storage.find(input_statement.text)

        if existing_statement:
            #exista statement ul
            input_statement = existing_statement

        return input_statement
