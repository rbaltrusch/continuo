# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 16:03:40 2019

@author: Korean_Crimson
"""
import math
from functools import partial

from harmony import get_consonance
from harmony import make_bass_line
from harmony import make_motif
from harmony import make_progression
from postprocessing import get_bass_line_inversions
from postprocessing import smooth_bass_line
from rhythm import octavify


def make_piece_alt(timeline, note_length, scale_len):
    """generate a piece, work in progress"""
    progression = make_progression(number_of_chords=8)
    bass_line = make_bass_line(progression)
    list_of_bass_line_inversions = get_bass_line_inversions(bass_line, smoothness=50000)
    bassline = smooth_bass_line(list_of_bass_line_inversions)
    for i, note in enumerate(bassline):
        note %= scale_len
        root, third, fifth = progression[note].notes
        timeline = octavify(timeline, i, note_length, root.transpose(12), 1)
        timeline = octavify(timeline, i, note_length, third.transpose(12), 0)
        timeline = octavify(timeline, i, note_length, fifth.transpose(12), 0)


def make_piece(time_length, note_length, number_of_layers, scale_len, random_intervals):
    """returns list of lists (containing notes (type double)"""
    motif_length = 24
    layers = []
    current_motifs = []
    length = math.ceil(time_length / (note_length * motif_length))
    for _ in range(length):
        for j in range(number_of_layers):
            if not j:
                motif = smooth_bass_line(
                    get_bass_line_inversions(
                        make_bass_line(make_progression(motif_length)), smoothness=50000
                    )
                )
            else:
                sophistication = 1
                make_motif_func = partial(
                    make_motif,
                    layers,
                    sophistication,
                    scale_len,
                    random_intervals,
                    motif_length,
                )
                motif = get_motif(make_motif_func, layers)
                if not motif in current_motifs:
                    current_motifs.append(motif)

            whole_layer = motif[:motif_length]
            if len(layers) < number_of_layers:
                layers.append(whole_layer)
            else:
                layers[j].extend(whole_layer)
            print(j, whole_layer)
    return layers


def get_motif(make_motif_func, layers):
    """returns list of notes (type double), after determining max consonance motif"""
    poss_motives = []
    consonances = []
    for _ in range(250):
        motif = make_motif_func()
        temp_consonance = 0
        for j, note in enumerate(motif):
            temp_consonance += sum([get_consonance(layer[j], note) for layer in layers])
        temp_consonance /= len(motif) * len(layers) if layers else 1
        poss_motives.append(motif)
        consonances.append(temp_consonance)
    motif = poss_motives[consonances.index(max(consonances))]
    return motif
