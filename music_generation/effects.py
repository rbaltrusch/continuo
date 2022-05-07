# -*- coding: utf-8 -*-
"""Wrapper around the musical.audio.effect module"""

from musical.audio import effect

def apply_effects(data):
    """Takes in a numpy array and applies sound effects"""
    return effect.flanger(effect.tremolo(effect.chorus(data, 2), 4), 4)
