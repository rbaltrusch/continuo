# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 15:59:04 2019

@author: Korean_Crimson
"""
from random import choice

def get_consonance(note1, note2):
    '''returns a measure of consonance (between 0 and 1) of two notes (type double)'''
    consonance_value = 0
    if isinstance(note1, int) and isinstance(note2, int):
        diff = abs(note1 - note2) % 7
        consonance_dict = {0: 0.25, 1: -0.25, 2: 1, 3: 0.5, 4: 0.5, 5: 1, 6: -0.25}
        if diff in consonance_dict.keys():
            consonance_value = consonance_dict[diff]
    return consonance_value

def get_momentum(momentums, chosen_momentum=1, momentum_number=7):
    '''give momentum to a motif by forcing it to commit to a certain direction.
    This is not rhythmic momentum but note momentum, i.e. in which direction
    the motif will go (to shape the motif)'''
    if len(momentums) > 2 and momentums.count(chosen_momentum) > 1:
        momentums.remove(chosen_momentum)
    else:
        momentums = [1, -1] if not len(momentums) == 2 else momentums
        momentums.extend([chosen_momentum] * (momentum_number - len(momentums)))
    return momentums

def get_next_chord(chord):
    '''returns a random choice (double) of the available harmonic follow-ups
    for the given chord (double)'''
    harmony = {0: [6, 1, 3], 1: [4], 2: [1, 3], 3: [4], 4: [0, 5], 5: [6, 4, 3, 1], 6: [0, 5]}
    return choice(harmony[chord])

def make_progression(number_of_chords):
    '''returns a chord progression (list of doubles), starting with 0 and
    ending with 4, i.e. root and fifth, respectively'''
    progression = [0]
    for _ in range(number_of_chords - 2):
        progression.append(get_next_chord(progression[-1]))
    progression.append(4)
    return progression

def make_bass_line_alt(progression, progression_time):
    '''alternative way of making baseline for a given progression (list of notes)
    .Returns list of notes (double). Progression_time is how many notes should
    be in the bass line'''
    bass_line = []
    if progression_time == len(progression):
        bass_line = progression
    elif not progression_time % len(progression):
        for note in progression:
            for _ in range(int(progression_time / len(progression))):
                bass_line.append(note)
    elif progression_time / len(progression) > 1:
        leftover_len = progression_time - len(progression)
        bass_line = progression
        for _ in range(leftover_len):
            if not choice([0, 4]):
                bass_line.insert(0, 0)
            else:
                bass_line.append(4)
    else:
        print('progression_time needs to be larger than progression')
    return bass_line

def make_bass_line(progression):
    ''' dummy bass line'''
    return progression

def find_missing_note(layer, counter, scale_len):
    '''returns note (double) with the highest consonance'''
    consonances = []
    for note in range(scale_len):
        consonances.append(sum([get_consonance(note_, note) for note_ in layer]) / (len(layer)))
    return consonances.index(max(consonances))

def find_min_change_in_smoothness(previous_notes, posterior_notes, missing_note, scale_len):
    '''returns index of the layer in which the missing note would create the
    minimum change in smoothness of voice leading'''
    diff = [abs(note - missing_note) % scale_len for note in previous_notes + posterior_notes]
    difflist = sum(diff) / len(diff)
    layer_index = difflist.index(min(difflist)) if difflist else 0
    return layer_index

def make_motif(layers, time_counter, sophistication, scale_len, random_intervals, motif_length):
    '''returns a motif (list of notes (type double)) based on maximum consonance
    with notes in existing layers'''
    momentums = [0]
    chosen_momentum = 0
    motif = [choice(range(scale_len))]
    for i in range(motif_length - 1):
        notes = []
        tentative_consonances = []
        for _ in range(sophistication):
            momentums = get_momentum(momentums, chosen_momentum)
            chosen_momentum = choice(momentums)
            tentative_note = motif[-1] + chosen_momentum * choice(random_intervals)

            consonances = [get_consonance(layer[i - motif_length], tentative_note) for layer in layers]
            tentative_consonance = sum(consonances) / (len(layers)) if layers else 0
            tentative_consonances.append(tentative_consonance)
            notes.append(tentative_note)
        max_consonance_index = tentative_consonances.index(max(tentative_consonances))
        motif.append(notes[max_consonance_index])
    return motif

def decide_on_motif(motif_list, time_length, number_of_layers):
    '''true if an old motive should be chosen'''
    if motif_list:
        good_number_of_motifs = int((time_length / 4)) * number_of_layers
        poss_new_motifs = good_number_of_motifs - len(motif_list)
        possibilities = [False for x in range(poss_new_motifs)] + [True for x, _ in enumerate(motif_list)]
        make_new_motif_flag = (choice(possibilities))
    else:
        make_new_motif_flag = False
    return make_new_motif_flag

def convert_from_db(num_db):
    '''converts DB to decimal'''
    return 10 ** (num_db / 10)
