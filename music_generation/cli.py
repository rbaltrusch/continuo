# -*- coding: utf-8 -*-
"""Module responsible for the cli parser construction"""

import argparse


def construct_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--generate-config",
        "-g",
        nargs="?",
        type=str,
        default="",
        dest="config_filepath",
        help="Generates a template music configuration file under the specified filepath",
    )

    parser.add_argument(
        "--config-file", "-c", help="The filepath of a music configuration file"
    )

    parser.add_argument(
        "--time-length",
        "--time",
        type=int,
        default=30,
        help="The length of time the generated music should last",
    )

    parser.add_argument(
        "--layers",
        "-l",
        type=int,
        default=3,
        help="The amount of layers to be generated",
    )

    parser.add_argument(
        "--tempo", "-t", type=int, default=60, help="The tempo of the generated music"
    )

    parser.add_argument(
        "--mode",
        "-m",
        choices=["major", "minor"],
        default="major",
        help="The mode of the generated music",
    )

    parser.add_argument(
        "--base-note",
        "-b",
        default="A3",
        help="The lowest note used in the generated music (e.g. A3)",
    )

    parser.add_argument(
        "--motif-length",
        type=int,
        default=24,
        help="The length of the generated motifs",
    )

    parser.add_argument(
        "--layer-offsets",
        "-o",
        type=int,
        nargs="*",
        action="extend",
        help="The amount of semitones layers should be offset from base note",
    )

    parser.add_argument(
        "--sophistication",
        "-s",
        type=int,
        default=1,
        help="The amount of options that should be considered when generating new notes",
    )

    parser.add_argument(
        "--variations",
        "-v",
        type=int,
        default=50000,
        help="The amount of motif variations to be considered",
    )

    parser.add_argument(
        "--motifs", type=int, default=250, help="The amount of motifs to be considered"
    )

    return parser
