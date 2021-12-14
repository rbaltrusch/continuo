# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 15:53:15 2019

@author: Korean_Crimson
"""
from musical.audio import playback
from musical.audio.source import sine

from harmony import convert_from_db


def organ_sound(freq, time):
    """get sound font of a church organ by layering the first 32 harmonics with
    correct scaling on top of each other"""
    frequencies = []
    sinewave = 0
    harmonic_scalings = get_organ_harmonic_scalings()
    amplitude_scaling = 1 / 350000000  # anti-saturation
    for i, harmonic_scaling in enumerate(harmonic_scalings):
        frequencies.append((i + 1) * freq)
        sinewave += sine(frequencies[i], time) * convert_from_db(harmonic_scaling)
    return sinewave * amplitude_scaling


def get_organ_harmonic_scalings():
    """return scaling of a church organ for the first 32 harmonics"""
    return [
        55,
        56,
        57,
        60,
        48,
        49,
        46,
        44,
        45,
        42,
        40,
        33,
        32,
        28,
        27,
        26,
        25,
        24,
        23,
        22,
        22,
        18,
        20,
        19,
        15,
        20,
        11,
        14,
        13,
        12,
        11,
        10,
    ]


def organ_sound_test():
    """test playback with soundfont"""
    chords = [
        [50, 75, 100, 125, 150, 200, 250],
        [66.7, 84.4, 100, 112.5, 133.3, 200, 266.7],
        [75, 112.5, 133.3, 150, 190, 225],
    ]
    for chord in chords:
        data = 0
        for note in chord:
            data += organ_sound(freq=note * 5, time=3)
        playback.play(data)


if __name__ == "__main__":
    organ_sound_test()
