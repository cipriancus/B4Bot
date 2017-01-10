from __future__ import unicode_literals
from collections import Counter
from model import utils
from .logic_adapter import LogicAdapter


class MultiLogicAdapter(LogicAdapter):
    """
    MultiLogicAdapter allows ChatterBot to use multiple logic
    adapters. It has methods that allow ChatterBot to add an
    adapter, set the chat bot, and process an input statement
    to get a response.

    MultiLogicAdapter permite bot-ului sa aibe mai multe adaptoare logice
    selectand cel mai bun raspuns
    """

    def __init__(self, **kwargs):
        super(MultiLogicAdapter, self).__init__(**kwargs)

        # Adaptorul logic
        self.adapters = []

        # Adaptoare necesare
        # Neaparat NoKnowlegeAdapter
        self.system_adapters = []

    def process(self, statement):
        """
        Se da output ul unor adaptoare logice
        pentru un input
        """
        results = []
        result = None
        max_confidence = -1

        #se parcurg toate adaptoarele
        #se da un raspuns
        #se selecteaza cel mai bun
        for adapter in self.get_adapters():
            if adapter.can_process(statement):
                confidence, output = adapter.process(statement)
                results.append((confidence, output, ))

                if confidence > max_confidence:
                    result = output
                    max_confidence = confidence


        # Daca mai multe adaptoare au acelasi raspuns,
        # probabil e cel mai bun
        if len(results) >= 3:
            statements = [s[1] for s in results]
            count = Counter(statements)
            most_common = count.most_common()
            if most_common[0][1] > 1:
                result = most_common[0][0]
                max_confidence = self.get_greatest_confidence(result, results)

        return max_confidence, result

    def get_greatest_confidence(self, statement, options):
        """
        Trimite cea mai mare valoare de incredere pentru un statement
        ce apare de mai multe ori
        """
        values = []
        for option in options:
            if option[1] == statement:
                values.append(option[0])

        return max(values)

    def get_adapters(self):
        adapters = []
        adapters.extend(self.adapters)
        adapters.extend(self.system_adapters)
        return adapters

    def add_adapter(self, adapter, **kwargs):
        utils.validate_adapter_class(adapter, LogicAdapter)
        adapter = utils.initialize_class(adapter, **kwargs)
        self.adapters.append(adapter)

    def insert_logic_adapter(self, logic_adapter, insert_index, **kwargs):
        utils.validate_adapter_class(logic_adapter, LogicAdapter)

        NewAdapter = utils.import_module(logic_adapter)
        adapter = NewAdapter(**kwargs)

        self.adapters.insert(insert_index, adapter)

    def remove_logic_adapter(self, adapter_name):
        for index, adapter in enumerate(self.adapters):
            if adapter_name == type(adapter).__name__:
                del self.adapters[index]
                return True
        return False

    def set_chatbot(self, chatbot):
        super(MultiLogicAdapter, self).set_chatbot(chatbot)

        for adapter in self.get_adapters():
            adapter.set_chatbot(chatbot)
