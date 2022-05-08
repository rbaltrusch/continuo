# -*- coding: utf-8 -*-
"""Entry point to the music generator"""

# pylint: disable=wrong-import-position
import os
from typing import List

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"  # hide pygame hello

import functools
import logging

from music_generation import (
    playback,
    layer,
    generator,
    duration,
    music_algorithm,
    cli,
    config,
    output,
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


def setup_music_generation(args) -> None:
    music_algorithm.NUMBER_OF_MOTIFS = args.motifs
    music_algorithm.NUMBER_OF_VARIATIONS = args.variations


def construct_generator(args) -> generator.Generator:
    """Generates music using the passed argparser"""
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

    return generator.Generator(scale, duration_, music_generator, volume=args.volume)


def construct_layers(args) -> List[layer.Layer]:
    """Loads layers from file or constructs new ones"""
    if args.load_filepath:
        return output.load_from_json(args.load_filepath)

    layer_offsets = args.layer_offsets if args.layer_offsets else [0, 12, 12]
    layers = layer.init_layers(
        number_of_layers=args.layers, layer_offsets=layer_offsets
    )
    return layers


def save_to_file(args, data, layers):
    """Saves data and layers to all specified formats"""
    formats = {
        "wav": functools.partial(output.save_to_wav_file, data),
        "json": functools.partial(output.save_to_json, layers),
    }

    # pylint: disable=consider-using-f-string
    save_formats = ["wav"] if not args.save_formats else args.save_formats
    for format_ in set(save_formats):
        filepath = "{}.{}".format(os.path.splitext(args.save_filepath)[0], format_)
        formats[format_](filepath)


def generate_music(args) -> None:
    """Generates music"""
    setup_music_generation(args)
    layers = construct_layers(args)
    generator_ = construct_generator(args)
    data = generator_.generate_music(layers)

    if args.playback == "True":
        playback.play(data)

    if args.save_filepath:
        save_to_file(args, data, layers)


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
