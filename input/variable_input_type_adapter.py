from __future__ import unicode_literals
from input.input_adapter import InputAdapter
from conversation.statement import Statement


class VariableInputTypeAdapter(InputAdapter):
    '''
    Face conversia din diferite tipuri de input la un obiest de tipul Statement
    '''

    JSON = 'json'
    TEXT = 'text'
    OBJECT = 'object'
    VALID_FORMATS = (JSON, TEXT, OBJECT, )

    def __init__(self, **kwargs):
        super(VariableInputTypeAdapter, self).__init__(**kwargs)

    def detect_type(self, statement):

        string_types = str

        if hasattr(statement, 'text'):
            return self.OBJECT
        if isinstance(statement, string_types):
            return self.TEXT
        if isinstance(statement, dict):
            return self.JSON

        input_type = type(statement)

        raise self.UnrecognizedInputFormatException(
            'Nu se cunoaste tipul, tipurile admise sunt Text, Obiect- Statement sau JSON.'.format(
                input_type
            )
        )

    def process_input(self, statement):
        input_type = self.detect_type(statement)

        if input_type == self.OBJECT:
            return statement

        if input_type == self.TEXT:
            return Statement(statement)

        if input_type == self.JSON:
            input_json = dict(statement)
            text = input_json["text"]
            del(input_json["text"])

            return Statement(text, **input_json)

    class UnrecognizedInputFormatException(Exception):
        def __init__(self, value='Formatul de input nu este cunoscut'):
            self.value = value

        def __str__(self):
            return repr(self.value)
