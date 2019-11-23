import networkx as nx
from networkx.algorithms import bipartite

subjects = ['a', 'b', 'c']
days = ['m', 'w']

class Tutor:
    def __init__(self, id, subjects, days):
        self.id = id
        self.subjects = subjects
        self.days = days

class Tutee:
    def __init__(self, id, subject, days):
        self.id = id
        self.subject = subject
        self.days = days

tutors_to_match = [
    Tutor(1, ['a', 'b'], ['m', 'w']), Tutor(2, ['b', 'c'], ['w']), Tutor(3, ['c', 'a'], ['m', 'w'])]
tutees_to_match = [
    Tutee(-1, 'a', ['m', 'w']), Tutee(-2, 'b', ['m', 'w']), Tutee(-3, 'c', ['m', 'w'])]

p = nx.Graph()

tutors_on_day = dict((d, [t for t in tutors_to_match if d in t.days]) for d in days)

for t in tutors_to_match:
    p.add_nodes_from(((t.id, d) for d in t.days), subjects=t.subjects, bipartite=0)

for s in tutees_to_match:
    p.add_node(s.id, subject=s.subject)
    for d in s.days:
        for t in tutors_on_day[d]:
            p.add_edge((t.id, d), s.id, weight=0)

print(bipartite.minimum_weight_full_matching(p))