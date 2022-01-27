# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 16:03:40 2019

@author: Korean_Crimson
"""
import random
from statistics import mean
from typing import List

import harmony


Notes = List[int]

def smooth_bass_line(bass_lines: List[Notes]) -> Notes:
    """Returns the bass line with the least number of leaps in it"""
    return min(bass_lines, key=lambda x: sum(abs(note2 - note1) for note1, note2 in zip(x, x[1:])))

def create_variations(bass_line: Notes, num: int) -> List[Notes]:
    """returns list of lists containing inversions"""
    inversions = [0, 2, 4]
    return [[note + random.choice(inversions) for note in bass_line] for _ in range(num)]

def make_piece(params, scale_len) -> List[Notes]:
    """returns layers of notes"""
    layers: List[Notes] = [[] for _ in range(params.number_of_layers)]
    for _ in range(params.length):
        for j, layer in enumerate(layers):
            if not j:
                motif = smooth_bass_line(
                    create_variations(harmony.make_progression(params.motif_length), num=50000)
                )
            else:
                sophistication = 1
                layers_ = [x[-params.motif_length:] for x in layers]
                motifs = [harmony.make_motif(layers_, sophistication, scale_len,
                                             params.intervals, params.motif_length)
                          for _ in range(250)]
                motif = get_most_consonant_motif(motifs, layers)
            new_motif = motif[:params.motif_length]
            layer.extend(new_motif)
            print(j, new_motif)
    return layers


def get_most_consonant_motif(motifs: List[Notes], layers: List[Notes]) -> Notes:
    """returns list of notes (type double), after determining most consonant motif"""
    return max(motifs, key=lambda x: get_motif_consonance(x, layers))

def get_motif_consonance(motif: Notes, layers: List[Notes]) -> float:
    """Returns the consonance of the motif compared with existing notes in layers"""
    consonances = [mean([harmony.get_consonance(note, new_note) for note in notes])
                        for i, (new_note, *notes) in enumerate(zip(motif, *layers))]
    return mean(consonances) if consonances else 0
