# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 15:59:04 2019

@author: Korean_Crimson
"""
import functools
import random
from statistics import mean
from typing import List


def get_consonance(note1: int, note2: int) -> float:
    """returns a measure of consonance (between 0 and 1) of two notes (type double)"""
    diff = abs(note1 - note2) % 7
    consonance_dict = {0: 0.25, 1: -0.25, 2: 1, 3: 0.5, 4: 0.5, 5: 1, 6: -0.25}
    return consonance_dict.get(diff, 0)


def get_next_chord(chord: int) -> int:
    """returns a random choice (double) of the available harmonic follow-ups
    for the given chord (double)"""
    harmony = {
        0: [6, 1, 3],
        1: [4],
        2: [1, 3],
        3: [4],
        4: [0, 5],
        5: [6, 4, 3, 1],
        6: [0, 5],
    }
    return random.choice(harmony[chord])


def make_progression(length: int) -> List[int]:
    """returns a chord progression (list of doubles), starting with 0 and
    ending with 4, i.e. root and fifth, respectively"""
    notes = [0]
    for _ in range(length - 2):
        notes.append(get_next_chord(notes[-1]))
    return notes + [4]


def make_motif(layers, sophistication, scale_len, intervals, motif_length) -> List[int]:
    """returns a motif (list of notes (type double)) based on maximum consonance
    with notes in existing layers"""
    momentums = list(range(-2, 3))
    motif = random.choices(range(scale_len), k=1)
    def get_note_consonance(notes_, note):
        return mean([get_consonance(x, note) for x in notes_])
    for notes in zip(*layers[:motif_length-1]):
        new_notes = [motif[-1] + random.choice(momentums) * random.choice(intervals)
                 for _ in range(sophistication)]
        new_note = max(new_notes, key=functools.partial(get_note_consonance, notes))
        motif.append(new_note)
    return motif
