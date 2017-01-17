import logging
from conversation.statement import Statement
from conversation.response import Response

class Trainer(object):
    """
    Base class for all other trainer classes.
    """

    def __init__(self, storage, **kwargs):
        self.storage = storage
        self.logger = logging.getLogger(__name__)

    def train(self, *args, **kwargs):
        """
        This class must be overridden by a class the inherits from 'Trainer'.
        """
        raise self.TrainerInitializationException()

    def get_or_create(self, statement_text):
        """
        Return a statement if it exists.
        Create and return the statement if it does not exist.
        """
        statement = self.storage.find(statement_text)

        if not statement:
            statement = Statement(statement_text)

        return statement

    class TrainerInitializationException(Exception):
        """
        Exception raised when a base class has not overridden
        the required methods on the Trainer base class.
        """

        def __init__(self, value=None):
            default = (
                'A training class must specified before calling train(). '
                )
            self.value = value or default

        def __str__(self):
            return repr(self.value)

    def _generate_export_data(self):
        result = []

        for statement in self.storage.filter():
            for response in statement.in_response_to:
                result.append([response.text, statement.text])

        return result

    def export_for_training(self, file_path='./export.json'):
        """
        Create a file from the database that can be used to
        train other chat bots.
        """
        from jsondb.db import Database
        database = Database(file_path)
        export = {'export': self._generate_export_data()}
        database.data(dictionary=export)


class ListTrainer(Trainer):
    """
    Allows a chat bot to be trained using a list of strings
    where the list represents a conversation.
    """

    def train(self, conversation):
        """
        Train the chat bot based on the provided list of
        statements that represents a single conversation.
        """
        statement_history = []

        for text in conversation:
            statement = self.get_or_create(text)

            if statement_history:
                statement.add_response(
                    Response(statement_history[-1].text)
                )

            statement_history.append(statement)
            self.storage.update(statement)


class BotCorpusTrainer(Trainer):
    """
    Allows the chat bot to be trained using data from the
    ChatterBot dialog corpus.
    """

    def __init__(self, storage, **kwargs):
        super(BotCorpusTrainer, self).__init__(storage, **kwargs)
        from corpus import Corpus

        self.corpus = Corpus()

    def train(self, *corpora):
        trainer = ListTrainer(self.storage)

        # Allow a list of coupora to be passed instead of arguments
        if len(corpora) == 1:
            if isinstance(corpora[0], list):
                corpora = corpora[0]

        for corpus in corpora:
            corpus_data = self.corpus.load_corpus(corpus)
            for data in corpus_data:
                for pair in data:
                    trainer.train(pair)

