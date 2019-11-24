import math
import networkx as nx
from networkx.algorithms import bipartite

allSubjects = ['a', 'b', 'c']
allDays = ['m', 'w']

class Tutor:
    def __init__(self, tutorID, subjects, prefs, days):
        #every tutor as a unique id
        self.tutorID = tutorID
        self.subjects = sorted(subjects)
        self.prefs = prefs
        self.subPrefs = []
        i, j = 0, 0
        while i < len(allSubjects):
            if self.subjects[j] == allSubjects[i]:
                #if the tutor is willing to teach this subject store the associated value in a tuple
                self.subPrefs.append((allSubjects[i], prefs[j]))
                j += 1
            else:
                #else note that the tutor will not teach the subject by assigning infinity in the tuple
                self.subPrefs.append((allSubjects[i], math.inf))
            i += 1
        self.days = days

class Tutee:
    def __init__(self, tuteeID, subject1, subject2, days):
        self.tuteeID = tuteeID
        self.subject1 = subject1
        self.subject2 = subject2
        self.days = days

# s takes as inputs: one tutor object, one tutee object and returns as output: a tuple ->(one positive float or infinity marking the suitability of pairing the two
# a lower value shows better compatability, reason for score)
def s(tutor, tutee):
    impossible = True # remains True if no matching days for this pair
    for d in tutor.days:
        if d in tutee.days:
            impossible = False

    alpha = 1.5     # a coefficient that generates preference for tutees getting their first preference

    if impossible:
        return (math.inf, "days")
    else:
        firstPref = tutor.subPrefs[allSubjects.index(tutee.subject1)][1]
        secondPref = alpha * tutor.subPrefs[allSubjects.index(tutee.subject2)][1]
        if firstPref <= secondPref:
            return (firstPref, "first")
        else:
            return (secondPref, "second")

# match takes a list of tutors and tutees and returns the best possible matching
def match(tutors, tutees):
    scoreMat = [len(tutors)][len(tutees)] #scoreMat[tutorIndex][tuteeIndex] returns the score for this pair and the label explaining the score - is stored as a tuple (score, label)
    for tutor in range(len(tutors)):
        for tutee in range(len(tutees)):
            scoreMat[tutor][tutee] = s(tutors[tutor], tutees[tutee])

    # convert matrix to a complete bipartite graph
    G = nx.Graph()
    # add nodes - tutors and tutees
    G.add_nodes_from([tutor.tutorID for tutor in tutors], bipartite=0)
    G.add_nodes_from([tutee.tuteeID for tutee in tutees], bipartite=1)
    # add edges - copy across from matrix
    for 

'''
tutors_to_match = [
    Tutor(1, ['a', 'b'], ['m', 'w']),
    Tutor(2, ['b', 'c'], ['w']),
    Tutor(3, ['c', 'a'], ['m', 'w'])]
tutees_to_match = [
    Tutee(-1, 'a', 'b', ['m', 'w']),
    Tutee(-2, 'b', 'c', ['m', 'w']),
    Tutee(-3, 'c', 'a', ['m', 'w'])]

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
'''
