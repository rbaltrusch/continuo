from musical.theory import Note, Scale, Chord
from musical.audio import playback
from random import choice
from timeline import Timeline, Hit #found in timeline.py file

### function definitions

# set global variables
def setglobals():
    global consonance_thr, random_intervals, random_motiflengths, timelength, time, timeline, tempo, timesig, eigth, layer, numberoflayers, transpose_array
    consonance_thr = 10
    numberoflayers = 4
    timelength = 30
    transpose_array = [12, 24, 24, 24, 36, 24, 24, 12, 0]
    #random_intervals = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1,1,1,1,1,1,1,1,1,1,1, 0, 0, 0, 0, 0]
    random_intervals = [0,1,1,2]
    random_motiflengths = [2, 3, 3, 4, 4, 4, 5, 5, 6, 7]
    tempo = 40
    timesig = 4
    eigth = 60/tempo/2
    time = 0.0 # Keep track of currect note placement time in seconds
    timeline = Timeline()
    layer = []

# defines how well two notes fit together when sounding as a chord
def getconsonance(note1, note2):
    if note1 is None or note2 is None: return 1 
    diff = abs(note1 - note2)
    if diff > 6:
        diff -= 7
    if diff == 2 or diff == 5:
        return 1
    elif diff == 3 or diff == 4:
        return 0.25
    elif diff == 0:
        return 0.25
    elif diff == 1 or diff == 6:
        return -0.25
    else:
        return 0 

#give momentum to a motif by forcing it to commit to a certain direction
def getmomentum(momentum,chosenmomentum = 1):
    momentumnumber = 5 #supposed to be 7
    if len(momentum) == 2:
        while len(momentum) < momentumnumber: momentum.append(chosenmomentum) 
    elif len(momentum) > 2:
        if momentum.count(chosenmomentum) > 1: momentum.remove(chosenmomentum)
        else:
            momentum = [1, -1]
            while len(momentum) < momentumnumber: momentum.append(chosenmomentum) 
    if momentum == [0]: momentum = [1, -1]
    #print('momentum', momentum)
    return momentum

#make a motif
def makemotif(layer, progression, timecounter):
    #motiflength = choice(random_motiflengths)
    motiflength = 8 #supposed to be 8
    momentum = [0]
    chosenmomentum = 0
    consonance = 0
    chords = [0,0,-1,-1,-2,-2,-1,-1]
    #chords = [0,0,3,3,4,4,4,4]
    chords = [0,0,2,5,1,4,0,0]

    motif = []
    for c in range(motiflength):
        if len(layer) == 0: notconsonant = False
        else: notconsonant = True
        toobig = True
        toosmall = True
        loopcounter = 0
        solutions = []
        while toobig or toosmall or notconsonant: 
            #if c == 0: motif = choice([0, 2, 4,6])
            momentum = getmomentum(momentum, chosenmomentum)
            chosenmomentum = choice(momentum)
            if len(motif)%2 == 1: note = motif[-1] + chosenmomentum*choice(random_intervals) #all the odd notes are chosen at "random", all even notes are chord notes
            else: 
                chord = chords[c]
                chordnotes = [chord, chord+2, chord+4, chord+6]
                if len(motif)==0: note = choice(chordnotes)
                else:
                    diff=list([(abs((chordnotes[x]-motif[-1]))) for x in range(len(chordnotes))])
                    note=diff[diff.index(min(diff))]
            if note >= 13:
                toobig = True
                continue
            else: 
                toobig = False
            if note < -7:
                toosmall = True
                continue
            else:
                toosmall = False
                if not toobig or not notconsonant: break
            #print(layer[0][c], note)
            tentative_consonance = sum([getconsonance(layer[x][c+timecounter], note) for x in range(len(layer))])/(len(layer))
            #print(tentative_consonance, len(layer))
            #for x in range(len(layer)): print(x)
            solutions.append((note, tentative_consonance))
            if tentative_consonance < consonance_thr:
                notconsonant = True
            else: 
                notconsonant = False
                consonance = sum([getconsonance(layer[x][c], note) for x in range(len(layer))])/(len(layer))
            loopcounter += 1
            if loopcounter > 1000: 
                solutions = [list(t) for t in zip(*solutions)]
                print('maxsolutions ', max(solutions[1]))
                note = solutions[0][solutions[1].index(max(solutions[1]))]
                break                  
        motif.append(note)
    return(motif, motiflength)

def octavify(timeline, time, timecounter, motiflength, root, onoff):
    if onoff == 1:
        timeline.add(time + timecounter*eigth, Hit(root.transpose(-12), eigth/2))
        timeline.add(time + (timecounter+0.5)*eigth, Hit(root, eigth/2))
    elif onoff == 0:
        timeline.add(time + timecounter*eigth, Hit(root.transpose(-12), eigth))
    else:
        print('invalid onoff value')
    return(timeline)

# true if an old motive should be chosen
def decideonmotif(motiflist):
    if not motiflist: return(False) #empty lists are considered boolean false
    goodnumberofmotifs = int((timelength/5))*numberoflayers
    poss_oldmotive = len(motiflist)
    poss_newmotive = goodnumberofmotifs - poss_oldmotive
    possibilities=list([False for x in range(poss_newmotive)] + [True for x in range(poss_oldmotive)])
    #print(possibilities, len(motiflist))
    return(choice(possibilities))
    

# Define key and scale
key = Note('A3')
scale = Scale(key, 'minor')
# Grab progression chords from scale starting at the octave of our key
progression = Chord.progression(scale, base_octave=key.octave)
motiflist = []

setglobals()

overalltimecounter = 0
scalecounter = 0
while overalltimecounter < timelength/eigth:
    scalecounter += 1
    for c in range(numberoflayers):
        timecounter = overalltimecounter
        if not decideonmotif(motiflist):
            motif, motiflength=makemotif(layer, progression, timecounter)
            motiflist.append(motif)
        else:
            notconsonant = True
            temp_consonance = 0
            #print(layer)
            loopcounter = 0
            poss_motives = []
            if c == 0:
                motif = choice(motiflist)
            while notconsonant and c >= 1 and len(layer) == numberoflayers:
                motif = choice(motiflist)
                if motif == layer[any(range(c-1))][-len(motif):-1]:
                    continue
                for counter in range(len(motif)):
                    temp_consonance += sum([getconsonance(layer[x][-len(motif)+counter], motif[counter]) for x in range(c)])/(c)
                temp_consonance /= len(motif)
                poss_motives.append((motif, temp_consonance))
                if temp_consonance/motiflength > consonance_thr:
                    notconsonant = False
                loopcounter += 1
                if loopcounter > 250:
                    poss_motives = [list(t) for t in zip(*poss_motives)]
                    print('maxsolutions motives', max(poss_motives[1]))
                    motif = poss_motives[0][poss_motives[1].index(max(poss_motives[1]))]
                    #motiflist.append(motif)
                    break
        wholelayer = []
        for i in range(1): #no of repetitions
            del wholelayer
            wholelayer = []
            for j in range(motiflength):
                note = motif[j]
                wholelayer.append(note)
                #print(note)
                if note > 6 and note < 13: 
                    note -= 7
                    chord = progression[note]
                    root, third, fifth = chord.notes
                    root = root.transpose(12)
                else:                                
                    chord = progression[note]
                    root, third, fifth = chord.notes        
                timecounter += 1
                #print(timecounter)
                if motif[j] < 0:
                    root = root.transpose(-12)
                if c == 0:
                    timeline = octavify(timeline, time, timecounter, motiflength, root.transpose(transpose_array[c]), 1)
                else: 
                    timeline = octavify(timeline, time+0.25*eigth, timecounter, motiflength, root.transpose(transpose_array[c]), 0) #add +0.25*eigth to time for added effect
            if len(layer) < numberoflayers:
                layer.append(wholelayer)
            else:
                for note in wholelayer:
                    layer[c].append(note)
        print(wholelayer, len(motiflist))

        '''
        #repeat but a fifth above
        for i in range(2):
            for j in range(motiflength):
                timecounter += 1
                chord = progression[wholelayer[j]]
                root, third, fifth = chord.notes
                timeline = octavify(timeline, time, timecounter, motiflength, root.transpose(transpose_array[c]+7), 0)
        '''
    overalltimecounter += abs(overalltimecounter - timecounter)
    print(overalltimecounter)

chord = progression[0]
root, third, fifth = chord.notes
for c in range(2):
    timeline = octavify(timeline, time, timecounter+1, motiflength, root.transpose(0), 0)
    timeline = octavify(timeline, time, timecounter+1,motiflength, root.transpose(12), 0)
    timeline = octavify(timeline, time, timecounter+1, motiflength, third.transpose(24), 0)
    timeline = octavify(timeline, time, timecounter+1, motiflength, fifth.transpose(24), 0)
    timeline = octavify(timeline, time, timecounter+1, motiflength, root.transpose(36), 0)
    timecounter += 1

print("Rendering audio...")

# Reduce volume to 5%

data = timeline.render()

data = data * 0.05

print("Playing audio...")

playback.play(data)

print("Done!")