import random

positiveresponses = ["{} sounds great, i would love that", "I havent gone {} in a long time, sounds fun",
                     "Good idea, i would love to go {}",
                     "I like your idea, maybe we can do something else after {}?"]
negativeresponses = ["I'm usually open to doing most things but I really hate {}",
                     "I will never do that, i hate {}",
                     "{} sucks", "If you don't have any other suggestions, I'm in"]
neutralresponses = ["{} is not my cup of tea, but I guess I can give it a try",
                    "I'm not sure if i'm up for {} today",
                    "If {} is the only option, sure.. but I would prefer to do something else"]
previous_suggestion = None
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