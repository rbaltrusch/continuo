from musical.theory import Note, Scale, Chord
from musical.audio import playback
from random import choice
from timeline import Timeline, Hit #found in timeline.py file

### function definitions

# set global variables
def setglobals():
    global consonance_thr, random_intervals_main, intervals_accom, intervals_bass, random_motiflengths, timelength, time, timeline, tempo, timesig, eigth, layer, numberoflayers, transpose_array, scalelen, random_intervals, playback_on
    consonance_thr = 10
    numberoflayers = 3
    timelength = 20
    transpose_array = [0, 12, 24, 24, 36, 24, 24, 12, 0]
    random_intervals_main = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1,1,1,1,1,1,1,1,1,1,1, 0, 0, 0, 0, 0]
    random_intervals = random_intervals_main
    intervals_accom = [0,1,2]
    intervals_bass = [0,1,2,3,4,5,7]
    random_motiflengths = [2, 3, 3, 4, 4, 4, 5, 5, 6, 7]
    tempo = 100
    timesig = 4
    eigth = (60/tempo)/2
    notelengths = [eigth/2, eigth, eigth*2, eigth*4, eigth*8]
    time = 0.0 # Keep track of currect note placement time in seconds
    timeline = Timeline()
    layer = []
    scalelen = 7
    playback_on = True

# defines how well two notes fit together when sounding as a chord
def getconsonance(note1, note2):
    if note1 is None or note2 is None: return 1 
    diff = abs(note1 - note2)
    while diff > 6: diff -= 7
    if diff == 2 or diff == 5:
        return 1
    elif diff == 3 or diff == 4:
        return 0.25
    elif diff == 0:
        return 0
    elif diff == 1 or diff == 6:
        return -0.25
    else:
        print('consonance error has occured')
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

def getnextchord(chord):
    if chord == 0:
        return(choice([6,1,3]))
    elif chord == 2:
        return(choice([1,3]))
    elif chord == 5:
        return(choice([6,4,3,1]))
    elif ([1,3]).count(chord) == 1:
        return(4)
    elif ([4,6]).count(chord) == 1:
        return(choice([0,5]))
    else:
        print('progression error occured')

def makeprogression(numberofchords):
    progression=[0]
    for c in range(numberofchords-1):
        if c != numberofchords-2: progression.append(getnextchord(progression[-1]))
        else: progression.append(4)
    return(progression)

def makebassline(progression, progressiontime):
    bassline=[]
    if progressiontime == len(progression): return(progression)
    elif progressiontime % len(progression) == 0:
        for i in range(len(progression)):
            for j in range(int(progressiontime/len(progression))): bassline.append(progression[i])
    elif progressiontime/len(progression) > 1: 
        leftoverlen = progressiontime - len(progression)
        bassline = progression
        for c in range(leftoverlen): 
            if choice([0,4]) == 0: bassline = [0] + bassline
            else: bassline.append(4)
    else:
        print('progressiontime needs to be larger than progression')
    return(bassline)

def findmissingnote(layer, counter):
    notes = range(scalelen)
    consonances = []
    for note in notes: 
        consonances.append(sum([getconsonance(layer[x][counter], note) for x in range(len(layer))])/(len(layer)))
    return(consonances.index(max(consonances)))

def findchangeinsmoothness(previousnotes, currentnotes, posteriornotes):
    pass

def fixharmony(layer):
    previousnotes=[]
    currentnotes=[]
    for i in range(len(layer[0]),-1):
        posteriornotes=[]
        for j in range(len(layer)): posteriornotes.append(layer[i+1][j])
        print(previousnotes, currentnotes, posteriornotes)
        missingnote=findmissingnote(layer, i)
        if currentnotes.count(missingnote) > 0: continue
        else: pass
        previousnotes=list(currentnotes)
        currentnotes=list(posteriornotes)
        del posteriornotes

#make a motif
def makemotif(layer, progression, timecounter, sophistication):
    #print('making motif')
    #motiflength = choice(random_motiflengths)
    motiflength = 8 #supposed to be 8
    momentum = [0]
    chosenmomentum = 0
    consonance = 0
    #chords = [0,0,-1,-1,-2,-2,-1,-1]
    #chords = [0,0,3,3,4,4,4,4]
    #chords = [0,0,2,5,1,4,0,0]
    #chords = [0,0,0,0,4,4,4,4]
    chords = progression 

    motif = []
    for c in range(motiflength):
        if len(layer) == 0: notconsonant = False
        else: notconsonant = True
        toobig = True
        toosmall = True
        loopcounter = 0
        solutions = []
        while toobig or toosmall or notconsonant: 
            if c == 0: motif.append(choice([0, 2, 4]))
            momentum = getmomentum(momentum, chosenmomentum)
            chosenmomentum = choice(momentum)
            note = motif[-1] + chosenmomentum*choice(random_intervals)
            
            '''
            if len(motif)%2 == 1: note = motif[-1] + chosenmomentum*choice(random_intervals) #all the odd notes are chosen at "random", all even notes are chord notes
            else: 
                chord = chords[c]
                chordnotes = [chord, chord+2, chord+4]
                if len(motif)==0: note = choice(chordnotes)
                else:
                    diff=list([(abs((chordnotes[x]-motif[-1]))) for x in range(len(chordnotes))])
                    note=diff[diff.index(min(diff))]
            '''
            
            if note >= (2*scalelen)-1:
                toobig = True
                continue
            else: 
                toobig = False
            if note < -scalelen:
                toosmall = True
                continue
            else:
                toosmall = False
                #print('hello0', notconsonant)
                if not toobig and not notconsonant: break
            #print('hello1')
            min_len = min(len(layer[x]) for x in range(len(layer)))
            for l in layer: 
                if len(l) == min_len: 
                    index_min=layer.index(l)
                    break 
            #print(index_min, len(layer))
            #print(c+timecounter, len(layer[-1]))
            tentative_consonance = sum([getconsonance(layer[x][c+timecounter], note) for x in range(index_min)])/(len(layer))
            solutions.append((note, tentative_consonance))
            if tentative_consonance < consonance_thr:
                notconsonant = True
            else: 
                notconsonant = False
                consonance = sum([getconsonance(layer[x][c+timecounter], note) for x in range(len(layer))])/(len(layer))
            loopcounter += 1
            if loopcounter > sophistication: 
                solutions = [list(t) for t in zip(*solutions)]
                #print('maxsolutions ', max(solutions[1]))
                note = solutions[0][solutions[1].index(max(solutions[1]))]
                break                  
        motif.append(note)
    return(motif, motiflength)

def octavify(timeline, time, timecounter, root, onoff):
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
    #goodnumberofmotifs = int((timelength/4))*numberoflayers
    goodnumberofmotifs = 10000
    poss_oldmotive = len(motiflist)
    poss_newmotive = goodnumberofmotifs - poss_oldmotive
    possibilities=list([False for x in range(poss_newmotive)] + [True for x in range(poss_oldmotive)])
    #print(possibilities, len(motiflist))
    return(choice(possibilities))

def smoothbassline(bassline, progression, smoothness): #smoothness is the counter of how long we let the program search for a smooth bassline
    listofbasslines=[]
    inversions = [0,2,4]
    for counter in range(smoothness): 
        newbassline = []
        for note in bassline:
            note += choice(inversions)
            newbassline.append(note)
        listofbasslines.append(newbassline)
        del newbassline
    
    listofdifferences = []
    for bassline in listofbasslines:
        difference = 0
        for i in range(len(bassline)-1):
            difference += abs(bassline[i+1] - bassline[i])
        listofdifferences.append(difference)
        del difference 
    min_index = listofdifferences.index(min(listofdifferences))
    smoothbassline = listofbasslines[min_index]
    return smoothbassline          

# Define key and scale
key = Note('A3')
scale = Scale(key, 'harmonicminor')
# Grab progression chords from scale starting at the octave of our key
progression = Chord.progression(scale, base_octave=key.octave)
p = progression
motiflist = []

setglobals()

'''
overalltimecounter = 0
for c in range(1):
    progression=makeprogression(8)
    print(progression)
    bassline=makebassline(progression, len(progression)*2)
    print(bassline)
    bassline = smoothbassline(bassline, progression, 50000)
    print(bassline)
    timecounter = overalltimecounter
    for note in bassline:
        if note > 6: note-= scalelen
        elif note < 0: note+= scalelen
        chord = p[note]
        root, third, fifth = chord.notes
        timeline = octavify(timeline, time, timecounter, root.transpose(12), 1)
        timeline = octavify(timeline, time, timecounter, third.transpose(12), 0)
        timeline = octavify(timeline, time, timecounter, fifth.transpose(12), 0)
        timecounter += 1
    overalltimecounter = timecounter


data = timeline.render()
data = 0.05*data
playback.play(data)
'''

overalltimecounter = 0
scalecounter = 0
while overalltimecounter < timelength/eigth:
    scalecounter += 1
    currentmotifs = []
    for c in range(numberoflayers):
        timecounter = overalltimecounter
        if c == 0:
            progression=makeprogression(8)
            motiflength=len(progression)
            bassline=makebassline(progression, motiflength)
            bassline = smoothbassline(bassline, progression, 50000)
            motif = bassline
        else: 
            if not decideonmotif(motiflist):
                motif, motiflength=makemotif(layer, progression, timecounter, 10000)
                motiflist.append(motif)
            else:
                currentmotif = True
                notconsonant = True
                temp_consonance = 0
                #print(layer)
                loopcounter = 0
                poss_motives = []
                if c == 0:
                    while currentmotif: 
                        motif = choice(motiflist) 
                        if currentmotifs.count(motif) == 0: currentmotif = False
                while notconsonant and c >= 1 and len(layer) == numberoflayers:
                    while currentmotif: 
                        motif = choice(motiflist) 
                        if currentmotifs.count(motif) == 0: currentmotif = False
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
        currentmotifs.append(motif)
        wholelayer = []
        for i in range(1): #no of repetitions
            del wholelayer
            wholelayer = []
            for j in range(motiflength):
                #print(j, motiflength, len(motif))
                note = motif[j]
                wholelayer.append(note)
                #print(note)
                timecounter += 1
                '''
                if note > scalelen-1 and note < (2*scalelen)-1: 
                    note -= scalelen
                    chord = p[note]
                    root, third, fifth = chord.notes
                    root = root.transpose(12)
                else:                                
                    chord = p[note]
                    root, third, fifth = chord.notes        
                #print(timecounter)
                if motif[j] < 0:
                    root = root.transpose(-12)
                if c == 0:
                    timeline = octavify(timeline, time, timecounter, root.transpose(transpose_array[c]), 1)
                else: 
                    timeline = octavify(timeline, time+0.25*eigth, timecounter, root.transpose(transpose_array[c]), 1) #add +0.25*eigth to time for added effect
                '''
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
                timeline = octavify(timeline, time, timecounter, root.transpose(transpose_array[c]+7), 0)
        '''
    del currentmotifs
    overalltimecounter += abs(overalltimecounter - timecounter)
    print(overalltimecounter)

for layer0 in layer: #layer0 is a single layer
    timecounter=0
    for note in layer0:
        if note > scalelen-1 and note < (2*scalelen)-1: 
            note -= scalelen
            chord = p[note]
            root, third, fifth = chord.notes
            root = root.transpose(12)
        else:                                
            chord = p[note]
            root, third, fifth = chord.notes 
        root, third, fifth = chord.notes
        if layer.index(layer0)==0: timeline = octavify(timeline, time, timecounter, root.transpose(transpose_array[layer.index(layer0)]), 1)
        else: timeline = octavify(timeline, time+0.25*eigth, timecounter, root.transpose(transpose_array[layer.index(layer0)]), 1)
        timecounter+=1
        

chord = p[0]
root, third, fifth = chord.notes
for c in range(2):
    timeline = octavify(timeline, time, timecounter+1, root.transpose(0), 0)
    timeline = octavify(timeline, time, timecounter+1, root.transpose(12), 0)
    timeline = octavify(timeline, time, timecounter+1, third.transpose(24), 0)
    timeline = octavify(timeline, time, timecounter+1, fifth.transpose(24), 0)
    timeline = octavify(timeline, time, timecounter+1, root.transpose(36), 0)
    timecounter += 1

print("Rendering audio...")

# Reduce volume to 5%

data = timeline.render()

data = data * 0.05

print("Playing audio...")

if playback_on: playback.play(data)

print("Done!")