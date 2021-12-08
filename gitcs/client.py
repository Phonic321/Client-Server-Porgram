import socket
import sys


#socket details and connecting
if len(sys.argv) == 3:
    TCP_IP = str(sys.argv[1])
    TCP_PORT = int(sys.argv[2])

else:
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5005
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

s.send("Initial Send".encode("utf-8")) #message sent to start server data collection



first_time = True # first connection loop check
while 1:
    # username check
    if first_time == True:
        data = s.recv(BUFFER_SIZE)

        if not data:
            break

        #check if server is full
        if data.decode("utf-8") == "Full!":
            print("The Server is currently full!")
            break

        print(data)
        answer = input("What is your username(Type END the connection): ")
        first_time = False
        s.send(answer.encode("utf-8"))
    # extra messages
    else:
        data = s.recv(BUFFER_SIZE)

        if not data:
            break

        print(data) #echo

        answer = input("Enter your message you would like to send here. Type END to end the connection: ")
        # disconnect or send check
        if answer == "END":
            break
        else:
            s.send(answer.encode("utf-8"))
s.close()
