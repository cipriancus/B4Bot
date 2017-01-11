import socket



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 8888               # Reserve a port for your service.

s.connect((host, port))

f = open('client_tosend.json','rb')

print ('Sending..1.')
l = f.read(1024)
while (l):
    print ('Sending..2.')
    s.send(l)
    l = f.read(1024)
print ("out")

f.close()
buffer = ''
l = s.recv(1024)
buffer+=l.decode('utf-8')
while (len(l)==1024):
    print ("Receiving...")
    l = s.recv(1024)
    buffer += l.decode('utf-8')
    print (1)
print ("out")
print (buffer)
print ("Done ")
s.shutdown(socket.SHUT_WR)

s.close()
