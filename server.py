import queue
import select
import sys
import socket
import time
import random

helpcommands = ["-h", "--h", "-help", "--help"]
if sys.argv[1] in helpcommands:
    print("The program must be invoked by taking in the port number as a parameter\n"
          "Example: 'python server.py 8080' \n"
          "After starting the program, you have to connect at least 2 clients before starting\n"
          "When you are ready, you get the option of sending your own messages, or make the program"
          " generate some at random"
          "\nDon't worry, instructions will be given along the way."
          )
    exit()

botlist = []  # List of bot names connected

host = socket.gethostbyname(socket.gethostname())  # Host IP
port = int(sys.argv[1])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket and bind
sock.bind((host, port))
inputs = [sock]  # Sockets to receive msgs from
outputs = []  # Sockets to send msgs too

response_list = []  # List of responses
errors = []  # List of error messages


def kickcon(c, reason):
    i = 0
    while i < len(outputs):  # Iterates through the connection-list
        if outputs[i] is c:
            name = botlist.pop(i)
            outputs.pop(i)  # Removes the given connection from the lists
            inputs.pop(i + 1)  # Outputs [0] = inputs [1] because inputs[0] is the server
            c.close()
            errors.append("{} has been kicked out for {}".format(name, reason))
        i += 1


def kickbot(name):
    for i in range(len(outputs)):
        if botlist[i] in name:
            outputs[i].close()
            botlist.pop(i)  # Removes name from botlist
            outputs.pop(i)  # Removes from list of outputs
            inputs.pop(i + 1)  # Inputs[0] is never empty, so outputs[1] = inputs[0]
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
    phrases = ["Do you want to {}?", "I feel like going to {} , how about you?", "How do you feel about going to {}?"] # Phrases to send

    phrase = random.choice(phrases).format(action) # Generates a message to send.
    return phrase


def sendback():  # Sends back all responses to all clients except the one it came from

    for f in range(len(response_list)):  # Iterates through the response list
        print(response_list[f])
        time.sleep(1)
        sending = response_list[f] + " responsex29"  # Before sending, we append the code responsex29 so the client
        # knows it's a response from another client
        for s in write:
            # A response should not be sent back to where it came from
            if write.index(s) != f:
                # Try-except in case the client has disconnected
                try:
                    s.send(sending.encode())
                except:
                    pass
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
                    kickcon(f, "a client side error or disconnection")
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



sock.listen()
while True:

    if len(outputs) == 0:
        print("No clients are connected, the program will wait until you have at least 2 connected clients")
        # Creates r-list, w-list and x-list and updates it each iteration in the loop
    read, write, exception = select.select(inputs, outputs, inputs)
    # Allows user to connect up to 4 bots between sequences, and not just 1 per msg sequence
    for o in range(4):
        for s in read:
            if s is sock:
                # Accepts connection from socket
                c, addr = s.accept()
                try:
                    name = c.recv(1024).decode()
                except Exception as e:
                    pass

                if name in botlist: # The program only allows 1 instance of each bot
                    c.close()
                    read, write, exception = select.select(inputs, outputs, inputs)
                    print("Bot {} is already connected, you can't have 2 instances of one bot in the program".format(
                        name))
                    time.sleep(1)
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
                    The client will never receive unsolicited messages, so this is not needed -> all messages from clients 
                    will either come while connecting or inside the broadcast-function
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
        print("You can send a new message now...")
        time.sleep(1)
        print("'r' = sequence of randomly generated messages(5)\n"
              "'n' = message from input\n'kick [botname]' "
              "to kick bot from conversation\n'q' to disconnect and terminate the program")
        x = input()
        if x == "r":
            if len(outputs) > 0: # Checks if list is not empty
                for t in range(5):
                    global_message = gensuggestions()
                    broadcast(sock, global_message)
                    if len(outputs) > 0:
                        print("Sequence done.", end='', flush=True)
                        time.sleep(1)
                        print(".", end='', flush=True)
                        time.sleep(1)
                        print(".")
                        time.sleep(1)
                time.sleep(1)

        elif x == "n":
            print("Input message")
            global_message = input()
            broadcast(sock, global_message)
            # Next lines create a kind of countdown with the ...
            print("Sequence done.", end='', flush=True)
            time.sleep(1)
            print(".", end='', flush=True)
            time.sleep(1)
            print(".")
            time.sleep(1)
        elif "kick" in x:
            kickbot(x) # calls function to kick the bot
        elif x == "q":
            sock.close()
            break;
