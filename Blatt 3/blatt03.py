# AUFGABE 1

def mygetattr(obj, name):
    # gets attributes of instance
    try:
        return obj.__dict__[name]
    except (KeyError, AttributeError):
        pass # <-- modify this part
    # else if not found - get attributes of class
    # return mygetattr_class(obj, name)
    # raise AttributeError("Attribute was not found)

def register_override():
    global virtual_attr
    virtual_attr = dict()
    # ...

# AUFGABE 2


def lifestep(field):
    offset = range(-1, 2)
    new_field = set()
    # for every neighbour of a living cell
    # count adjacent living cells
    # if neighbour was a living cell and has 2-3 adjacent living cells -> add to new field
    # if neighbour was a dead cell and has 3 adjacent living cells -> add to new field

    for cell in field:
        for y in offset:
            for x in offset:
                check = (cell[0] + x, cell[1] + y)
                adjacent = 0
                for cy in offset:
                    for cx in offset:
                        neighbour = (check[0] + cy, check[1] + cx)
                        if neighbour in field and neighbour != check:
                            adjacent += 1
                if check in field:
                    if adjacent == 2 or adjacent == 3:
                        new_field.add(check)
                else:
                    if adjacent == 3:
                        new_field.add(check)

    return new_field


def lifestring(field):
    min_val = list(map(min, zip(*field)))  # holds [x-min, y-min] values of field
    max_val = list(map(max, zip(*field)))  # holds [x-max, y-max] values of field

    string = []

    if field:
        for y in range(min_val[1], max_val[1] + 1):
            for x in range(min_val[0], max_val[0] + 1):
                if (x, y) in field:
                    string.append("X")
                else:
                    string.append(" ")
            if y != max_val[1]:  # just add newline "\n" when line is not last line
                string.append("\n")

    return "".join(string)


# AUFGABE 3

class OpenClass(type):
    def __new__(cls, name, bases, attr):
        if name == "__enhance__":
            att_keys = [key for key in attr if not key.startswith("__")]
            for b in bases:
                for key in att_keys:
                    setattr(b, key, attr[key])
        else:
            # return type.__new__(cls, name, bases, attr)
            return super(OpenClass, cls).__new__(cls, name, bases, attr)
