# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 16:45:05 2022

@author: richa
"""
import numpy
import pygame


def play(data: numpy.ndarray, rate=44100):
    """Plays back the specified data using the pygame.mixer module"""
    pygame.mixer.quit()
    pygame.mixer.init(rate, -16, channels=2, buffer=1024)
    data = (data.clip(-1, 1) * 32767).astype(numpy.int16)

    # handle stereo mixer by duplicating data
    *_, channels = pygame.mixer.get_init()
    if channels == 2:
        data = numpy.repeat(data.reshape(data.size, 1), 2, axis=1)

    sound = pygame.sndarray.make_sound(data)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))
    pygame.mixer.quit()
