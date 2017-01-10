import os
import socket
import time
from math import floor

import language_check
from nltk.parse import stanford
from nltk.stem import WordNetLemmatizer

from Classes.Client import ClientThread

os.environ["JAVAHOME"] = "C:\Program Files\Java\jre1.8.0_111"
os.environ["STANFORD_PARSER"] = "D:\Stanford\stanford-parser-full-2015-12-09"
os.environ["STANFORD_MODELS"] = "D:\Stanford\stanford-parser-full-2015-12-09"


def main():
    try:
        stanford_parser = stanford.StanfordDependencyParser()
        lemmatizer = WordNetLemmatizer()

        host, port = "", 8000

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))

        print("Serving HTTP on port {p}...".format(p=port))
        sock.listen(1)

        print("Listening to connections...")

        connection, (ip, port) = sock.accept()

        while True:
            print("Connected to client with IP {ip} and port {port}\n".format(ip=ip, port=port))

            start_time = time.time()

            text = connection.recv(1024).decode("UTF-8")
            client = ClientThread(_parser=stanford_parser,
                                  _lemmatizer=lemmatizer,
                                  _connection=connection,
                                  _language_tool=language_check,
                                  _text=text)
            client.start()

            client.join()

            print("Total time is {time} seconds.\n".format(time=floor(time.time() - start_time)))

    except Exception as exception:
        print("Exception occurred in \"main\" > " + str(exception))


if __name__ == '__main__':
    main()
