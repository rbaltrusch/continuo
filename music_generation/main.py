# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 12:20:25 2019

@author: Korean_Crimson
"""

from musical.theory import Note, Scale, Chord
from musical.audio import playback
from musical.audio.save import save_wave
from postprocessing import apply_effects, fix_harmony
from music_algorithm import make_piece
from rhythm import make_rhythm, octavify
import timeline

def init():
    '''Define key and scale'''
    key = Note('A3')
    scale = Scale(key, 'major')
    progression = Chord.progression(scale, base_octave=key.octave)
    scale_len = 7
    return progression, scale_len

def set_params():
    '''set global variables'''
    number_of_layers = 3
    time_length = 25
    random_intervals = [5, 4, 3, 2, 1, 1, 0, 0]
    tempo = 40
    eigth = (60 / tempo) / 2
    note_lengths = [eigth]
    return note_lengths, eigth, random_intervals, time_length, number_of_layers

def save_to_file(layers, data):
    '''gives choice to save generated piece to text file'''
    save = input("Do you want to save? (y/n): ")
    if save == "y":
        title = input("Please input the title under which you wish to save: ")
        save_wave(data, f"{title}.wav")
        with open(f"{title}.txt", "w+") as file:
            for layer in layers:
                for note in layer:
                    file.write(f"{str(note)} ")

def load_from_file():
    '''gives choice of loading piece from saved text file'''
    load = input("Do you want to load a piece? (y/n): ")
    layer = []
    if load == "y":
        with open(input("Please input the text file title: "), "r") as file:
            contents = file.read()
        split_contents = contents.split("*")
        split_contents.pop(-1)
        for content in split_contents:
            layer.append([int(num) for num in content.split() if num.isdigit()])
    return layer, load

def playback_music(data):
    '''play back audio data'''
    playback_on = input("playback? (y/n): ")
    if playback_on == 'y':
        print("Playing audio...")
        playback.play(data)
    print("Done!")

def render_timeline(layers, note_lengths, progression, scale_len):
    '''rendering the timeline'''
    timeline_ = timeline.Timeline()
    transpose_array = [0, 12, 12, 24, 24, 24, 24, 12, 0]
    for layer, transposition in zip(layers, transpose_array):
        note_lengths = make_rhythm(layer, note_lengths)
        time = 0
        for note_length, note in zip(note_lengths, layer):
            note %= scale_len
            chord = progression[note]
            root, _, _ = chord.notes
            enabled = True if layers.index(layer) == 0 else False
            root_ = root.transpose(transposition)
            timeline_, time = octavify(timeline_, time, note_length, root_, enabled)
    return timeline_

def main_func():
    '''main function'''
    progression, scale_len = init()
    note_lengths, eigth, random_intervals, time_length, number_of_layers = set_params()
    layers, load = load_from_file()
    if load == "n":
        layers = make_piece(time_length, eigth, number_of_layers, scale_len, random_intervals)
        note_lengths_ = make_rhythm(layers[0], note_lengths)
        layers = fix_harmony(layers, scale_len, no_of_times=10000)
    timeline_ = render_timeline(layers, note_lengths_, progression, scale_len)
    data = apply_effects(timeline_)
    playback_music(data)
    save_to_file(layers, data)

if __name__ == '__main__':
    main_func()
