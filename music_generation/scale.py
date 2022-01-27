# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 17:50:33 2022

@author: richa
"""
import musical.theory

#pylint: disable=too-few-public-methods
class Scale:
    """Scale class"""

    def __init__(self, key: str, tonality: str):
        self.key = key
        self.tonality = tonality
        root = musical.theory.Note(self.key)
        self.scale = musical.theory.Scale(root, self.tonality)
        self.chords = musical.theory.Chord.progression(self.scale, base_octave=root.octave)
        self.length = 7
        self.notes = list(range(self.length))

    def __repr__(self):
        return f"{self.key} {self.tonality}"
