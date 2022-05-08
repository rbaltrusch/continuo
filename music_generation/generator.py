# -*- coding: utf-8 -*-
"""Layer module"""

from typing import List
from dataclasses import dataclass

from music_generation import scale, duration, music_algorithm, timeline, layer


@dataclass
class Generator:
    """Generator class that generates layered music"""

    scale: scale.Scale
    duration: duration.Duration
    music_generator: music_algorithm.MusicGenerator
    volume: float = 0.05

    def generate_music(self, layers: List[layer.Layer]):
        """Generates layered music and returns it as an numpy.ndarray of audio data"""
        for _ in range(self.duration.length):
            music_algorithm.make_piece(layers, self.music_generator)

        timeline_ = timeline.Timeline(tempo=self.duration.tempo)
        timeline_.construct(layers, self.scale)
        data = timeline_.render(volume=self.volume)
        return data
