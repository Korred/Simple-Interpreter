# Aufgabe 1

# Aufgabe 2

# Aufgabe 3
def mybin(integer):
    if integer == 0:
        return "0"
    else:
        bin = []
        while integer > 0:
            if (round(integer) & 1) == 0:
                bin = ["0"] + bin      # append to front, because we need to read bits backwards
            else:
                bin = ["1"] + bin
            integer = integer // 2
        bin = ["0b"] + bin
        return "".join(bin)

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