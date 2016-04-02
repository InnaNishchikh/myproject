import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',8000))
s.listen(1)

while (True):
    connection,address = s.accept()
    data = str(connection.recv(1024))
    print(data)
    path = data.split('\n')[0].split(' ')[1]
    path = path[1:]
    if (path == ''):
        path == 'index.html'
    file = open(path,'rb')
    response = """\
HTTP/1.1 200 OK
Content-Type: text/html



""" + str(file.read())
    connection.send(response.encode())
    
connection.close()
s.close()