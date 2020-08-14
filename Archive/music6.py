###file imports
from main import *

def getconsonance(note1, note2):
    if note1 is None or note2 is None: return 1 
    diff = abs(note1 - note2)
    while diff > 6: diff -= 7
    if diff == 2 or diff == 5:
        return 1
    elif diff == 3 or diff == 4:
        return 0.5
    elif diff == 0:
        return 0.25
    elif diff == 1 or diff == 6:
        return -0.25
    else:
        print('consonance error has occured')
        return 0 

#give momentum to a motif by forcing it to commit to a certain direction
def getmomentum(momentum,chosenmomentum = 1):
    momentumnumber = 7 #supposed to be 7
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

def norm(note): #normalise note that is outside scalelen for functions that need it between 0 to scalelen format
    while note>=scalelen: note-=scalelen 
    return note

def findminchangeinsmoothness(previousnotes, currentnotes, posteriornotes, missingnote):
    diff = []
    difflist = []
    for i in range(len(previousnotes)):
        if len(previousnotes) > 0: diff.append(norm(abs(previousnotes[i]-missingnote)))
        if len(posteriornotes) > 0: diff.append(norm(abs(posteriornotes[i]-missingnote)))
        difflist.append(sum(diff)/len(diff))
    if len(difflist)>0: layerindex=difflist.index(min(difflist))
    else: layerindex = 0
    changednote=missingnote
    return changednote, layerindex

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
                #consonance = sum([getconsonance(layer[x][c+timecounter], note) for x in range(len(layer))])/(len(layer))
                consonance = solutions[-1]
            loopcounter += 1
            if loopcounter > sophistication: 
                solutions = [list(t) for t in zip(*solutions)]
                #print('maxsolutions ', max(solutions[1]))
                note = solutions[0][solutions[1].index(max(solutions[1]))]
                break                  
        motif.append(note)
    return(motif, motiflength)

# true if an old motive should be chosen
def decideonmotif(motiflist):
    if not motiflist: return(False) #empty lists are considered boolean false
    goodnumberofmotifs = int((timelength/4))*numberoflayers
    #goodnumberofmotifs = 10000
    poss_oldmotive = len(motiflist)
    poss_newmotive = goodnumberofmotifs - poss_oldmotive
    possibilities=list([False for x in range(poss_newmotive)] + [True for x in range(poss_oldmotive)])
    #print(possibilities, len(motiflist))
    return(choice(possibilities))

   

def convertdb(db):
    return(10**(db/10))



def makepiece_alt():
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

def makepiece():
    timecounter = 0
    overalltimecounter = 0
    scalecounter = 0
    while overalltimecounter < timelength/eigth and load!="y":
        scalecounter += 1
        currentmotifs = []
        for c in range(numberoflayers):
            timecounter = overalltimecounter
            if c == 0:
                progression=makeprogression(8)
                motiflength=len(progression)
                #print("lenprogression", len(progression))
                bassline=makebassline(progression, motiflength)
                bassline = smoothbassline(bassline, progression, 50000)
                motif = bassline
            else: 
                if not decideonmotif(motiflist):
                    motif, motiflength=makemotif(layer, progression, timecounter, 10000)
                    #print("motiflength", motiflength)
                    motiflist.append(motif)
                else:
                    #print("hello else else")
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
                        #print("in while loop", notconsonant, c, len(layer))
                        while currentmotif: 
                            #print("in while while loop")
                            whilecounter=0
                            whileflag=True
                            while len(motif)>maxmotiflength and whilecounter<100: 
                                whileflag=False
                                #print(len(motiflist), whilecounter)
                                motif = choice(motiflist) 
                                whilecounter+=1
                                if whilecounter>=100: whileflag = True
                            if whileflag:
                                motif, motiflength=makemotif(layer, progression, timecounter, 1)
                                #print('hello from motifmaking in while')
                                #print(currentmotifs.count(motif))
                            if currentmotifs.count(motif) == 0: currentmotif = False
                        #print(len(motif))
                        if motif == layer[any(range(c-1))][-len(motif):-1]:
                            #print('hello from continue 1')
                            continue
                        if len(motif)>maxmotiflength:
                            #print('hello from continue 2', len(motif))
                            #currentmotif=True 
                            continue 
                        for counter in range(len(motif)):
                            #print(len(motif)-1, c-1, len(layer))
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
                    note = motif[j]
                    wholelayer.append(note)
                    timecounter += 1
                if len(layer) < numberoflayers:
                    layer.append(wholelayer)
                else:
                    for note in wholelayer:
                        layer[c].append(note)
            print(wholelayer, len(motiflist))
    
            ###
            #repeat but a fifth above
            for i in range(2):
                for j in range(motiflength):
                    timecounter += 1
                    chord = progression[wholelayer[j]]
                    root, third, fifth = chord.notes
                    timeline = octavify(timeline, time, timecounter, root.transpose(transpose_array[c]+7), 0)
            ###
        del currentmotifs
        overalltimecounter += abs(overalltimecounter - timecounter)
        print(overalltimecounter)











