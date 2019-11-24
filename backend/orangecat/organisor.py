import math
import random
import networkx as nx
from networkx.algorithms import bipartite

class Tutor:
    def __init__(self, tutorID, subjects, prefs, days):
        #every tutor as a unique id
        self.tutorID = "tutor" + str(tutorID)
        self.subjects = subjects
        self.prefs = prefs
        self.subPrefs = []
        for i in range(len(subjects)):
            self.subPrefs.append((subjects[i], prefs[i]))
        self.days = days

class Tutee:
    def __init__(self, tuteeID, subjects, days):
        self.tuteeID = "tutee" + str(tuteeID)
        self.subjects = subjects # an ordered list. subjects[0] is the favourite option
        self.days = days

# s takes as inputs: one tutor object, one tutee object and returns as output: a tuple ->(one positive float or infinity marking the suitability of pairing the two
# a lower value shows better compatability, reason for score)
def s(tutor, tutee):
    impossible = True # remains True if no matching days for this pair
    for d in tutor.days:
        if d in tutee.days:
            impossible = False


    # TWEAKABLE VARIABLE ALERT
    alpha = 1.5     # a coefficient that generates preference for tutees getting their first preference
    # Don't forget that this can be tweaked

    
    if impossible:
        return (math.inf, "days")
    else:
        prefs = []
        subs = []
        for i in range(len(tutee.subjects)):
            
            if not tutee.subjects[i] in tutor.subjects:
                prefs.append(math.inf)
            else:
                ind = tutor.subjects.index(tutee.subjects[i])
                prefs.append((alpha ** i) * tutor.subPrefs[ind][1])
            subs.append(tutee.subjects[i])
        
        bestPref = min(prefs)
        return (bestPref, subs[prefs.index(bestPref)])

# match takes a list of tutors and tutees and returns the best possible matching
def match(tutors, tutees):
    tutDict = {}
    for tutor in tutors:
        tutDict[tutor.tutorID] = tutor
    for tutee in tutees:
        tutDict[tutee.tuteeID] = tutee
    
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

    #remove duplicate dict data
    for tutee in tutees:
        M.pop(tutee.tuteeID, None)
    #remove any infinite edges
    ok = True
    for key in M:
        if G.get_edge_data(key, M[key])['weight'] == math.inf:
            ok = False
            M.pop(key)
    
    matchableTutors = [tutor for tutor in tutors if tutor.tutorID in M]
    matchableTutees = [tutee for tutee in tutees if tutee.tuteeID in M.values()]

    # if not ok we need to call repeat on a subset of tutors and tutees
    if not ok:
        return match(matchableTutors, matchableTutees)

    tts = []    #tutor, tutee, subject
    print("")
    for key in M:
        subject = G.get_edge_data(key, M[key])['label']
        print(subject)
        print(tutDict[M[key]].tuteeID)
        print(tutDict[M[key]].subjects)
        tts.append([tutDict[key], tutDict[M[key]], subject])

    days = {'misc': 0}
    table = []

    # if only one day is an option then trivially assign pair to that time slot - we then balance the rest accordingly    
    i = 0
    while i < len(tts):
        pairDays = []
        for d in tts[i][0].days:
            if d in tts[i][1].days:
                pairDays.append(d)
        if len(pairDays) == 1:
            day = pairDays[0]
            if day in days:
                days[day] += 1
            else:
                days[day] = 1
            tts[i].append(d)
            table.append(tts.pop(i))
        else:
            tts[i].append(pairDays)
            i += 1

    overlap = lambda xs, ys: [x for x in xs if x in ys]
    pick = lambda xs: random.choice(xs)

    # if any remaining pairs can be grouped with the trivial groupings then do so
    i = 0
    while i < len(tts):
        pair = tts[i]
        pair.append(overlap(pair[3], days))
        if len(pair[4]) == 0:
            pair[4] = 'misc'
            i += 1
        else:
            pair[3] = pick(pair[4])
            table.append(tts.pop(i)[:4])

    # deal with outliers
    i = 0
    while i < len(tts):
        pair = tts[i]
        pair[3] = pick(pair[3])
        table.append(tts.pop(i)[:4])
    
    
    return table


tutors_to_match = [
    Tutor("Alfie", ['a', 'b'], [0, 1], ['m', 'w']),
    Tutor("Beth", ['b', 'c'], [0, 1], ['w']),
    Tutor("Ceri", ['c', 'a'], [0, 1], ['m', 'w'])]
tutees_to_match = [
    Tutee("Xena", ['a', 'b'], ['m', 'w']),
    Tutee("Yog", ['b', 'c'], ['m', 'w']),
    Tutee("Zin", ['c', 'a'], ['m', 'w'])]

match_table = match(tutors_to_match, tutees_to_match)
for row in match_table:
    print("{} matched with {} for {} at {}".format(row[0].tutorID, row[1].tuteeID, row[2], row[3]))
