# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 15:59:04 2019

@author: Korean_Crimson
"""
from random import choice
import itertools
from musical.audio import effect
from harmony import find_min_change_in_smoothness, find_missing_note

def fix_harmony(layers, scale_len, no_of_times):
    '''iterate over the notes in the musical layers and try to find the note
    that can change with the smallest change in voice leading smoothness'''
    for _ in range(no_of_times):
        previous_notes = []
        posterior_notes = list(itertools.chain(*layers))
        current_notes = posterior_notes
        for i, layer in enumerate(layers):
            missing_note = find_missing_note(layer, i - 1, scale_len)
            if i and not missing_note in current_notes:
                changednote, index = find_min_change_in_smoothness(previous_notes, posterior_notes, missing_note, scale_len)
                layer[index][i] = changednote
                previous_notes = current_notes
    return layers

def smooth_bass_line(list_of_bass_line_inversions):
    '''smoothness is the counter of how long we let the program search for a smooth bass_line'''
    list_of_differences = []
    for bass_line in list_of_bass_line_inversions:
        difference = 0
        for i in range(len(bass_line)-1):
            difference += abs(bass_line[i+1] - bass_line[i])
        list_of_differences.append(difference)
    min_index = list_of_differences.index(min(list_of_differences))
    smoothed_bass_line = list_of_bass_line_inversions[min_index]
    return smoothed_bass_line

def get_bass_line_inversions(bass_line, smoothness):
    '''returns list of lists containing inversions'''
    inversions = [0, 2, 4]
    list_of_bass_line_inversions = []
    for _ in range(smoothness):
        new_bass_line = []
        for note in bass_line:
            note += choice(inversions)
            new_bass_line.append(note)
        list_of_bass_line_inversions.append(new_bass_line)
    return list_of_bass_line_inversions

def apply_effects(timeline):
    '''applies sound effects and reduces volume to avoid saturation'''
    data = timeline.render()
    data = data * 0.05 # Reduce volume to 5%
#    data = effect.chorus(data, 2)
#    data = effect.tremolo(data, 4)
#    data = effect.flanger(data, 4)
    return data
