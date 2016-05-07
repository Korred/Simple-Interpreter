# Aufgabe 1 - Huffman Coding

# komischerweise gehen die Tests nicht immer durch, habe wohl irgendeinen Zustand in make_tree
# drin, so dass verschiedenes Verhalten für gleiche Parameter auftritt

class leaf_node:

    type = "leaf"

    def __init__(self,value,weight,parent):
        self.value = value
        self.weight = weight
        self.parent = parent

    def getCode(self):
        if (self.parent.left == self):
            return "0"
        else:
            return "1"

class internal_node:

    type = "internal"

    def __init__(self,weight,left,right,parent):
        self.weight = weight
        self.left = left
        self.right = right
        self.parent = parent

    def getCode(self):
        if (self.parent is not None):
            if (self.parent.left == self):
                return "0"
            else:
                return "1"
        else:
            return ""

# create huffman tree
def make_tree(freq):
    treeList = []
    # create leaf nodes
    for value, weight in freq.items():
        treeList.append(leaf_node(value,weight,None))
    while (len(treeList) > 1):
        sub1, sub2 = getTwoLowestNodes(treeList)
        treeList.remove(sub1)
        treeList.remove(sub2)
        # create new subtree
        if (sub1.weight <= sub2.weight):
            new_internal = internal_node(sub1.weight+sub2.weight,sub1,sub2,None)
        else:
            new_internal = internal_node(sub1.weight+sub2.weight,sub2,sub1,None)
        treeList.append(new_internal)
        sub1.parent = new_internal
        sub2.parent = new_internal

    return treeList[0]

# return two nodes with the lowest weight
def getTwoLowestNodes(nodeList):
    tree1 = None
    tree2 = None
    for t in nodeList:
        if tree1 is not None:
            if (tree2 is None):
                tree2 = t
            else:
                if (t.weight < tree1.weight):
                    tree1 = t
                else:
                    if (t.weight < tree2.weight):
                        tree2 = t
        else:
            tree1 = t
    if (tree1.weight >= tree2.weight):
        return tree1, tree2
    else:
        return tree2, tree1

def make_mapping(tree):
    mapping = {}
    leafNodes = getLeafNodes(tree)
    for leaf in leafNodes:
        mapping.update({leaf.value: followLeafGetCode(leaf)})
    return mapping

def getLeafNodes(tree):
    if (tree.type == "leaf"):
        return set([tree])
    else:
        return getLeafNodes(tree.left).union(getLeafNodes(tree.right))

# get code for a specific leaf node
def followLeafGetCode(inNode):
    coding = ""
    node = inNode
    while node.parent is not None:
        coding += node.getCode()
        node = node.parent
    return coding[::-1]

def encode(mapping,text):
    code = ""
    for s in text:
        code += mapping[s]
    return code

def decode(tree,code):
    text = ""
    for s in code:
        value,code = getValueFromCode(tree,code)
        text += value
    return text

def getValueFromCode(tree,code):
    if (tree.type == "leaf"):
        return tree.value, code
    else:
        if (code.replace(code[1:],'') == "1"):
            return getValueFromCode(tree.right,code[1:])
        else:
            return getValueFromCode(tree.left,code[1:])