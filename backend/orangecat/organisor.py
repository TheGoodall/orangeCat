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
            if j < len(self.subjects) and self.subjects[j] == allSubjects[i]:
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
    tutorIDIndex = len(tutors) * [0]
    tuteeIDIndex = len(tutees) * [0]
    scoreMat = len(tutors) * [len(tutees) * [0]] #scoreMat[tutorIndex][tuteeIndex] returns the score for this pair and the label explaining the score - is stored as a tuple (score, label)
    for tutor in range(len(tutors)):
        tutorIDIndex[tutor] = tutors[tutor].tutorID
        for tutee in range(len(tutees)):
            tuteeIDIndex[tutee] = tutees[tutee].tuteeID
            scoreMat[tutor][tutee] = s(tutors[tutor], tutees[tutee])

    # convert matrix to a complete bipartite graph
    G = nx.Graph()
    # add nodes - tutors and tutees
    G.add_nodes_from([tutor.tutorID for tutor in tutors], bipartite=0)
    G.add_nodes_from([tutee.tuteeID for tutee in tutees], bipartite=1)
    # add edges - copy across from matrix
    for tutori in range(len(tutorIDIndex)):
        for tuteej in range(len(tuteeIDIndex)):
            G.add_edge(tuteeIDIndex[tuteej], tutorIDIndex[tutori], weight=scoreMat[tutori][tuteej][0], label=scoreMat[tutori][tuteej][1])

    M = bipartite.minimum_weight_full_matching(G)
    return M


tutors_to_match = [
    Tutor("Alfie", ['a', 'b'], [0, 1], ['m', 'w']),
    Tutor("Beth", ['b', 'c'], [0, 1], ['w']),
    Tutor("Ceri", ['c', 'a'], [0, 1], ['m', 'w'])]
tutees_to_match = [
    Tutee("Xena", 'a', 'b', ['m', 'w']),
    Tutee("Yog", 'b', 'c', ['m', 'w']),
    Tutee("Zin", 'c', 'a', ['m', 'w'])]

print(match(tutors_to_match, tutees_to_match))
