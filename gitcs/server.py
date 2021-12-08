import threading
import socket
import sys


print_lock = threading.Lock() # mutex to lock for print functions

users = [] # list of users
conns = []


def worker(s, addr):

    # users string that will add all the users for display
    allUsers = "Users: ".encode("utf-8")

    # Dsiplay connection address everytime a connection occurs
    print('Connection address:', addr)
    print('\n')

    # username and first message variables
    username = ''
    first_time = True

    while 1:

        data = s.recv(BUFFER_SIZE)

        #disconnects
        if not data:
            #print_lock.acquire()
            print(username + " disconnected")
            users.remove(username)
            #print_lock.release()
            # remove user from list of users

            conns.remove(s)

            #print_lock.acquire()  # update names must be locked
            if len(users) == 0:
                users.append("")
            #print_lock.release()
            break

        # check if its the user is barely connecting and tell the user that they need a username
        if username == '' and first_time == True:
            # check if users are already connected to the server before hand
            if len(users) != 0:
                for x in users:
                    allUsers += (x + ", ").encode("utf-8")
                str = ("Weclome User. Here is a list of users. ".encode("utf-8") + allUsers +
                   ". Please Provide a username for your user".encode("utf-8"))
                s.send(str)
                first_time = False

            #first user connected
            else:
                str = ("Weclome User. Here is a list of users.".encode("utf-8") + " You are the only current user.".encode("utf-8") +
                       " Please Provide a username for your user".encode("utf-8"))
                s.send(str)
                first_time = False

        #check if user is barely connected but their username hasnt been added yet
        elif username == '' and not first_time:
            username = data.decode('utf-8')
            #print_lock.acquire()
            str2 = username + " > " + data.decode("utf-8")
            print(str2)
            users.append(username)

            #print_lock.release()
            x = 0
            while x < len(users):
                if username == users[x]:
                    conns[x].send(str2.encode("utf-8"))
                x = x + 1

        #if the username has already been added, then just receive any extra data that the client sends
        else:
            str2 = username + " > " + data.decode("utf-8")
            #print_lock.acquire()
            print(str2)
            #print_lock.release()
            x = 0
            while x < len(users):
                if username == users[x]:
                    conns[x].send(str2.encode("utf-8"))
                x = x + 1
#hi
    #close the socket
    s.close()

#socket details
if len(sys.argv) == 3:
    #print("Custom")
    TCP_IP = str(sys.argv[1])
    TCP_PORT = int(sys.argv[2])
else:
   # print("default")
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5005
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(20)
#up to 20 connections
#print(TCP_IP)
#print(TCP_PORT)
print("socket is listening" )

while 1:
    #accept connections and start a thread for each
    conn, addr = s.accept()

    #check if server is full
    if len(users) > 19:
        print("The Server is currently full!")
        conn.send("Full!".encode("utf-8"))
    else:
        conns.append(conn)
        t = threading.Thread(target=worker, args=(conn, addr))
        t.start()
s.close()