# Aufgabe 1

# Aufgabe 2

# Aufgabe 3

def myint(bin_string):
    cut_string = bin_string[2:][::-1]
    length = len(cut_string)
    int = 0
    i = 0
    while i < length:
        expo = length-i-1
        if cut_string[expo] == '1':
            int += 2**expo
        i += 1
    return int