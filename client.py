import random
import sys
import socket;

positiveresponses = ["{} sounds great, i would love that", "I havent gone {} in a long time, sounds fun",
                     "Good idea, i would love to go {}",
                     "I like your idea, maybe we can do something else after {}?"]
negativeresponses = ["I'm usually open to doing most things but I really hate {}",
                     "I will never do that, i hate {}",
                     "{} sucks", "If you don't have any other suggestions, I'm in"]
neutralresponses = ["{} is not my cup of tea, but I guess I can give it a try",
                    "I'm not sure if i'm up for {} today",
                    "If {} is the only option, sure.. but I would prefer to do something else"]

global previous_suggestion
previous_suggestion = None;


def findresponse(likes, dislikes, hates, a):
    # Makes an iterable list containing all the words sent from the server
    wordlist = a.split()
    global previous_suggestion
    for word in wordlist:
        # 3 next if statements checks if the word is in my list of actions and returns an appropriate response from
        # the bot
        if word in likes:
            previous_suggestion = word;
            return random.choice(positiveresponses).format(word + "ing")
        elif word in dislikes:
            previous_suggestion = word
            return random.choice(neutralresponses).format(word + "ing")
        elif word in hates:
            temp = previous_suggestion
            previous_suggestion = word
            # If the bot hates the suggestion, there is a 1 in 25 chance the bots response will be a swear word
            if random.randint(0, 25) == 1:
                return "f you"
            else:
                previous_suggestion = word
                # If the bot hates this suggestion, and liked or was neutral to the previous suggestion
                # it will suggest that instead
                if temp in likes or temp in dislikes:
                    sugg1 = word + "ing"
                    sugg2 = temp + "ing"
                    return "I don't really like {}, but i liked your previous suggestion" \
                           " {} much better. I would rather do that".format(sugg1, sugg2)
                else:
                    return random.choice(negativeresponses).format(word + "ing")

    return "I don't understand, sorry"


def alice(a):
    # List of verbs that the bot likes, dislikes and hates
    dislikes = ["cry", "hike", "run", "walk", "swim", "sleep", "cry", "fight", "drink", "party", "climb", "kick"]
    likes = ["shoot", "kill", "work", "think", "look", "find", "sing", "drive", "perform", "build", "create"]
    hates = ["develop", "code", "laugh", "fly", "cook", "wash", "talk", "hang", "paint", "dive", "buy"]
    return findresponse(likes, dislikes, hates, a)



def bob(a):
    # List of verbs that the bot likes, dislikes and hates
    dislikes = ["cry", "hike", "run", "walk", "swim", "sleep", "cry", "fight", "drink", "party", "climb", "kick"]
    hates = ["shoot", "kill", "work", "think", "look", "find", "sing", "drive", "perform", "build", "create"]
    likes = ["develop", "code", "laugh", "fly", "cook", "wash", "talk", "hang", "paint", "dive", "buy"]
    return findresponse(likes, dislikes, hates, a)


def dora(a):
    # List of verbs that the bot likes, dislikes and hates
    likes = ["cry", "hike", "run", "walk", "swim", "sleep", "cry", "fight", "drink", "party", "climb", "kick"]
    hates = ["shoot", "kill", "work", "think", "look", "find", "sing", "drive", "perform", "build", "create"]
    dislikes = ["develop", "code", "laugh", "fly", "cook", "wash", "talk", "hang", "paint", "dive", "buy"]
    return findresponse(likes, dislikes, hates, a)

def chuck(a):
    # List of verbs that the bot likes, dislikes and hates
    likes = ["cry", "hike", "run", "walk", "swim", "sleep", "cry", "fight", "drink", "party", "climb", "kick"]
    dislikes = ["shoot", "kill", "work", "think", "look", "find", "sing", "drive", "perform", "build", "create"]
    hates = ["develop", "code", "laugh", "fly", "cook", "wash", "talk", "hang", "paint", "dive", "buy"]
    return findresponse(likes, dislikes, hates, a)
    #return "f you"


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

# The client will receive 3 types of messages -> messages to see if the client is still connected,
# messages that are responses from other clients, and suggestions from the host
while True:
    x = socket.recv(1024).decode()

    # responsex29 signifies a response from another client.
    # Before printing the message, it cuts out the identifier 'responsex29'
    if "responsex29" in x:
        x = x.replace("responsex29", "")
        print(x)
    # connectedx29 signifies a message to check if client is connected
    # If it doesn't have the identifier, we know it's a suggestion from the server/host,
    # so we will print it out and send a response to the suggestion
    else:
        x = x.replace("?", "")
        sending = botname + ": " + findbot(botname, x)
        print("New sequence... ")
        print("\nHost:" + x)
        socket.send(sending.encode())
        sending = sending.replace(botname + ":", "")
        print("Me:", sending)
