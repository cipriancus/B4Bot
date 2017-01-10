from __future__ import unicode_literals
from adapters.adapters import Adapter
from model.utils import import_module


class LogicAdapter(Adapter):

    def __init__(self, **kwargs):
        super(LogicAdapter, self).__init__(**kwargs)
        from model.comparisons import levenshtein_distance
        from model.response_selection import get_first_response


        if 'statement_comparison_function' in kwargs:
            import_path = kwargs.get('statement_comparison_function')
            if isinstance(import_path, str):
                kwargs['statement_comparison_function'] = import_module(import_path)

        if 'response_selection_method' in kwargs:
            import_path = kwargs.get('response_selection_method')
            if isinstance(import_path, str):
                kwargs['response_selection_method'] = import_module(import_path)

        self.compare_statements = kwargs.get(
            'statement_comparison_function',
            levenshtein_distance
        )

        self.select_response = kwargs.get(
            'response_selection_method',
            get_first_response
        )

    def can_process(self, statement):
        return True

    def process(self, statement):
        """
        Metoda pentru a selecta un raspuns pentru un statement primit

        O valoare de incredere si declaratia de raspuns selectata trebuie să fie returnata
        Valoarea de incredere este un raiting asupra acuratetii raspunsului, data de adaptop
        Valoarea trb sa fie intre 0 si 1

        Aceasta valoare este folosita de alti adaptori pt a selecta raspunsul

        :param statement: Un statement
        :type statement: Statement

        :rtype: float, Statement
        """
        raise self.AdapterMethodNotImplementedError()

    class EmptyDatasetException(Exception):

        def __init__(self, value='Un statement vid a fost primit'):
            self.value = value

        def __str__(self):
            return repr(self.value)
