import socket
##############################MOODUL 3##################################

HOST = ''
PORT_KM = 50010
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_answer(answer):
    s.connect((HOST, PORT_KM))
    s.sendall(bytes(answer,'utf-8'))
    s.close()
