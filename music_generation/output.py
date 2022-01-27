# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 13:44:31 2022

@author: richa
"""
from musical.audio.save import save_wave

#pylint: disable=unspecified-encoding
def save_to_file(layers, data):
    """gives choice to save generated piece to text file"""
    title = input("Please input the title under which you wish to save: ")
    save_wave(data, f"{title}.wav")
    with open(f"{title}.txt", "w+") as file:
        for layer in layers:
            file.write(" ".join(map(str, layer)))


def load_from_file():
    """gives choice of loading piece from saved text file"""
    with open(input("Please input the text file title: "), "r") as file:
        contents = file.read().split("*")
    return [[int(num) for num in content.split() if num.isdigit()] for content in contents[:-1]]
