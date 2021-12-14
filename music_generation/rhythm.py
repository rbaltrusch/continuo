# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 16:07:02 2019

@author: Korean_Crimson
"""
from random import choice

import timeline


def make_rhythm(layer, note_lengths):
    """layer is a list of notes."""
    momentums = []
    prev_note_length_i = -3
    note_lengths_prob = choose_note_lengths(note_lengths)
    for _ in layer:
        momentums = get_rhythmic_momentum(momentums)
        new_note_length = get_note_length(
            momentums, prev_note_length_i, note_lengths_prob, note_lengths
        )
        note_lengths.append(new_note_length)
        prev_note_length_i = note_lengths.index(note_lengths[-1])
    return note_lengths


def get_note_length(momentums, prev_note_length_i, note_lengths_prob, note_lengths):
    """return note length randomly based on rhytyhmic momentum"""
    momentum = -3 if prev_note_length_i == -3 else choice(momentums)
    if momentum in [-1, 0, 1]:
        momentum = len(note_lengths) - prev_note_length_i
        index = prev_note_length_i + momentum
        index = index if index < len(note_lengths) else -1
        note_length = note_lengths[index]
    elif momentum == -3:
        note_length = choice(note_lengths_prob)
    else:
        note_length = choice(note_lengths)
    return note_length


def choose_note_lengths(note_lengths):
    """returns list"""
    return [choice(note_lengths) for i, _ in enumerate(note_lengths) if i < 3]


def get_rhythmic_momentum(momentums):
    """returns list of momentums"""
    chosen_momentum = choice(momentums) if momentums else 0
    if len(momentums) == 2:
        momentums.extend([chosen_momentum] * 5)
    elif len(momentums) > 2 and momentums.count(chosen_momentum) > 1:
        momentums.remove(chosen_momentum)
    else:
        momentums = [0, 0, 0, 0, 0, 1, -1, -2]
    return momentums


def octavify(timeline_, time, note_length, root, enabled):
    """Adds note to timeline, octavified if enabled."""
    if enabled:
        timeline_.add(time, timeline.Hit(root.transpose(-12), note_length / 2))
        timeline_.add(time + 0.5 * note_length, timeline.Hit(root, note_length / 2))
    else:
        timeline_.add(time, timeline.Hit(root.transpose(-12), note_length))
    time = time + note_length
    return timeline_, time
