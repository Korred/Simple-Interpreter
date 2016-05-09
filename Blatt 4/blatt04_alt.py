class htree(object):
    '''
    Simple tree structure

          value (root)
         <     >
       left    right
    '''
    def __init__(self, value=None, left=None, right=None):
        self.left = left
        self.right = right
        self.value = value


def make_tree(mapping):
    import operator
    # mapping is a dict which is orderless (unless it is an OrderedDict)
    # assuming it is not - sort mapping by ascending values

    sorted_map = sorted(mapping.items(), key=operator.itemgetter(1))
    first_node = sorted_map.pop(0)[0]
    curr_tree = htree(first_node)

    for i in sorted_map:
        curr_tree = htree(None, curr_tree, htree(i[0]))
    return curr_tree


def make_mapping(tree):
    # returns a dict with a code for each leaf-node

    def crawl(tree, code=''):
        if not tree.left and not tree.right:
            return [(tree.value, code)]
        else:
            l = crawl(tree.left, code + "0")
            r = crawl(tree.right, code + "1")
            joined = list()
            joined.append(l)
            joined.append(r)

            return [i for sublist in joined for i in sublist]

    return dict(crawl(tree))


def encode(mapping, string):
    return "".join(map(lambda x: mapping[x], list(string)))

def decode(tree, code):
    curr_node = tree
    decoded = list()

    for c in list(code):
        if curr_node.left and curr_node.right:
            if c == '0':
                if curr_node.left.left and curr_node.left.right:
                    curr_node = curr_node.left
                else:
                    decoded.append(curr_node.left.value)
                    curr_node = tree

            if c == '1':
                if curr_node.right.left and curr_node.right.right:
                    curr_node = curr_node.right
                else:
                    decoded.append(curr_node.right.value)
                    curr_node = tree
        else:
            # edge case - when tree is just a root-node, nothing else
            decoded.append(curr_node.value)

    return "".join(decoded)
