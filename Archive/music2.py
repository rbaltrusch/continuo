from musical.theory import Note, Scale, Chord
from musical.audio import playback
from random import choice
from timeline import Timeline, Hit #found in timeline.py file

### function definitions

# set global variables
def setglobals():
    global consonance_thr, random_intervals, random_motiflengths, timelength, time, timeline, tempo, timesig, eigth, layer
    consonance_thr = 0.6
    random_intervals = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0]
    random_motiflengths = [2, 3, 3, 4, 4, 4, 5, 5, 6, 7]
    tempo = 120
    timesig = 4
    eigth = 60/tempo/2
    timelength = 30
    time = 0.0 # Keep track of currect note placement time in seconds
    timeline = Timeline()
    layer = []

# defines how well two notes fit together when sounding as a chord
def getconsonance(note1, note2):
    if note2 == None: return 1 
    diff = abs(note1 - note2)
    if diff == 2 or diff == 5:
        return 1
    elif diff == 0 or diff == 3 or diff == 4:
        return 0.5
    elif diff == 1 or diff == 6:
        return 0
    else:
        return 0 

#give momentum to a motif by forcing it to commit to a certain direction
def getmomentum(momentum,chosenmomentum = 1):
    if len(momentum) == 2:
        while len(momentum) < 7: momentum.append(chosenmomentum)
    elif len(momentum) > 2:
        if momentum.count(chosenmomentum) > 1: momentum.remove(chosenmomentum)
        else:
            momentum = [1, -1]
            while len(momentum) < 7: momentum.append(chosenmomentum)
    if momentum == [0]: momentum = [1, -1]
    print('momentum', momentum)
    return momentum

#make a motif
def makemotif(layer):
    motiflength = choice(random_motiflengths)
    startnote = choice([0, 2, 4])
    motif = [startnote]
    momentum = [0]
    chosenmomentum = 0
    consonance = 0

    for c in range(motiflength-1):
        if len(layer) == 0: notconsonant = False
        else: notconsonant = True
        toobig = True
        while toobig or notconsonant: 
            momentum = getmomentum(momentum, chosenmomentum)
            chosenmomentum = choice(momentum)
            note = startnote + chosenmomentum*choice(random_intervals)
            if note > 6:
                toobig = True
            else: 
                toobig = False
                print('hello1')
                if not notconsonant: break 
            print(consonance,' 1')
            #if (lambda consonance: for i in range(len(layer)): consonance =+ getconsonance(layer[i][c], note)) < consonance_thr*len(layer):
            #if sum(list(map(getconsonance(layer[x][c], note), range(len(layer))))) < consonance_thr*len(layer):
            if sum([getconsonance(layer[x][c], note) for x in range(len(layer))])/len(layer) < consonance_thr:
                notconsonant = True
                print(consonance,' 2')
            else: 
                notconsonant = False
                consonance = sum([getconsonance(layer[x][c], note) for x in range(len(layer))])/len(layer)
                print(consonance,' 3') 
        print('hello2')                   
        motif.append(note)
    return(motif, motiflength)

def octavify(timeline, time, timecounter, motiflength, onoff):
    if onoff == 1:
        timeline.add(time + timecounter*eigth, Hit(root.transpose(-12), eighth/2))
        timeline.add(time + (timecounter+0.5)*eigth, Hit(root, eigth/2))
    elif onoff == 0:
        timeline.add(time + timecounter*eigth, Hit(root.transpose(-12), eigth))
    else:
        print('invalid onoff value')
    return(timeline)

# Define key and scale
key = Note('D3')
scale = Scale(key, 'minor')
# Grab progression chords from scale starting at the octave of our key
progression = Chord.progression(scale, base_octave=key.octave)
motiflist = []

setglobals()

### layer 1 
motif, motiflength=makemotif(layer)
motiflist.append(motif)
timecounter = 0
wholelayer = []
c = 0
for i in range(5):
    del wholelayer
    wholelayer = []
    for j in range(motiflength):
        note = motif[j]
        wholelayer.append(note)
        print(note)
        chord = progression[note]
        root, third, fifth = chord.notes
        timecounter += 1
        if motif[j] < 0:
            root = root.transpose(-12)
        timeline = octavify(timeline, time, timecounter, motiflength, 0)
    layer.append(wholelayer)


### layer 2

'''
#motiflength = choice(random_motiflengths)
motiflength = len(layer[0])
startnote = choice([0, 2, 4])
timecounter = 0
motif = [startnote]
print(layer)
print(layer[0])
momentum = [0]
chosenmomentum = 0

consonance = 0
for c in range(1,len(layer[0])):
    toobig = True
    notconsonant = True
    while toobig or notconsonant:
        momentum = getmomentum(momentum, chosenmomentum)
        chosenmomentum = choice(momentum)
        note = startnote + chosenmomentum*choice(random_intervals)
        if note > 6:
            toobig = True
        else: 
            toobig = False
        if (consonance + getconsonance(layer[0][c], note))/c < consonance_thr:
            notconsonant = True
        else:
            notconsonant = False
            consonance += getconsonance(layer[0][c], note)
    motif.append(note)
'''

motif, motiflength=makemotif(layer)

c = 1
for i in range(5):
    del wholelayer
    wholelayer = []
    for j in range(motiflength):
        note = motif[j]
        wholelayer.append(note)
        print(note)
        chord = progression[note]
        root, third, fifth = chord.notes
        timecounter += 1
        if motif[j] < 0:
            root = root.transpose(-12)
        #timeline.add(time + timecounter/motiflength, Hit(root.transpose(24), 1.0/motiflength))
        timeline.add(time + timecounter*eigth, Hit(root.transpose(24), eigth))
    layer.append(wholelayer)


### layer 3

#motiflength = choice(random_motiflengths)
motiflength = len(layer[0])
startnote = choice([0, 2, 4])
timecounter = 0
motif = [startnote]
print(layer)
print(layer[0])
momentum = [0]
chosenmomentum = 0

consonance = 0
for c in range(1,len(layer[0])):
    toobig = True
    notconsonant = True
    while toobig or notconsonant:
        momentum = getmomentum(momentum, chosenmomentum)
        chosenmomentum = choice(momentum)
        note = startnote + chosenmomentum*choice(random_intervals)
        if note > 6:
            toobig = True
        else: 
            toobig = False
        if (consonance + getconsonance(layer[0][c], note) + getconsonance(layer[1][c],note))/c < consonance_thr:
            notconsonant = True
        else:
            notconsonant = False
            consonance += getconsonance(layer[0][c], note) + getconsonance(layer[1][c], note)
    motif.append(note)

c = 2
for i in range(5):
    del wholelayer
    wholelayer = []
    for j in range(motiflength):
        note = motif[j]
        wholelayer.append(note)
        print(note)
        chord = progression[note]
        root, third, fifth = chord.notes
        timecounter += 1
        if motif[j] < 0:
            root = root.transpose(-12)
        timeline.add(time + timecounter*eigth, Hit(root.transpose(12), eigth))
        #timeline.add(time + timecounter/motiflength, Hit(third.transpose(12), 1.0/motiflength))
    layer.append(wholelayer)


### layer 4

#motiflength = choice(random_motiflengths)
motiflength = len(layer[0])
startnote = choice([0, 2, 4])
timecounter = 0
motif = [startnote]
print(layer)
print(layer[0])
momentum = [0]
chosenmomentum = 0

consonance = 0
for c in range(1,len(layer[0])):
    toobig = True
    notconsonant = True
    while toobig or notconsonant:
        momentum = getmomentum(momentum, chosenmomentum)
        chosenmomentum = choice(momentum)
        note = startnote + chosenmomentum*choice(random_intervals)
        if note > 6:
            toobig = True
        else: 
            toobig = False
        if (consonance + getconsonance(layer[0][c], note) + getconsonance(layer[1][c],note) + getconsonance(layer[2][c],note))/c < consonance_thr:
            notconsonant = True
        else:
            notconsonant = False
            consonance += getconsonance(layer[0][c], note) + getconsonance(layer[1][c], note) + getconsonance(layer[2][c],note)
    motif.append(note)

c = 3
for i in range(5):
    del wholelayer
    wholelayer = []
    for j in range(motiflength):
        note = motif[j]
        wholelayer.append(note)
        print(note)
        chord = progression[note]
        root, third, fifth = chord.notes
        timecounter += 1
        if motif[j] < 0:
            root = root.transpose(-12)
        timeline.add(time + timecounter*eigth, Hit(root.transpose(24), eigth))
    layer.append(wholelayer)


print("Rendering audio...")

# Reduce volume to 5%

data = timeline.render()

data = data * 0.05

print("Playing audio...")

playback.play(data)

print("Done!")