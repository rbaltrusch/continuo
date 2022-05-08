# -*- coding: utf-8 -*-
"""Layer module"""

from itertools import zip_longest
from dataclasses import dataclass, field
from typing import List


@dataclass
class Layer:
    """Layer class, holds notes for one voice in the piece"""

    notes: List[int] = field(default_factory=list)
    offset: int = 0

    def extend(self, notes: List[int]):
        """Extends the layer by the specified notes"""
        self.notes.extend(notes)

    def __iter__(self):
        for note in self.notes:
            yield note

    def __getitem__(self, key):
        return self.notes[key]


def init_layers(number_of_layers: int = 3, layer_offsets=(0, 12, 12)) -> List[Layer]:
    """Initialises a list of layers"""
    return [
        Layer(offset=offset)
        for _, offset in zip_longest(
            range(number_of_layers),
            layer_offsets[:number_of_layers],
            fillvalue=0,
        )
    ]
