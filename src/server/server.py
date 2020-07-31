import socket
import sys
from os import listdir

mypath ='.'
from os.path import isfile, join

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
from os import walk


def listFiles():
    f = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        break
    return f


HOST = ''
PORT = 3820

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, PORT))

socket.listen(1)
while (1):
    conn, addr = socket.accept()
    print('New client connected ..')
    reqCommand = conn.recv(1024)
    reqCommand = reqCommand.decode()
    print('Client> %s' % (reqCommand))
    if (reqCommand == 'quit'):
        conn.close()
        socket.close()
    elif (reqCommand == 'lls'):
        list = listFiles()
        a = 'server.py'
        b = '.DS_Store'
        for k in list:
            print(k)
            if (k == a or k == b):
                list.remove(k)
        y=""
        for j in list:
            y=y+j+" "
        conn.send(y.encode())
            

    # elif (reqCommand == lls):
    # list file in server directory
    else:
        string = reqCommand.split(' ', 1)  # in case of 'put' and 'get' method
        reqFile = string[1]

        if (string[0] == 'put'):
            with open(reqFile, 'wb') as file_to_write:
                while True:
                    data = conn.recv(1024)
                    # sdata=data.decode()
                    if not data:
                        break
                    file_to_write.write(data)
            file_to_write.close()
            print('Receive Successful')
        elif (string[0] == 'get'):
            with open(reqFile, 'rb') as file_to_send:
                for data in file_to_send:
                    conn.sendall(data)
            print('Send Successful')

    conn.close()

socket.close()
