from adapters.adapters import Adapter


class StorageAdapter(Adapter):
    """
    Clasa abstracta pentru Storage Adapter
    """

    def __init__(self, base_query=None, *args, **kwargs):

        super(StorageAdapter, self).__init__(**kwargs)

        self.kwargs = kwargs
        self.read_only = kwargs.get('read_only', False)
        self.adapter_supports_queries = True
        self.base_query = None

    def generate_base_query(self, bot, session_id):
        """
        Create a query
        """
        if self.adapter_supports_queries:
            for filter_instance in bot.filters:
                self.base_query = filter_instance.filter_selection(bot, session_id)

    def count(self):
        """
        Return nr de intrari din BD
        """
        raise self.AdapterMethodNotImplementedError()

    def find(self, statement_text):
        """
        Return un obiect din DB, dc exista
        """
        raise self.AdapterMethodNotImplementedError()

    def remove(self, statement_text):
        """
        Sterge un raspuns ce face match pe input
        """
        raise self.AdapterMethodNotImplementedError()

    def filter(self, **kwargs):
        """
        Return o lista de obiecte din BD
        kwargs contine un nr de atribute.
        Doar obiectele ce au toate atrib sunt returnate
        """
        raise self.AdapterMethodNotImplementedError()

    def update(self, statement):
        """
        Modifica entitatea in BD
        """
        raise self.AdapterMethodNotImplementedError()

    def get_random(self):
        """
        Returns random statement from BD
        """
        raise self.AdapterMethodNotImplementedError()

    def drop(self):
        """
        Sterge BD a unui adaptor
        """
        raise self.AdapterMethodNotImplementedError()

    def get_response_statements(self):
        """
        Intoarcere numai declaratii.
        O declaratie trebuie sa existe care sa fie cel mai apropiat match in campul
        In_response_to. In caz contrar, adaptorul logic poate gasi cel mai apropiata
         declaratie care sa nu aiba un raspuns cunoscut.

        """
        statement_list = self.filter()

        responses = set()
        to_remove = list()
        for statement in statement_list:
            for response in statement.in_response_to:
                responses.add(response.text)
        for statement in statement_list:
            if statement.text not in responses:
                to_remove.append(statement)

        for statement in to_remove:
            statement_list.remove(statement)

        return statement_list

    class EmptyDatabaseException(Exception):

        def __init__(self, value="Baza de date este goala"):
            self.value = value

        def __str__(self):
            return repr(self.value)
