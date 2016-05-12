# Aufgabe 1 - Huffman Coding

class node:

    def __init__(self,value,weight,left,right,parent,isLeaf):
        self.value = value
        self.weight = weight
        self.left = left
        self.right = right
        self.parent = parent
        self.isLeaf = isLeaf

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
        treeList.append(node(value,weight,None,None,None,True))
    while (len(treeList) > 1):
        sub1, sub2 = getTwoLowestNodes(treeList)
        treeList.remove(sub1)
        treeList.remove(sub2)
        new_internal = node(None,sub1.weight+sub2.weight,sub1,sub2,None,False)
        treeList.append(new_internal)
        sub1.parent = new_internal
        sub2.parent = new_internal

    return treeList[0]

# return two nodes with the lowest weight
def getTwoLowestNodes(nodeList):
    sortedNodeList = sorted(nodeList, key=lambda x: x.weight, reverse=False)
    return sortedNodeList[0],sortedNodeList[1]

def make_mapping(tree):
    mapping = {}
    leafNodes = getLeafNodes(tree)
    for leaf in leafNodes:
        mapping.update({leaf.value: followLeafGetCode(leaf)})
    return mapping

def getLeafNodes(tree):
    if (tree.isLeaf):
        return set([tree])
    else:
        return getLeafNodes(tree.left).union(getLeafNodes(tree.right))

# get code for a specific leaf node
def followLeafGetCode(inNode):
    coding = []
    while inNode.parent is not None:
        coding.append(inNode.getCode())          # effizienter: liste erstellen mit den einzelnen Strings, dann .join verwenden
        inNode = inNode.parent
    string = "".join(coding)
    return string[::-1]

def encode(mapping,text):
    code = []
    for s in text:
        code.append(mapping[s])
    return "".join(code)

def decode(tree,code):
    text = []
    for s in code:
        if(len(code) != 0):
            value,code = getValueFromCode(tree,code)
            text.append(value)
    return "".join(text)

def getValueFromCode(tree,code):
    if (tree.isLeaf):
        return tree.value, code
    else:
        if (code.replace(code[1:],'') == "1"):
            return getValueFromCode(tree.right,code[1:])
        else:
            return getValueFromCode(tree.left,code[1:])
