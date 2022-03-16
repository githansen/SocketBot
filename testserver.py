import _thread
import socket
import sys
import random
import threading
import time

# This function returns a verb for a suggestion that the server sends out
def gensuggestions():
    action = random.choice(["cry", "hike", "run", "walk", "swim", "sleep", "cry", "fight", "drink", "party",
                            "climb", "kick", "shoot", "kill", "work", "think", "look", "find",
                            "sing", "drive", "perform", "build", "create", "develop", "code",
                            "laugh", "fly", "cook", "wash", "talk", "hang", "paint", "dive", "buy"])
    return action


def printresponses():
    for z in responselist:
        print(z)
        time.sleep(1)
    for z in bad_messages:
        print(z)
    bad_messages.clear()
    responselist.clear()

# Socket configuration
host = socket.gethostbyname(socket.gethostname())
port = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))

# List of connections, names of bots and responses from the bots
connection_list = []
botlist = []
responselist = []
errorlist = []
bad_messages = []
print("Welcome to the chat program. ")

def printerrors():
    for x in errorlist:
        print(x)
    errorlist.clear()

# This function takes in a name as a parameter, looks for a connection with the same name, and then kicks the bot out
def kickbot(botname):
    i = 0;
    success = False
    while i < len(botlist):
        if botlist[i] in botname:
            print("{} has been kicked out".format(botlist[i]))
            botlist.pop(i)
            connection_list[i].close()
            connection_list.pop(i)
            success = True
        i += 1
    if not success:
        print("No such bot as {}".format(botname.split()[1]))


def kickcon(c, reason):
    f = 0
    while f < len(connection_list):
        if connection_list[f] == c:
            errorlist.append("{} has been kicked out for {}".format(botlist[f], reason))
            botlist.pop(f)
            connection_list[f].close()
            connection_list.pop(f)
            break
        f += 1


# Function to check if all bots in the list are still connected
def stillconnected(c):
        f = 0
        while f < len(connection_list):
            # Try-except checks if the bots in the list are still connected by sending a message.
            # If it's disconnected, an exception will be thrown
            if c == connection_list[f]:
                try:
                    c.send("connectedx29".encode())
                    return True
                except:
                    print(botlist[f] + " has been disconnected")
                    connection_list.pop(f)
                    botlist.pop(f)
                    return False
            f += 1
        return False


# Sends back all responses to all clients except the one it came from
def sendback():
    f = 0
    print(len(connection_list))
    print(len(responselist))
    while f < len(connection_list):
        i = 0
        while i < len(responselist):
            if i != f:
                message = responselist[i] + " responsex29"
                connection_list[f].send(message.encode())
            i += 1
        for x in bad_messages:
            message = x + " responsex29"
            connection_list[f].send(message.encode())
        f += 1





global global_message
global_message = None




def receive(c):
    while True:
        while global_message != "ready":
            time.sleep(0.00001)
        try:
            p = c.recv(1024).decode()
            responselist.append(p)
            c.settimeout(99999)
        except socket.timeout as e:
            print(e)
            kickcon(c, "taking too long to respond.")
            exit()
        if "f you" in p:
            bad_messages.append(p)
            kickcon(c, "being rude")
            exit()
        else:
            c.settimeout(99999)


def send(c):
    global global_message
    while True:
        if global_message is not None:
            if stillconnected(c) is True:
                c.send(global_message.encode())
                c.settimeout(2)
                global_message = "ready"
            else:
                exit()
            time.sleep(2)
            global_message = None

def connections():
    sock.listen()
    while True:
        # The program should not discriminate and accept all connections
        c, addr = sock.accept()
        name = c.recv(1024).decode()
        # In this program, I will only accept 1 instace of each bot
        if name in botlist:
            c.close()
            print("Bot {} is already connected, you can't have 2 instances of one bot in the program".format(name))
        # Adds both connection and botname in lists
        else:
            botlist.append(name)
            connection_list.append(c)
            print("New Connection: {} botname: {}".format(addr, name))
            thread = threading.Thread(target=receive,args=(c,))
            thread.start()
            thread2 = threading.Thread(target=send, args=(c,))
            thread2.start()

def randomsuggestions(a = None):
    if a is None:
        for i in range(5):
            global global_message
            global_message = "do you want to " + gensuggestions() + " ?"
            print("Me: ", global_message)
            time.sleep(2)
            sendback()
            printresponses()
            printerrors()

# Creates thread that listens for new connection
thread = threading.Thread(target=connections)
thread.start()

print(
    "To get started, please connect at least 2 bots, you currently have {} bots connected".format(len(connection_list)))

# A minimum of 2 connections is needed for the program to start
amount = len(connection_list)
while len(connection_list) < 4:
    if len(connection_list) > amount:
        print("You need 1 more connection to start")
        amount = len(connection_list)
print("The program is ready to start")
time.sleep(2)
print(
    "We will now ask our bots some questions. You get to decide if you want to send custom messages or "
    "randomly generated ones. Currently you have {} bots connected ".format(len(connection_list)))

time.sleep(1)
print("\nSo you can get a feel of it, the program will start of by generating a few messages on it's own")
time.sleep(1)

# Starts program by making some suggestions
randomsuggestions()

print("'r' = sequence of randomly generated messages"
      " \n'n' = message from input\n'kick [botname]' to kick bot from conversation")

while True:
    # Takes input from user to decide what to do next

    x = input()
    if x == "r":
        global_message = "Do you want to {} ?".format(gensuggestions())
        print("Me:", global_message)
        time.sleep(0.1)
    elif x == "n":
        print("Input message")
        global_message = input()
    elif x == "q":
        break;
    elif "kick" in x:
        kickbot(x)
    time.sleep(2)
    printresponses()
    print("You can send a new message now\n'r' = sequence randomly generated messages\n"
          "'n' = message from input\n'kick [botname]' to kick bot from conversation")

