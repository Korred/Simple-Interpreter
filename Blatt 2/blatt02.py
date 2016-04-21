import random
from collections import deque
# FYI: Run only specific test - for example: py.test -q -s blatt02.py::test_stack_list


# AUFGABE 1
def compute_word_occurences(text):
    words = text.split()
    nest = dict()
    for i in range(len(words)):
        if i+1 < len(words):
            curr = words[i]
            foll = words[i+1]
            if curr not in nest:
                nest[curr] = dict()
            if foll not in nest[curr]:
                nest[curr][foll] = 0
            nest[curr][foll] += 1
    return nest


def make_random_text(nest, num):
    start = random.choice(list(nest.keys()))
    random_text = [start]

    for i in range(num-1):
        d = nest[random_text[i]]
        if d:  # check if dict for given word is not empty
            max_word = max(d.keys(), key=lambda k: d[k])  # lambda function to define key for max
            random_text.append(max_word)
        else:
            break
    return " ".join(random_text)

# Alternativ:

#def compute_word_occurences(str):
#    words = str.split()                 # split by words
#    dict = {}
#    for word in words:                  # check all words in the string
#        dict[word] = get_following_words_as_dict(word,words)
#    return dict

# in: single word and list of words
# out: dictionary of word's followers as key and amount of occurences as value
#def get_following_words_as_dict(word,words):
#    followers = {}
#    for i in range(0,len(words)-1):
#        if word == words[i]:
#            follower = words[i+1]
#            if follower in followers:   # increase amount of word thats already in the dictionary
#                followers[follower] = followers[follower]+1
#            else:                       # first entry in dictionary
#                followers[follower] = 1
#    return followers

#def make_random_text(dict,amount):
#    import random
#    text = ""
#    for i in range(0,amount):
#        rand_word = random.choice(dict.keys())
#        text += rand_word
#        text += random.choice(dict[rand_word].keys())
#    return text

# AUFGABE 3
# Mutability of common python types:

# The following are immutable objects:
#    Numeric types: int, float, complex
#    string
#    tuple
#    frozen set
#    bytes

# The following objects are mutable:
#    list
#    dict
#    set
#    byte array

# 3.3

def hanoi(discs):
    return (deque([i for i in range(discs, 0, -1)]), deque(), deque())


def move(towers,f,t):
    amt = len(towers)
    if not (f < amt and t < amt):
        raise ValueError("One of the provided towers does not exist!")
    else:
        try:
            disc = towers[f].pop()
        except IndexError:
            raise ValueError("Cannot move disc from tower {} as no disc present!".format(str(f)))

        if len(towers[t]) > 0:
            upper_disc = towers[t][-1]
            if disc < upper_disc:
                towers[t].append(disc)
            else:
                raise ValueError("Cannot place disc {} on smaller disc {}!".format(str(disc), str(upper_disc)))
        else:
            towers[t].append(disc)
            








