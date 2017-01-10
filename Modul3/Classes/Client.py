import json
from threading import Thread

from Modules import functions


class ClientThread(Thread):
    def __init__(self, _parser, _lemmatizer, _connection, _language_tool,_text):
        self.parser = _parser
        self.lemmatizer = _lemmatizer
        self.language_tool = _language_tool
        self.connection = _connection

        self.input_text = _text
        Thread.__init__(self)

    def run(self):
        #question = self.connection.recv(1024)
        # printing the initial response from client

        final_output = functions.parse_sentence(_parser=self.parser,
                                                _lemmatizer=self.lemmatizer,
                                                _text=self.input_text,
                                                _language_tool=self.language_tool)

        open("JSON OutputFile/exemplu.json", "wt").write(json.dumps(final_output, indent=2))

        response = str(final_output)

        self.connection.send(bytes(response, encoding="utf-8"))

        #self.connection.close()
