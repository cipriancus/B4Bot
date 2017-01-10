from .response import Response


class Statement(object):
    """
    Un statement este un text pe care cineva il poate spune,
    adica un input text
    """

    def __init__(self, text, **kwargs):
        self.text = text
        self.in_response_to = kwargs.pop('in_response_to', [])
        self.extra_data = kwargs.pop('extra_data', {})

    def __str__(self):
        return self.text

    def __repr__(self):
        return '<Statement text:%s>' % (self.text)

    def __hash__(self):
        return hash(self.text)

    def __eq__(self, other):
        if not other:
            return False

        if isinstance(other, Statement):
            return self.text == other.text

        return self.text == other

    def add_extra_data(self, key, value):
        """
        Aceasta metoda adauga o forma de stocare suplimentara a informatiilor

        Se pot stoca informatii destre acest statement, cum ar fi POS-ul :

            - key = 'pos_tags'
            - value = [('Now', 'RB'), ('for', 'IN'), ('something', 'NN'), ('different', 'JJ')]
        """
        self.extra_data[key] = value

    def add_response(self, response):
        """
        Adauga un raspuns in lista de raspunsuri a statement-ului,
        daca exista se va creste contorul lui
        """
        if not isinstance(response, Response):
            raise Statement.InvalidTypeException(
                'Un obiect de tipul {} a fost primit dar '
                'se astepta un obiect de tipul  {} '.format(
                    type(response),
                    type(Response(''))
                )
            )

        updated = False
        for index in range(0, len(self.in_response_to)):
            if response.text == self.in_response_to[index].text:
                self.in_response_to[index].occurrence += 1
                updated = True

        if not updated:
            self.in_response_to.append(response)

    def remove_response(self, response_text):
        """
        Se sterge un raspuns din lista de raspunsuri a statement ului
        """
        for response in self.in_response_to:
            if response_text == response.text:
                self.in_response_to.remove(response)
                return True
        return False

    def get_response_count(self, statement):
        """
        Cauta numarul de ocazii in care statement-ul a fost folosit
        ca raspuns la input-ul ( statement-ul curent ), adica de cate
        ori s-a folosit acest raspuns pentru o intrebaree
        """
        for response in self.in_response_to:
            if statement.text == response.text:
                return response.occurrence

        return 0

    def serialize(self):
        """
        Creeaza un dictionar din obiect pentru a-l putea
        serializa
        """
        data = {}

        data['text'] = self.text
        data['in_response_to'] = []
        data['extra_data'] = self.extra_data

        for response in self.in_response_to:
            data['in_response_to'].append(response.serialize())

        return data

    class InvalidTypeException(Exception):

        def __init__(self, value='Tip primit invalid'):
            self.value = value

        def __str__(self):
            return repr(self.value)
