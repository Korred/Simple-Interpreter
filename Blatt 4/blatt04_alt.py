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
    # mapping is a dict which is orderless (unless it is an OrderedDict)
    # assuming it is not - sort mapping by ascending values

    node_list = sorted([(htree(k), mapping[k]) for k in mapping], key=lambda x: x[1])

    while node_list:
        if len(node_list) == 1:
            return node_list[0][0]
        else:
            l = node_list.pop(0)
            r = node_list.pop(0)
            new_tree = htree(None, l[0], r[0])
            node_list.append((new_tree, l[1] + r[1]))
            node_list.sort(key=lambda x: x[1])


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