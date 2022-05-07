# -*- coding: utf-8 -*-
"""Entry point to the music generator"""

import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"  # hide pygame hello
import logging

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
    """Reads in the specified config file"""
    if not config_file:
        return {}
    return config.read_configuration_file(
        filepath=config_file,
        required_fields=["momentums", "intervals", "consonance_dict", "harmony_dict"],
    )


def generate_music(args):
    """Generates music using the passed argparser"""
    layer_offsets = args.layer_offsets if args.layer_offsets else [0, 12, 12]
    layers = layer.init_layers(
        number_of_layers=args.layers, layer_offsets=layer_offsets
    )
    scale = Scale(key=args.base_note, tonality=args.mode)

    kwargs = read_config_file(args.config_filepath)
    music_generator = music_algorithm.MusicGenerator(
        scale_length=scale.length,
        motif_length=args.motif_length,
        sophistication=args.sophistication,
        **kwargs
    )

    duration_ = duration.Duration(
        time_length=args.time_length,
        tempo=args.tempo,
        motif_length=args.motif_length,
    )

    music_algorithm.NUMBER_OF_MOTIFS = args.motifs
    music_algorithm.NUMBER_OF_VARIATIONS = args.variations
    generator_ = generator.Generator(scale, duration_, music_generator)
    data = generator_.generate_music(layers)
    playback.play(data)


def main():
    """Main function"""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    parser = cli.construct_parser()
    args = parser.parse_args()
    for name, value in vars(args).items():
        if name != "config_filepath":
            logging.info("Using setting %s: %s", name, value)

    if args.config_filepath:
        config.write_configuration_file(
            filepath=args.config_filepath,
            music_generator=music_algorithm.MusicGenerator(),
        )
    else:
        generate_music(args)


main()
