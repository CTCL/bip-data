import sys

class fknode:
    def __init__(self, name, parent=None):
        self.parents = []
        self.children = []
        self.name = name
        if parent:
            self.parents.append(parent)
            parent.children.append(self)

    def add_parent(self, parent):
        self.parents.append(parent)
        parent.children.append(self)

fks = [l.strip().split(' ') for l in open(sys.argv[1], 'rb') if "FOREIGN KEY" in l]
node_dict = {}
fk = fks[0]
child_idx = fk.index("TABLE") + 1
parent_idx = fk.index("REFERENCES") + 1
pairs = [(l[child_idx], l[parent_idx]) for l in fks]
for p in pairs:
    if not node_dict.has_key(p[0]):
        node_dict[p[0]] = fknode(p[0])
    if not node_dict.has_key(p[1]):
        node_dict[p[1]] = fknode(p[1])
    node_dict[p[0]].add_parent(node_dict[p[1]])

#heads = dict([(n, node_dict[n]) for n in  node_dict if len(node_dict[n].parents) == 0])
def order_heads(node_list):
    heads = [node for node in node_list if len(node.parents) == 0]
    order = []
    while len(heads) > 0:
        head = heads.pop(0)
        order.append(head.name)
        for child in head.children:
            child.parents.remove(head)
            if len(child.parents) == 0:
                heads.append(child)
    return order

order = order_heads(node_dict.values())

#find loops
#pick a node at random and traverse until we get a node we've already seen
def find_loop(node, visited_list = []):
    if node in visited_list:
        return visited_list[visited_list.index(node):]
    else:
        visited_list.append(node)
        for parent in node.parents:
            ret = find_loop(parent, visited_list)
            if ret:
                return ret
            else:
                visited_list.remove(parent)
        return None

non_ordered = [node_dict[n] for n in node_dict if n not in order]
loops = []
for node in non_ordered:
    loop = find_loop(node)
    if loop:
        loops.append([l.name for l in loop])
        for l in loop:
            non_ordered.remove(l)
            for child in l.children:
                child.parents.remove(l)
        new_ordered = order_heads(non_ordered)
        loops = loops + new_ordered



print order
print loops
