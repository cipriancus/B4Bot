import warnings
from storage.storage_adapter import StorageAdapter
from conversation.response import Response
from conversation.statement import Statement


class JsonFileStorageAdapter(StorageAdapter):
    """
    Permite stocarea conversatiilor cu userii in format JSON

    :keyword database: Path ul catre json ul in care se va stoca
    :type database: str

    :keyword read_only: True si nu se vor salva in BD
    :type read_only: bool
    """

    def __init__(self, **kwargs):
        super(JsonFileStorageAdapter, self).__init__(**kwargs)
        from jsondb import Database

        database_path = self.kwargs.get('database', 'database.db')
        self.database = Database(database_path)

        self.adapter_supports_queries = False

    def _keys(self):
        return list(self.database[0].keys())

    def count(self):
        return len(self._keys())

    def find(self, statement_text):
        values = self.database.data(key=statement_text)

        if not values:
            return None

        values['text'] = statement_text

        return self.json_to_object(values)

    def remove(self, statement_text):
        for statement in self.filter(in_response_to__contains=statement_text):
            statement.remove_response(statement_text)
            self.update(statement)

        self.database.delete(statement_text)

    def deserialize_responses(self, response_list):
        """
        Face conversia de la o lista de raspunsuri
        la o lista de obiecte Response
        """
        proxy_statement = Statement('')

        for response in response_list:
            data = response.copy()
            text = data['text']
            del data['text']

            proxy_statement.add_response(
                Response(text, **data)
            )

        return proxy_statement.in_response_to

    def json_to_object(self, statement_data):
        # copiem pt a nu modifica obiectul original
        statement_data = statement_data.copy()

        # Construim obiectul pentru lista de raspunsuri
        statement_data['in_response_to'] = self.deserialize_responses(
            statement_data['in_response_to']
        )

        # Stergem atrb text
        text = statement_data.pop('text')

        return Statement(text, **statement_data)

    def _all_kwargs_match_values(self, kwarguments, values):
        for kwarg in kwarguments:

            if '__' in kwarg:
                kwarg_parts = kwarg.split('__')

                key = kwarg_parts[0]
                identifier = kwarg_parts[1]

                if identifier == 'contains':
                    text_values = []
                    for val in values[key]:
                        text_values.append(val['text'])

                    if (kwarguments[kwarg] not in text_values) and (
                            kwarguments[kwarg] not in values[key]):
                        return False

            if kwarg in values:
                if values[kwarg] != kwarguments[kwarg]:
                    return False

        return True

    def filter(self, **kwargs):
        results = []

        for key in self._keys():
            values = self.database.data(key=key)

            # Adaugam atrb text
            values['text'] = key

            if self._all_kwargs_match_values(kwargs, values):

                results.append(self.json_to_object(values))

        return results

    def update(self, statement, **kwargs):
        # Nu se modifica bd decat dc e permis
        if not self.read_only:
            data = statement.serialize()

            del data['text']
            self.database.data(key=statement.text, value=data)

            # Se verifica dc exista o intrare pt fiecare raspuns
            for response_statement in statement.in_response_to:
                response = self.find(response_statement.text)
                if not response:
                    response = Statement(response_statement.text)
                    self.update(response)

        return statement

    def get_random(self):
        from random import choice

        if self.count() < 1:
            raise self.EmptyDatabaseException()

        statement = choice(self._keys())
        return self.find(statement)

    def drop(self):
        self.database.drop()
