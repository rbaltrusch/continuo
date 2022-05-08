# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 13:44:31 2022

@author: richa
"""
import json
from typing import List

import numpy
from musical.audio.save import save_wave

from music_generation.layer import Layer


def save_to_wav_file(data: numpy.ndarray, filepath: str) -> None:
    """Saves the data to a wavfile"""
    save_wave(data, filepath)


def save_to_json(layers: List[Layer], filepath: str) -> None:
    """Saves the layers to a json file"""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump([layer.__dict__ for layer in layers], file, indent=4)


def load_from_json(filepath: str) -> List[Layer]:
    """Loads the layers from a json file"""
    with open(filepath, "r", encoding="utf-8") as file:
        contents = json.load(file)
    return [Layer(**dict_) for dict_ in contents]
