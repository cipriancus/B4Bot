from __future__ import unicode_literals
from storage.storage_adapter import StorageAdapter
from input.input_adapter import InputAdapter
from model import utils


class B4Bot(object):
    def __init__(self, **kwargs):
        from conversation.session import SessionManager
        from logic.multi_adapter import MultiLogicAdapter

        storage_adapter = kwargs.get('storage_adapter', 'storage.jsonfile.JsonFileStorageAdapter')

        logic_adapters = kwargs.get('logic_adapters',
                                    [
                                        'logic.best_match.BestMatch',
                                        'logic.mathematical_evaluation.MathematicalEvaluation',
                                        'logic.time_adapter.TimeLogicAdapter',
                                        'logic.joke_adapter.JokeLogicAdapter',
                                        'logic.low_confidence.LowConfidenceAdapter',
                                        'logic.entity_adapter.EntityLogicAdapter',
                                        'logic.interesting_adapter.InterestingLogicAdapter'
                                    ])

        input_adapter = kwargs.get('input_adapter', 'input.variable_input_type_adapter.VariableInputTypeAdapter')

        # Verificam adaptorii daca au impelentat interfetele corespunzatoare
        utils.validate_adapter_class(storage_adapter, StorageAdapter)
        utils.validate_adapter_class(input_adapter, InputAdapter)

        # da raspunsul efectiv, folosind mai multe adaptoare
        self.logic = MultiLogicAdapter(**kwargs)

        self.storage = utils.initialize_class(storage_adapter, **kwargs)

        self.input = utils.initialize_class(input_adapter, **kwargs)

        filters = kwargs.get('filters', tuple())
        self.filters = (utils.import_module(F)() for F in filters)

        # Setam un adaptor defaul in MultiLogicAdapter
        self.logic.system_adapters.append(
            utils.initialize_class('logic.no_knowledge_adapter.NoKnowledgeAdapter', **kwargs))

        # adaugam adaptoarele pentru raspunsurile noastre
        # in MultiLogicAdapter
        for adapter in logic_adapters:
            self.logic.add_adapter(adapter, **kwargs)

        # le dam adaptoarelor instanta de robot
        self.storage.set_chatbot(self)
        self.logic.set_chatbot(self)
        self.input.set_chatbot(self)

        try:
            kwargs.get('trainer', 'trainer.trainers.Trainer')
            trainer = kwargs.get('trainer', 'trainer.trainers.Trainer')

            TrainerClass = utils.import_module(trainer)
            self.trainer = TrainerClass(self.storage, **kwargs)
            self.training_data = kwargs.get('training_data')
        except ImportError:
            pass

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
        nltk_download_corpus('vader_lexicon')

    def get_response(self, input_item, session_id=None):
        """
        Trimitem raspunsul utilizatorului robotului pentru un input
        """
        if not session_id:
            session_id = str(self.default_session.uuid)

        input_statement = self.input.process_input_statement(input_item)

        statement, response, confidence = self.generate_response(input_statement, session_id)

        # Invatam ca input ul userului a fost raspuns valid la ultimul output
        previous_statement = self.conversation_sessions.get(
            session_id
        ).conversation.get_last_response_statement()
        self.learn_response(statement, previous_statement)

        self.conversation_sessions.update(session_id, (statement, response,))

        return response

    def generate_response(self, input_statement, session_id=None):
        """
        Trimitem raspunsul robotului pentru un input
        """
        if not session_id:
            session = self.conversation_sessions.get_default()
            session_id = str(session.uuid)

        self.storage.generate_base_query(self, session_id)

        confidence, response = self.logic.process(input_statement)

        return input_statement, response, confidence

    def learn_response(self, statement, previous_statement):
        """
        Se invata raspunsul
        """
        from conversation.response import Response

        if previous_statement:
            statement.add_response(
                Response(previous_statement.text)
            )

        self.storage.update(statement)

    def set_trainer(self, training_class, **kwargs):
        self.trainer = training_class(self.storage, **kwargs)

    @property
    def train(self):
        return self.trainer.train
