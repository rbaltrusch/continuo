# -*- coding: utf-8 -*-
"""
Copyright (c) 2017 Davy Wybiral

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, List

from musical.audio import source

from music_generation.enums import Notes
from music_generation.scale import Scale
from music_generation.layer import Layer

#pylint: disable=too-few-public-methods
#pylint: disable=missing-function-docstring

class Hit:
    """Rough draft of Hit class. Stores information about the hit and generates
      the audio array accordingly. Currently implements a basic cache to avoid
      having to rerender identical hits
  """

    cache = {} #type: ignore

    def __init__(self, note, length):
        self.note = note
        self.length = length

    def render(self):
        """Render hit of "key" for "length" amound of seconds"""
        key = (str(self.note), self.length)
        if key not in Hit.cache:
            Hit.cache[key] = source.square(self.note, self.length)
        return Hit.cache[key]


@dataclass
class Timeline:
    """Rough draft of Timeline class. Handles the timing and mixing of Hits"""

    rate: int = 44100
    tempo: int = 120

    def __post_init__(self):
        self.hits: DefaultDict[float, List[Hit]] = defaultdict(list)
        self._time = 0

    def set_time(self, time: int):
        """Sets the time to the passed value"""
        self._time = time

    def add(self, hit: Hit):
        """Add "hit" at "time" seconds in"""
        self.hits[self._time].append(hit)
        self._time += hit.length

    def calculate_length(self) -> float:
        """Determine length of playback from end of last hit"""
        length = 0.0
        for time, hits in self.hits.items():
            for hit in hits:
                length = max(length, time + hit.length)
        return length

    def construct(self, layers: List[Layer], scale: Scale) -> None:
        """Rendering the timeline"""
        for i, layer in enumerate(layers):
            self.set_time(0)
            for note in map(lambda x: x % scale.length, layer):
                chord = [*scale.chords[note]]
                note = chord[Notes.ROOT.value].transpose(layer.octave)
                self.append_note(note, self.eigth, octavify=not i)

    def render(self, volume: float = 1):
        """Return timeline as audio array by rendering the hits"""
        out = source.silence(self.calculate_length())
        for time, hits in self.hits.items():
            index = int(time * self.rate)
            for hit in hits:
                data = hit.render()
                out[index : index + len(data)] += data
        return out * volume

    def append_note(self, note, note_length, octavify=False) -> None:
        """Adds note to timeline, octavified if enabled."""
        if octavify:
            note_length /= 2
            self.add(Hit(note.transpose(-12), note_length))
        self.add(Hit(note, note_length))

    @property
    def eigth(self) -> float:
        return (60 / self.tempo) / 2
