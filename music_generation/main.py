# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 12:20:25 2019

@author: Korean_Crimson
"""
import math
from dataclasses import dataclass
from typing import Tuple

from musical.audio import effect

import music_algorithm
import playback
import timeline
from enums import Notes
from scale import Scale


def apply_effects(data):
    """Takes in a numpy array and applies sound effects"""
    return effect.flanger(effect.tremolo(effect.chorus(data, 2), 4), 4)

#pylint: disable=too-many-instance-attributes
@dataclass
class Params:
    """Parameter class"""

    number_of_layers: int = 3
    time_length: int = 45
    intervals: Tuple[int] = (5, 4, 3, 2, 1, 1, 0, 0) # type: ignore
    layer_octaves: Tuple[int] = (0, 12, 12, 24, 24, 24, 24, 12, 0) # type: ignore
    tempo: int = 40
    motif_length: int = 24

    def __post_init__(self):
        self.eigth = (60 / self.tempo) / 2
        self.length = math.ceil(self.time_length / (self.eigth * self.motif_length))


def render_timeline(timeline_, layers, params, scale):
    """Rendering the timeline"""
    for i, (layer, transposition) in enumerate(zip(layers, params.layer_octaves)):
        timeline_.set_time(0)
        for note in map(lambda x: x % scale.length, layer):
            chord = [*scale.chords[note]]
            note = chord[Notes.ROOT.value].transpose(transposition)
            timeline_.append_note(note, params.eigth, octavify=not i)


def main():
    """Main function"""
    scale = Scale("A3", "major")
    params = Params()
    layers = music_algorithm.make_piece(params, scale.length)
    timeline_ = timeline.Timeline()
    render_timeline(timeline_, layers, params, scale)
    data = timeline_.render(volume=0.05)
    playback.play(data)

if __name__ == "__main__":
    main()
