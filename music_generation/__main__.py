# -*- coding: utf-8 -*-
"""Entry point to the music generator"""

from music_generation import (
    playback,
    layer,
    generator,
    duration,
    music_algorithm,
    cli,
    config,
)
from music_generation.scale import Scale


def read_config_file(config_file: str):
    if not config_file:
        return {}
    return config.read_configuration_file(
        filepath=config_file,
        required_fields=["momentums", "intervals", "consonance_dict", "harmony_dict"],
    )


def generate_music(parser):
    layers = layer.init_layers(parser.number_of_layers, parser.layer_offsets)
    scale = Scale(key=parser.lowest_note, tonality=parser.mode)

    kwargs = read_config_file(parser.config_file)
    music_generator = music_algorithm.MusicGenerator(
        scale_length=scale.length,
        motif_length=parser.motif_length,
        sophistication=parser.sophistication,
        **kwargs
    )

    duration_ = (
        duration.Duration(
            time_length=parser.time_length,
            tempo=parser.tempo,
            motif_length=parser.motif_length,
        ),
    )

    generator_ = generator.Generator(scale, duration_, music_generator)
    data = generator_.generate_music(layers)
    playback.play(data)


parser = cli.construct_parser()
if parser.generate_config:
    config.write_configuration_file(
        filepath=parser.generate_config,
        music_generator=music_algorithm.MusicGenerator(),
    )
else:
    generate_music(parser)
