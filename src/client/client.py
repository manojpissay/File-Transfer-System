import socket
import sys
from os import listdir
from tkinter import *
from os.path import isfile, join
from os import walk

mypath='.'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

HOST = 'localhost'    # server name goes in here
PORT = 3820
def put(commandName):
    string = commandName.split(' ', 1)
    inputFile = string[1]
    list1=ls1()
    if(inputFile not in list1):
        e2.delete('1.0', END)
        e2.insert(END, inputFile+" does not exist on your system.")
        return
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName.encode())
    
    with open(inputFile, 'rb') as file_to_send:
        for data in file_to_send:
            socket1.sendall(data)
    e2.delete('1.0', END)
    e2.insert(END, 'PUT Successful!')
    print ('PUT Successful')
    socket1.close()
    return


def lls1(string):
       socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       socket1.connect((HOST, PORT))
       str='lls'
       socket1.send(str.encode())
       data=socket1.recv(1024)
       print("The avaiable list files are:\n")
       while(data):
           data=data.decode()
           if(string not in data):
                e2.delete('1.0', END)
                e2.insert(END, string+" does not exist on the server.")
                return 0
           data=socket1.recv(1024)
       

def lls():
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    str='lls'
    socket1.send(str.encode())
    data=socket1.recv(1024)
    e2.delete('1.0', END)
    print("The avaiable list files are:\n")
    while(data):
        print(data.decode())
        e2.insert(END,data.decode()+ " \n")
        data=socket1.recv(1024)
    print("only these files are there\n")

def quit():
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send('quit'.encode())

def ls1():
    f = []
    for (dirpath, dirnames, filenames) in walk(mypath):
           f.extend(filenames)
           return f

def ls():
    f = []
    for (dirpath, dirnames, filenames) in walk(mypath):
           f.extend(filenames)
           break
    e2.delete('1.0', END)
    for i in f:
         print(i)
         e2.insert(END,i+"\n")
         print("\n")

def get(commandName):
    string = commandName.split(' ', 1)
    inputFile = string[1]
    if(lls1(inputFile)==0):
        return
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName.encode())
    with open(inputFile, 'wb') as file_to_write:
        while True:
            data = socket1.recv(1024)
            # print (data)
            if not data:
                break
            # print data
            file_to_write.write(data)
    file_to_write.close()
    e2.delete('1.0', END)
    e2.insert(END, 'GET Successful!')
    print('GET Successful')
    socket1.close()
    return

def getB():
    get("get "+ge.get("1.0", "end-1c")) 

def putB():
    put("put "+pe.get("1.0", "end-1c"))   


gui = Tk()

gui.configure(background = "#fffffe")

gui.title("File Transfer System")

gui.geometry("620x580")

label = Label(gui,text="File Transfer System",font=("Times New Roman",30))
label.grid(sticky=W, padx=150,pady=20,column=2000,row=0)


label=Label(gui,text="Username: ",font=("Sans-Serif",15))
label.grid(sticky=W, padx=100,pady=10, column=2000,row=60)

ue=Text(gui,height=1, width=30)
ue.grid(sticky=W, padx=250,pady=10, column=2000,row=60)


submit = Button(gui,text="LS",fg="black",bg="green",command=ls)
submit.grid(sticky=W, padx=100,pady=0, column=2000,row=80)

submit = Button(gui,text="LLS",fg="black",bg="green",command=lls)
submit.grid(sticky=W, padx=200,pady=10, column=2000,row=80)


ge=Text(gui,height=1, width=30)
ge.grid(sticky=W, padx=100,pady=10, column=2000,row=160)

submit = Button(gui,text="GET",fg="black",bg="green",command=getB)
submit.grid(sticky=W, padx=200,pady=5, column=2000,row=165)




pe=Text(gui,height=1, width=30)
pe.grid(sticky=W, padx=100,pady=10, column=2000,row=180)

submit = Button(gui,text="PUT",fg="black",bg="green",command=putB)
submit.grid(sticky=W, padx=200,pady=5, column=2000,row=185)


e2=Text(gui,height=10, width=30)
e2.grid(sticky=W, padx=100,pady=10, column=2000,row=400)


gui.mainloop()

while(1):
    print('Instruction')
    print ('"put [filename]" to send the file the server ')
    print ('"get [filename]" to download the file from the server ')
    print ('"ls" to list all files in this directory')
    print ('"lls" to list all files in the server')
    print ('"quit" to exit')
    sys.stdout.write('%s> ' % ue)
    inputCommand = sys.stdin.readline().strip()
    if (inputCommand == 'quit'):
        quit()
        break
    elif (inputCommand == 'ls'):
            ls('ls')
    elif (inputCommand == 'lls'):
            lls('lls')
            
    else:
        string = inputCommand.split(' ', 1)
        if (string[0] == 'put'):
            put(inputCommand)
        elif (string[0] == 'get'):
            get(inputCommand)
