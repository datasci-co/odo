import os
import networkx as nx

from toolz import pluck
from .convert import convert, ooc_types
from .append import append
from .utils import cls_name


# Edges from Convert
dg = nx.DiGraph()
for a, b in convert.graph.edges():
    cost = convert.graph.edge[a][b]['cost']
    dg.add_edge(cls_name(a), cls_name(b), cost=cost)


# Edges from Append
for a, b in append.funcs:
    if b is not object and a != b:
        dg.add_edge(cls_name(b), cls_name(a))


# Color edges
for n in convert.graph.nodes() + list(pluck(0, append.funcs)):
    if issubclass(n, tuple(ooc_types)):
        dg.node[cls_name(n)]['color'] = 'red'

# Convert to pydot
p = nx.to_pydot(dg)


# Write out as dot
def dot_graph(filename='convert'):
    with open(filename + '.dot', 'w') as f:
        f.write(p.to_string())

    os.system('dot -Tpdf %s.dot -o %s.pdf' % (filename, filename))
    print("Wrote convert graph to %s.pdf" % filename)

if __name__ == '__main__':
    dot_graph()
