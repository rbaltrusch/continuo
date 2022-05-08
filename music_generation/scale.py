# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 17:50:33 2022

@author: richa
"""
from dataclasses import dataclass

import musical.theory


@dataclass
class Scale:
    """Scale class"""

    key: str
    tonality: str
    length: int = 7

    def __post_init__(self):
        root = musical.theory.Note(self.key)
        self.scale = musical.theory.Scale(root, self.tonality)
        self.chords = musical.theory.Chord.progression(
            self.scale, base_octave=root.octave
        )
        self.notes = list(range(self.length))
