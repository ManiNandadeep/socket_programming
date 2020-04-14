import socket
import select
import time
import os
import sys
import random

Q_no=0
Intro="\n\t\t\tWelcome to the Game Show!!\n"
Instruct="INSTRUCTIONS:\nThere will be 3 players participating.\nMarking scheme: +1 for a right answer, -0.5 for a wrong answer.\nType yes or y or YES or Y as buzzer.\nIf no one pressed the buzzer a new question will be appeared.\nThe first player to get 5 points is the winner.\n"
connections = []
addresses = []
Q=["1+1","1+2","1+3","1+4","1+5","1+6","1+7","1+8","1+9","1+10","1+11","1+12","1+13","1+14","1+15","1+16","1+17","1+18","1+19","1+20",
    "1+21","1+22","1+23","1+24","1+25","1+26"]
A=[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
Marks=[0,0,0]
response=[]


def create_socket():
    try:
        global host
        global port
        global s
        # host ="" 
        # print("Enter Port") 
        # port = input()
        host ="127.0.0.1"
        port=1234
        s = socket.socket()

    except socket.error as e:
        print("Socket creation error: " + str(e))


def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, int(port)))
        s.listen(5)

    except socket.error as e:
        print("Socket Binding error" + str(e) + "\n" + "Retrying...")

def Accept_util(j,conn,address):
    print("Connection has been established :Client " + str(j)+" " + address[0])
    conn.send(str.encode(Intro))
    time.sleep(1)
    conn.send(str.encode(Instruct))
    time.sleep(1)
    conn.send(str.encode("You are Player : "+ str(j)))

def Accept():
    for c in connections:
        c.close()

    del connections[:]
    del addresses[:]
    j=0
    while True:
            conn, address = s.accept()
            s.setblocking(1) 
            j=j+1
            connections.append(conn)
            addresses.append(address)
            if j<3:
                Accept_util(j,conn,address)
            else:
                Accept_util(j,conn,address)
                print("Maximum Clients connected")

                Thread()
                break;

def Thread():
    
    for i in range(len(Q)):
        Q_no=generator()
        for conn in connections:
            time.sleep(0.1)
            conn.send(str.encode(Q[Q_no]+": Do You Know this question?"))
        response1=select.select(connections,[],[],20)#str(conn.recv(1024),"utf-8")
        if(len(response1[0])>0):
            
            conn_name = response1[0][0];
            b = conn_name.recv(1024)
            b = b.decode("utf-8")
            response1=()
            for conn in connections:
                if conn!=conn_name:
                    conn.send(str.encode("Sorry, Player "+str(connections.index(conn_name)+1)+ " has pressed the buzzer."))
            for p in range(len(connections)):
                    if connections[p]==conn_name:
                        t=p;

            if b=='Yes' or b=='yes' or b=='YES' or b=='y':
                        conn_name.send(str.encode("Answer the Question"))
                        answer=str(conn_name.recv(1024),"utf-8")
                        if answer==str(A[Q_no]):
                            
                            Marks[t]=Marks[t]+1
                            conn_name.send(str.encode("Correct Answer, You get 1 Point"))
                            if Marks[t]==5:
                                for c in connections:
                                    c.send(str.encode("Terminate"))
                                    time.sleep(1)
                                break
                        else:
                            Marks[t]=Marks[t]-0.5
                            conn_name.send(str.encode("Wrong Answer, You get -0.5 Points"))
                            time.sleep(1)
                        if(len(Q)>0):
                            Q.pop(Q_no)
                            A.pop(Q_no)
            elif b==str(A[i]):
                conn_name.send(str.encode("You didn't press the buzzer before answering. This doesn't count."))
                time.sleep(1)


        else:
            for c in connections:
                c.send(str.encode("Nobody pressed the buzzer.Moving on to the next question"))
            if(len(Q)>0):
                Q.pop(Q_no)
                A.pop(Q_no)
                
        print(Marks)


def Declare_winner():
    i=Marks.index(max(Marks))
    for c in connections:
        if connections.index(c)!=i:
            c.send(str.encode("\nYou scored "+str(Marks[connections.index(c)])+" points\n"))

        else:
            c.send(str.encode("\nCongrats You Won!!!\nWinner Winner Chicken Dinner!!!"))

def generator():
    if(len(Q)>0):
        Q_no=random.randint(0,10000)%len(Q)
        return Q_no

def funcs():
    create_socket()
    bind_socket()
    Accept()
    Declare_winner()


if __name__=="__main__":
    funcs()
