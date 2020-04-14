import socket
import time
import select
import sys
import os
s = socket.socket()
# print("Enter port:")
# port = input()

# print("Enter IP address:")
# host = input()
port=1234
host="127.0.0.1"

s.connect((host, int(port))) 

inst=str(s.recv(1024),"utf-8")
print (inst)
p=24
k=0
a=str(s.recv(1024),"utf-8")
print(a)
y=str(s.recv(1024),"utf-8")
print(y)
while (k<p):
     
    flag = str(s.recv(1024),"utf-8")
    if flag=="Terminate":
        break
    print(flag)
    c,c1,c2=select.select([sys.stdin,s],[],[],20)
    if len(c)>0:
        if c[0] == sys.stdin:
            y=input()
            s.send(str.encode(y))
        else:
            d=str(c[0].recv(1024),"utf-8")
            print (d)
            k=k+1
            continue;
    flag2=str(s.recv(1024),"utf-8")
    print (flag2)
    if flag2=='Answer the Question':
        ans=input()
        time.sleep(1)
        s.send(str.encode(ans))
        k=k+1
        rep=str(s.recv(1024),"utf-8")
        print(rep)
    
flage3=str(s.recv(1024),"utf-8")
print(flage3)

    