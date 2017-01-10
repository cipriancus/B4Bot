import logging


class Adapter(object):
    """
    Superclasa Adapter
    """

    def __init__(self, **kwargs):
        self.bot = None

    def set_chatbot(self, chatbot):
        self.chatbot = chatbot

    class AdapterMethodNotImplementedError(NotImplementedError):

        def __init__(self, message=None):
            if not message:
                message = 'Metoda trebuie suprascrisa'
            self.message = message

        def __str__(self):
            return self.message
