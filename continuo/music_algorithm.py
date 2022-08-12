# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 16:03:40 2019

@author: Korean_Crimson
"""
from dataclasses import dataclass, field
import functools
import random
from statistics import mean
from typing import Dict, List, Tuple

from continuo.layer import Layer


Notes = List[int]
NUMBER_OF_VARIATIONS = 50000
NUMBER_OF_MOTIFS = 250


def get_default_consonance_dict() -> Dict[int, float]:
    """Returns the default mapping of septatonic note to consonance"""
    return {
        0: 0.25,
        1: -0.25,
        2: 1,
        3: 0.5,
        4: 0.5,
        5: 1,
        6: -0.25,
    }


def get_default_harmony_dict() -> Dict[int, List[int]]:
    """Returns the default mapping of septatonic note to possible following notes"""
    return {
        0: [6, 1, 3],
        1: [4],
        2: [1, 3],
        3: [4],
        4: [0, 5],
        5: [6, 4, 3, 1],
        6: [0, 5],
    }


@dataclass
class MusicGenerator:
    """MusicGenerator class that generates a layered piece of motivic music"""

    sophistication: int = 1
    motif_length: int = 24
    scale_length: int = 7
    momentums: Tuple[int] = (-1, 0, 1)  # type: ignore
    intervals: Tuple[int] = (5, 4, 3, 2, 1, 1, 0, 0)  # type: ignore
    consonance_dict: Dict[int, float] = field(
        default_factory=get_default_consonance_dict
    )
    harmony_dict: Dict[int, List[int]] = field(default_factory=get_default_harmony_dict)

    def get_consonance(self, note1: int, note2: int) -> float:
        """returns a measure of consonance (between 0 and 1) of two notes (type double)"""
        diff = abs(note1 - note2) % 7
        return self.consonance_dict.get(diff, 0)

    def get_most_consonant_motif(
        self, motifs: List[Notes], layers: List[Layer]
    ) -> Notes:
        """returns list of notes (type double), after determining most consonant motif"""
        return max(motifs, key=lambda x: self.get_motif_consonance(x, layers))

    def get_motif_consonance(self, motif: Notes, layers: List[Layer]) -> float:
        """Returns the consonance of the motif compared with existing notes in layers"""
        consonances = [
            mean([self.get_consonance(note, new_note) for note in notes])
            for new_note, *notes in zip(motif, *layers)
        ]
        return mean(consonances) if consonances else 0

    def make_progression(self) -> List[int]:
        """returns a chord progression (list of doubles), starting with 0 and
        ending with 4, i.e. root and fifth, respectively"""
        notes = [0]
        for _ in range(self.motif_length - 2):
            notes.append(self._get_next_chord(notes[-1]))
        motif = notes + [4]
        return motif[: self.motif_length]

    def make_motif(self, layers) -> List[int]:
        """returns a motif (list of notes (type double)) based on maximum consonance
        with notes in existing layers"""
        def get_note_consonance(notes_, note):
            return mean([self.get_consonance(x, note) for x in notes_])

        motif = random.choices(range(self.scale_length), k=1)
        for i, notes in enumerate(zip(*layers)):
            if i >= self.motif_length:
                break

            new_notes = [
                motif[-1] + self._get_random_interval() for _ in range(self.sophistication)
            ]
            new_note = max(new_notes, key=functools.partial(get_note_consonance, notes))
            motif.append(new_note)
        return motif[: self.motif_length]

    def _get_random_interval(self) -> int:
        return random.choice(self.momentums) * random.choice(self.intervals)

    def _get_next_chord(self, chord: int) -> int:
        """returns a random choice (double) of the available harmonic follow-ups
        for the given chord (double)"""
        return random.choice(self.harmony_dict[chord])


def smooth_bass_line(bass_lines: List[Notes]) -> Notes:
    """Returns the bass line with the least number of leaps in it"""
    return min(
        bass_lines,
        key=lambda x: sum(abs(note2 - note1) for note1, note2 in zip(x, x[1:])),
    )


def create_variations(bass_line: Notes, num: int = 1) -> List[Notes]:
    """returns list of lists containing inversions"""
    inversions = [0, 2, 4]
    return [
        [note + random.choice(inversions) for note in bass_line] for _ in range(num)
    ]


def make_piece(layers: List[Layer], music_generator: MusicGenerator):
    """Generates notes using the provided music generator
    and appends them to the specified layers
    """
    if not layers:
        return

    motif = smooth_bass_line(
        create_variations(music_generator.make_progression(), num=NUMBER_OF_VARIATIONS)
    )
    layers[0].extend(motif)

    for j, layer in enumerate(layers[1:], 1):
        motifs = [
            music_generator.make_motif(layers[:j]) for _ in range(NUMBER_OF_MOTIFS)
        ]
        motif = music_generator.get_most_consonant_motif(motifs, layers)
        layer.extend(motif)
