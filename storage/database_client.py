import socket
from conversation.statement import Statement


class DatabaseClient():
    '''
    Interogari la BD

    Returneaza un obiect responce
    '''

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host = socket.gethostname()
        self.port = 8888

    def get_db_responce(self, input_statement):
        self.write_json(input_statement, '', dict(), dict())

        return Statement(self.get_answer(self.send()))

    def send(self):
        self.s.connect((self.host, self.port))

        f = open('client_tosend.json', 'rb')

        l = f.read(1024)

        while (l):
            self.s.send(l)
            l = f.read(1024)

        f.close()
        buffer = ''
        l = self.s.recv(1024)

        buffer += l.decode('utf-8')

        while (len(l) == 1024):
            l = self.s.recv(1024)
            buffer += l.decode('utf-8')

        self.s.shutdown(socket.SHUT_WR)
        self.s.close()

        return buffer

    def get_answer(self, db_answer):
        position_of_answer=db_answer.find("answer",0,len(db_answer))
        position_of_answer=position_of_answer+len('answer')+6#sarim " si : "

        answer= db_answer[position_of_answer:]
        position_of_prop=answer.find('"prop":',0,len(answer))
        answer=answer[:position_of_prop]
        return answer

    def write_json(self, question, subjects, dict_prop, dict_answer):
        nr_subj = len(subjects)
        f = open('client_tosend.json', 'w')
        f.write("{\n")
        f.write('"question" : ')
        f.write(' "' + question + '"' + ', \n')
        f.write('"prop": [ ')
        i = 0

        if (nr_subj != 0):
            for index in subjects:
                i = i + 1
                f.write("\n { \n")
                f.write('"Subject" : ')
                f.write('"' + index + '"' + ',')
                length = len(dict_prop[index])
                for x in range(0, length):
                    f.write('\n"' + dict_prop[index][x] + '" : ')
                    f.write('"' + dict_answer[index][x] + '" ')

                    if x < length - 1:
                        f.write(",")

                f.write('\n }')

                if i < nr_subj:
                    f.write(', \n')
                else:
                    f.write('] \n')

        if question != "":
            f.write(']')
        f.write('\n }')
        f.close()
