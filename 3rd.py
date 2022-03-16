import queue
import select
import sys
import socket
import time
import random

botlist = []
host = socket.gethostbyname(socket.gethostname())
print(host)
port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
# Sockets from which we expect to read
inputs = [sock]
# Sockets to which we expect to write
outputs = []

response_list = []
errors = []


def kickcon(c, reason):
    i = 0
    while i < len(outputs):
        if outputs[i] is c:
            name = botlist.pop(i)
            outputs.pop(i)
            inputs.pop(i + 1)
            c.close()
            errors.append("{} has been kicked out for {}".format(name, reason))
        i += 1


def kickbot(name):
    i = 0
    for i in range(len(outputs)):
        if botlist[i] in name:
            outputs[i].close()
            botlist.pop(i)
            outputs.pop(i)
            # Inputs[0] is never empty, so outputs[1] = inputs[0]
            inputs.pop(i + 1)
            print("{} has been kicked out".format(name.split()[1]))
            time.sleep(2)
            return
        i += 1
    print("No such bot as {}".format(name.split()[1]))


def gensuggestions():
    action = random.choice(["cry", "hike", "run", "walk", "swim", "sleep", "cry", "fight", "drink", "party",
                            "climb", "kick", "shoot", "kill", "work", "think", "look", "find",
                            "sing", "drive", "perform", "build", "create", "develop", "code",
                            "laugh", "fly", "cook", "wash", "talk", "hang", "paint", "dive", "buy"])
    phrases = ["Let's go {}?", "Do you want to {}?", "I feel like going to {} , how about you?",
               "I haven't gone {} in a long time", "How do you feel about {}?"]

    phrase = random.choice(phrases).format(action)
    return phrase


# Sends back all responses to all clients except the one it came from
def sendback():
    # Iterates through the response list
    for f in range(len(response_list)):
        # Prints the response
        print(response_list[f])
        time.sleep(1)
        # Before sending, we append the code responsex29 so the client knows it's a response from another client
        sending = response_list[f] + " responsex29"
        for s in write:
            # A response should not be sent back to where it came from
            if write.index(s) != f:
                # Try-except in case the client has disconnected
                try:
                    s.send(sending.encode())
                except:
                    pass
    # Prints error messages
    for x in errors:
        print(x)
        time.sleep(1)
    # Clears the lists of responses and errors for the next msg sequence
    response_list.clear()
    errors.clear()


def broadcast(c, message):
    global read, write, exception
    if len(outputs) == 0:
        return
    # If the message is coming from the host
    if c is sock:
        print("Me: " + message)
        time.sleep(1)
        # Iterates through sockets ready to receive a message
        for f in write:
            # When we reach a client
            if f is not sock:
                # A good program will check if clients are
                # still connected before trying to interact with them, this is done with a try-except
                try:
                    f.send(message.encode())
                    f.settimeout(2)
                except Exception as e:
                    kickcon(f, "unknown reason")
                    if len(outputs) == 0:
                        sendback()
                        return
                # If the sending was successful,
                # we will receive the response from the client. try-except in case of a timeout
                else:
                    try:
                        x = f.recv(1024).decode()
                        response_list.append(x)
                        # If the response is a bad word, the client will be kicked out
                        if " f you" in x:
                            kickcon(f, "misbehaving")
                            if len(outputs) == 0:
                                return
                    # In case of a timeout, we will kick the client
                    except socket.timeout as e:
                        kickcon(f, "taking too long to respond")
                        if len(outputs) == 0:
                            sendback()
                            return
    sendback()
    read, write, exception = select.select(inputs, outputs, inputs)
    """
    # If the message is from one of the clients
    else:
        print(message)
        time.sleep(1)
        # Iterates through list of clients ready to receive
        for f in outputs:
            # "All responses should be sent back out to all clients except the one who sent it." Sock is not a client
            if f is not sock and f is not c:
                message = message + " responsex29"
                try:
                    f.send(message.encode())
                except Exception as e:
                    pass
"""


sock.listen()
while True:

    if len(outputs) == 0:
        print("No clients are connected, the program will wait until you connect clients")
        # Creates r-list, w-list and x-list and updates it each iteration in the loop
    read, write, exception = select.select(inputs, outputs, inputs)
    # Allows user to connect up to 2 bots between sequences, and not just 1 per msg sequence
    for o in range(2):
        for s in read:
            if s is sock:
                # Accepts connection from socket
                c, addr = s.accept()
                try:
                    name = c.recv(1024).decode()
                except Exception as e:
                    pass
                # The program only allows 1 instance of each bot
                if name in botlist:
                    c.close()
                    print("Bot {} is already connected, you can't have 2 instances of one bot in the program".format(
                        name))
                else:
                    # Updates the lists with the new connection
                    inputs.append(c)
                    outputs.append(c)
                    botlist.append(name)
                    read, write, exception = select.select(inputs, outputs, inputs)
                    print("New connection", addr)
                    time.sleep(1)
                    print(name + " will take part in the conversation now")
                    time.sleep(1)

                    """
            elif s in outputs:
                try:
                    data = s.recv(1024).decode()
                    print(data)
                    broadcast(s, data)
                except socket.timeout as e:
                    print(e)
                    """
    # The program needs at least 2 connections to be able to start
    if len(outputs) < 2:
        print("Please connect more clients to continue")
        time.sleep(3)
    else:
        # The user decides on input whether he wants a sequence of random messages,
        # kick a user or write their own message to the bots
        print("You can send a new message now\n'r' = sequence of randomly generated messages(5)\n"
              "'n' = message from input\n'kick [botname]' "
              "to kick bot from conversation\n'q' to disconnect and terminate the program")
        x = input()
        if x == "r":
            if len(outputs) > 0:
                for t in range(5):
                    global_message = gensuggestions()
                    broadcast(sock, global_message)
                    if len(outputs) > 0:
                        print("Sequence done...")
                        time.sleep(1)
                time.sleep(1)

        elif x == "n":
            print("Input message")
            global_message = input()
            broadcast(sock, global_message)
            print("Sequence done....")
            time.sleep(1)
        elif "kick" in x:
            kickbot(x)
        elif x == "q":
            sock.close()
            break;
