import random
import sys
import socket
import response

helpcommands = ["-h", "--h", "-help", "--help"]
if sys.argv[1] in helpcommands:
    print("The program must be invoked by giving 3 parameters -> IP-address, port number and bot name\n"
          "Example: python client.py 192.168.56.1 8080 bob\n"
          "For it to work, the bot must be one of bots available, or else the server will kick you out\n"
          "Bot list:\n"
          "bob \n"
          "alice\n"
          "dora\n"
          "chuck\n"
          "soria (all replies from user input)")
    exit()


def alice(a):
    # List of verbs that the bot likes, dislikes and hates
    dislikes = ["cry", "hike", "run", "walk", "swim", "sleep", "cry", "fight", "drink", "party", "climb", "kick"]
    likes = ["shoot", "kill", "work", "think", "look", "find", "sing", "drive", "perform", "build", "create"]
    hates = ["develop", "code", "laugh", "fly", "cook", "wash", "talk", "hang", "paint", "dive", "buy"]
    return response.findresponse(likes, dislikes, hates, a)


def bob(a):
    # List of verbs that the bot likes, dislikes and hates
    dislikes = ["cry", "hike", "run", "walk", "swim", "sleep", "cry", "fight", "drink", "party", "climb", "kick"]
    hates = ["shoot", "kill", "work", "think", "look", "find", "sing", "drive", "perform", "build", "create"]
    likes = ["develop", "code", "laugh", "fly", "cook", "wash", "talk", "hang", "paint", "dive", "buy"]
    return response.findresponse(likes, dislikes, hates, a)


def dora(a):
    # List of verbs that the bot likes, dislikes and hates
    likes = ["cry", "hike", "run", "walk", "swim", "sleep", "cry", "fight", "drink", "party", "climb", "kick"]
    hates = ["shoot", "kill", "work", "think", "look", "find", "sing", "drive", "perform", "build", "create"]
    dislikes = ["develop", "code", "laugh", "fly", "cook", "wash", "talk", "hang", "paint", "dive", "buy"]
    return response.findresponse(likes, dislikes, hates, a)


def chuck(a):
    # List of verbs that the bot likes, dislikes and hates
    likes = ["cry", "hike", "run", "walk", "swim", "sleep", "cry", "fight", "drink", "party", "climb", "kick"]
    dislikes = ["shoot", "kill", "work", "think", "look", "find", "sing", "drive", "perform", "build", "create"]
    hates = ["develop", "code", "laugh", "fly", "cook", "wash", "talk", "hang", "paint", "dive", "buy"]
    return response.findresponse(likes, dislikes, hates, a)


def soria():
    while True:
        msg = socket.recv(1024).decode()
        if "responsex29" in msg:
            msg = msg.replace("responsex29", "")
            print(msg)
        else:
            print(msg)
            print("reply: ")
            reply = botname + ": " + input()
            socket.send(reply.encode())
            reply = reply.replace(botname + ":", "")
            print("Me:", reply)


def findbot(name, msg):
    name = name.lower()
    if name == "chuck":
        return chuck(msg);
    elif name == "dora":
        return dora(msg)
    elif name == "alice":
        return alice(msg)
    elif name == "bob":
        return bob(msg)
    else:
        socket.send("{}:I am not a bot, goodbye".format(name).encode())
        socket.close()
        exit()


ip = sys.argv[1]
port = int(sys.argv[2])
botname = sys.argv[3]

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((ip, port))
socket.send(botname.encode())

if botname == "soria":
    soria()

# The client will receive 2 types of messages ->
# messages that are responses from other clients, and suggestions from the host
while True:
    x = socket.recv(1024).decode()
    # responsex29 signifies a response from another client.
    # Before printing the message, it cuts out the identifier 'responsex29'
    if "responsex29" in x:
        x = x.replace("responsex29", "")
        print(x)

    else:
        print("\nNew sequence... ")
        print("\nHost:" + x)
        x = x.replace("?", "") # Removes the question mark while processing the suggestion and finding response
        sending = botname + ": " + findbot(botname, x) # Calls on findbot() to generate the response
        socket.send(sending.encode())
        sending = sending.replace(botname + ":", "") # Formats the response before printing it out
        print("Me:", sending)
