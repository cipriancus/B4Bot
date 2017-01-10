from __future__ import unicode_literals
from logic.logic_adapter import LogicAdapter
from conversation.statement import Statement
import re
import json
import decimal
import numpy


class MathematicalEvaluation(LogicAdapter):
    """
    MathematicalEvaluation cauta termeni matematii si
    operatii si spune cu un grad de incredere daca poate
    raspunde la intrebare si ce raspuns este

    Algoritm:

    1) Stergem semne de punctuatie si facem lowercase
    2) Transformam din cuvinte in numere
    3) Cautam o ecuaties
    4) Simplificam ecuatia
    5) Rezolvam cu numpy
    """
    functions = ['log', 'sqrt']

    def __init__(self, **kwargs):
        super(MathematicalEvaluation, self).__init__(**kwargs)

        language = kwargs.get('math_words_language', 'english')
        self.math_words = self.get_language_data(language)
        self.cache = {}

    def get_language_data(self, language):
        """
        Incarcam datele de limba din corpusul nostru
        """
        from corpus import Corpus

        corpus = Corpus()

        math_words_data_file_path = corpus.get_file_path(
            'corpus.data.{}.math_words'.format(language),
            extension='json'
        )

        with open(math_words_data_file_path) as data:
            return json.load(data)

    def can_process(self, statement):
        """
        Determinam daca acest adaptor poate raspunde
        """
        confidence, response = self.process(statement)
        self.cache[statement.text] = (confidence, response)
        return confidence == 1

    def process(self, statement):
        """
        Simplifica statement ul
        si vede daca gaseste termeni matematici in el,
        pentru a putea vedea daca l poate procesa
        """
        input_text = statement.text

        # Daca input ul exista in cache il folosim direct
        if input_text in self.cache:
            cached_result = self.cache[input_text]
            self.cache = {}
            return cached_result

        # Cautam termeni matematici
        expression = str(self.simplify_chunks(self.normalize(input_text)))

        try:
            expression += "= " + str(
                eval(expression, {f: getattr(numpy, f) for f in self.functions})
            )

            # returneaza cu incredere de 0 sau 1 dc poate evalua expresia
            return 1, Statement(expression)
        except:
            return 0, Statement(expression)

    def simplify_chunks(self, input_text):
        """
        Facem split pe text
        """
        string = ''
        chunks = re.split(r"([\w\.-]+|[\(\)\*\+])", input_text)
        chunks = [chunk.strip() for chunk in chunks]
        chunks = [chunk for chunk in chunks if chunk != '']

        #cautam pe bucatile facute split legat de matematica
        for chunk in chunks:
            for checker in ['is_integer', 'is_float', 'is_operator', 'is_constant', 'is_function']:
                result = getattr(self, checker)(chunk)
                if result is not False:
                    string += str(result) + ' '
                    break

        return string

    def is_float(self, string):
        try:
            return decimal.Decimal(string)
        except decimal.DecimalException:
            return False

    def is_integer(self, string):
        try:
            return int(string)
        except:
            return False

    def is_constant(self, string):
        constants = {
            "pi": 3.141693,
            "e": 2.718281
        }
        return constants.get(string, False)

    def is_function(self, string):
        if string in self.functions:
            return string
        else:
            return False

    def is_operator(self, string):
        if string in "+-/*^()":
            return string
        else:
            return False

    def normalize(self, string):
        """
        Procesam textul
        """

        if len(string) is 0:
            return string

        string = string.lower()

        # stergem pucte
        if not string[-1].isalnum():
            string = string[:-1]

        # stergem cuvinte si facem replace
        string = self.substitute_words(string)

        # Returning normalized text
        return string

    def substitute_words(self, string):
        """
        Punem termeni matematici in loc de cuvinte
        """
        condensed_string = '_'.join(string.split())

        for word in self.math_words["words"]:
            condensed_string = re.sub(
                '_'.join(word.split(' ')),
                self.math_words["words"][word],
                condensed_string
            )

        for number in self.math_words["numbers"]:
            condensed_string = re.sub(
                number,
                str(self.math_words["numbers"][number]),
                condensed_string
            )

        for scale in self.math_words["scales"]:
            condensed_string = re.sub(
                "_" + scale,
                " " + self.math_words["scales"][scale],
                condensed_string
            )

        condensed_string = condensed_string.split('_')
        for chunk_index in range(0, len(condensed_string)):
            value = ""

            try:
                value = str(eval(condensed_string[chunk_index]))

                condensed_string[chunk_index] = value
            except:
                pass

        for chunk_index in range(0, len(condensed_string)):
            if self.is_integer(condensed_string[chunk_index]) or self.is_float(condensed_string[chunk_index]):
                i = 1
                start_index = chunk_index
                end_index = -1
                while (chunk_index + i < len(condensed_string) and (self.is_integer(condensed_string[chunk_index + i]) or self.is_float(condensed_string[chunk_index + i]))):
                    end_index = chunk_index + i
                    i += 1

                for sub_chunk in range(start_index, end_index):
                    condensed_string[sub_chunk] += " +"

                condensed_string[start_index] = "( " + condensed_string[start_index]
                condensed_string[end_index] += " )"

        return ' '.join(condensed_string)
