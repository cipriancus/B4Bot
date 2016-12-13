import socket

##############################MOODUL 2##################################

HOST = ''
PORT_KM = 50009
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def get_semantic_field(emotion):
    # trebuie creat un JSON cu campul semantic field si emotia
    semantic_field_json = ''

    semantic_field_json_bytes = semantic_field_json  # trebuie convertit in bytes

    s.connect((HOST, PORT_KM))
    s.sendall(semantic_field_json_bytes)
    responce = s.recv(128)
    s.close()

    responce = str(responce, 'utf-8')
    return responce


def get_joke():
    # trebuie creat un JSON cu campul joke
    joke_json = ''

    joke_json_bytes = joke_json  # trebuie convertit in bytes

    s.connect((HOST, PORT_KM))
    s.sendall(joke_json_bytes)
    responce = s.recv(128)
    s.close()

    responce = str(responce, 'utf-8')
    return responce


def get_empathy():
    # trebuie creat un JSON cu campul empathy
    empathy_json = ''

    empathy_json_bytes = empathy_json  # trebuie convertit in bytes

    s.connect((HOST, PORT_KM))
    s.sendall(empathy_json_bytes)
    responce = s.recv(128)
    s.close()

    responce = str(responce, 'utf-8')
    return responce


def get_info(info):
    return ''
