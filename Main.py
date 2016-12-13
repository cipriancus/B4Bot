import socket
from Emotion_Analysis import analize
from GET_M2 import get_semantic_field

#######DATE SERVER#####################################################
HOST = ''
PORT = 50008
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
#######################################################################

while 1:
    conn, addr = s.accept()
    data = conn.recv(1024)

    JSONsentence = str(data, 'utf-8')  # primesc propozitia

    sentence = ""  # trebuie luata prima propozitie din json
    pos_score, neg_score = analize(sentence)  # analizez propozitia pentru a detecta emotii

    semantic_fied_of_emotion = get_semantic_field("");  # trimitem emotia si primim campul semantic

    ###trebuie implementat NLG pentru a obtine o fraza
    nlg_sentence = ""

    pos_score, neg_score = analize(nlg_sentence)

    if not data: break
    conn.sendall(data)
    conn.close()
