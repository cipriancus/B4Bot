from __future__ import unicode_literals
from storage.storage_adapter import StorageAdapter
from input.input_adapter import InputAdapter
from model import utils


class B4Bot(object):

    def __init__(self, name, **kwargs):
        from conversation.session import SessionManager
        from logic.multi_adapter import MultiLogicAdapter

        self.name = name
        kwargs['name'] = name

        storage_adapter = kwargs.get('storage_adapter', 'storage.jsonfile.JsonFileStorageAdapter')

        logic_adapters = kwargs.get('logic_adapters', ['logic.best_match.BestMatch',
                                    'logic.mathematical_evaluation.MathematicalEvaluation',
                                    'logic.time_adapter.TimeLogicAdapter',
                                    'logic.low_confidence.LowConfidenceAdapter'])

        input_adapter = kwargs.get('input_adapter', 'input.variable_input_type_adapter.VariableInputTypeAdapter')

        # Verificam adaptorii daca au impelentat interfetele corespunzatoare
        utils.validate_adapter_class(storage_adapter, StorageAdapter)
        utils.validate_adapter_class(input_adapter, InputAdapter)

        #da raspunsul efectiv, folosind mai multe adaptoare
        self.logic = MultiLogicAdapter(**kwargs)

        self.storage = utils.initialize_class(storage_adapter, **kwargs)


        self.input = utils.initialize_class(input_adapter, **kwargs)

        filters = kwargs.get('filters', tuple())
        self.filters = (utils.import_module(F)() for F in filters)

        # Setam un adaptor defaul in MultiLogicAdapter
        self.logic.system_adapters.append(utils.initialize_class('logic.no_knowledge_adapter.NoKnowledgeAdapter', **kwargs))

        #adaugam adaptoarele pentru raspunsurile noastre
        #in MultiLogicAdapter
        for adapter in logic_adapters:
            self.logic.add_adapter(adapter, **kwargs)

        # le dam adaptoarelor instanta de robot
        self.storage.set_chatbot(self)
        self.logic.set_chatbot(self)
        self.input.set_chatbot(self)



        # Use specified trainer or fall back to the default
        trainer = kwargs.get('trainer', 'trainer.trainers.Trainer')
        TrainerClass = utils.import_module(trainer)
        self.trainer = TrainerClass(self.storage, **kwargs)
        self.training_data = kwargs.get('training_data')



        self.conversation_sessions = SessionManager()
        self.default_session = self.conversation_sessions.new()

        if kwargs.get('initialize', True):
            self.initialize()

    def initialize(self):
        from model.utils import nltk_download_corpus

        # downloadam ce ne trebuie pentru nltk
        nltk_download_corpus('stopwords')
        nltk_download_corpus('wordnet')
        nltk_download_corpus('punkt')
        nltk_download_corpus('vader_lexicon')

    def get_response(self, input_item, session_id=None):
        """
        Return the bot's response based on the input.

        :param input_item: An input value.
        :returns: A response to the input.
        :rtype: Statement
        """
        if not session_id:
            session_id = str(self.default_session.uuid)

        input_statement = self.input.process_input_statement(input_item)

        statement, response, confidence = self.generate_response(input_statement, session_id)

        # Learn that the user's input was a valid response to the chat bot's previous output
        previous_statement = self.conversation_sessions.get(
            session_id
        ).conversation.get_last_response_statement()
        self.learn_response(statement, previous_statement)

        self.conversation_sessions.update(session_id, (statement, response, ))

        return response

    def generate_response(self, input_statement, session_id=None):
        """
        Return a response based on a given input statement.
        """
        if not session_id:
            session = self.conversation_sessions.get_default()
            session_id = str(session.uuid)

        self.storage.generate_base_query(self, session_id)

        # Select a response to the input statement
        confidence, response = self.logic.process(input_statement)

        return input_statement, response, confidence

    def learn_response(self, statement, previous_statement):
        """
        Learn that the statement provided is a valid response.
        """
        from conversation.response import Response

        if previous_statement:
            statement.add_response(
                Response(previous_statement.text)
            )

        # Update the database after selecting a response
        self.storage.update(statement)

    def set_trainer(self, training_class, **kwargs):
        """
        Set the module used to train the chatbot.

        :param training_class: The training class to use for the chat bot.
        :type training_class: chatterbot.trainers.Trainer

        :param \**kwargs: Any parameters that should be passed to the training class.
        """
        self.trainer = training_class(self.storage, **kwargs)

    @property
    def train(self):
        """
        Proxy method to the chat bot's trainer class.
        """
        return self.trainer.train

    @classmethod
    def from_config(cls, config_file_path):
        """
        Create a new ChatBot instance from a JSON config file.
        """
        import json
        with open(config_file_path, 'r') as config_file:
            data = json.load(config_file)

        name = data.pop('name')

        return B4Bot(name, **data)

    class InvalidAdapterException(Exception):
        """
        An exception to be raised when an adapter of an unexpected class type is recieved.
        """

        def __init__(self, value='Recieved an unexpected adapter setting.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
