
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


# Socket configuration
host = socket.gethostbyname(socket.gethostname())
port = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))

# List of connections, names of bots and responses from the bots
connection_list = []
botlist = []
responselist = []
bad_messages = []
print("Welcome to the chat program. ")


# This function takes in a name as a parameter, looks for a connection with the same name, and then kicks the bot out
def kickbot(botname, reason):
    i = 0;
    success = False
    while i < len(botlist):
        if botlist[i] in botname:
            print("{} has been kicked out for {}".format(botlist[i], reason))
            botlist.pop(i)
            connection_list[i].close()
            connection_list.pop(i)
            success = True
        i += 1
    if not success:
        print("No such bot as {}".format(botname.split()[1]))


# Function to check if all bots in the list are still connected
def stillconnected():
    f = 0
    while f < len(connection_list):
        # Try-except checks if the bots in the list are still connected by sending a message.
        # If it's disconnected, an exception will be thrown
        try:
            connection_list[f].send("connectedx29".encode())
        except:
            print(botlist[f] + " has been disconnected")
            connection_list.pop(f)
            botlist.pop(f)
        f += 1


# Function to send message
def msg(a=None):
    # "A good program will check if clients are
    # still connected before trying to interact with them."
    stillconnected()

    f = 0
    # If a random message is requested, gensuggestions() will genereate it
    if a is None:
        sugg = gensuggestions()
        a = "Do you want to {}".format(sugg)
        print("Me:" + a)
        time.sleep(1)
    # If a custom message is requested, a will be the message from input
    else:
        print("ME:", a)
        time.sleep(1)
    # Iterates over list of connections and sends out to all
    while f < len(connection_list):
        connection_list[f].send(a.encode())
        time.sleep(1)
        # settimeout sets a max amount of time for the client to respond
        connection_list[f].settimeout(5)
        p = None
        # If a client takes longer than the set timeout limit,
        # an exception will be thrown and the program will stop. Therefore we need a try-except;
        try:
            p = connection_list[f].recv(1024).decode()
            print(p)
        # If an exception is thrown (response takes too long time), the bot will be kicked out
        except socket.timeout as e:
            kickbot(botlist[f], "taking too long to respond.")
        time.sleep(1);
        # If bot misbehaves
        if p is not None and "f you" in p:
            # Stores the bad message to send out later
            bad_messages.append(p)
            kickbot(botlist[f], "being rude.")
            f -= 1
        elif p is not None:
            responselist.append(p)
        f += 1
    # Sends all responses to all clients
    sendback()
    bad_messages.clear()
    responselist.clear()
    time.sleep(1);
    print(".... \nMessaging sequence done\n....")
    time.sleep(1)


# Sends back all responses to all clients except the one it came from
def sendback():
    f = 0
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


def randomsuggestions():
    for i in range(5):
        msg()


# Creates thread that listens for new connection
thread = threading.Thread(target=connections)
thread.start()

print(
    "To get started, please connect at least 2 bots, you currently have {} bots connected".format(len(connection_list)))

# A minimum of 2 connections is needed for the program to start
amount = len(connection_list)
while len(connection_list) < 2:
    if len(connection_list) > amount:
        print("You need 1 more connection to start")
        amount = len(connection_list)
print("The program is ready to start")
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
        randomsuggestions()

    elif x == "n":
        print("Input message")
        msg(input())
    elif x == "q":
        break;
    elif "kick" in x:
        kickbot(x)
    print("You can send a new message now\n'r' = sequence randomly generated messages\n"
          "'n' = message from input\n'kick [botname]' to kick bot from conversation")
