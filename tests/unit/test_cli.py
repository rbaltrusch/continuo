# -*- coding: utf-8 -*-
"""Cli module tests"""

import argparse
import pytest

from music_generation import cli


def test_default_parser():
    parser = cli.construct_parser()
    args = parser.parse_args("")
    assert args.config_filepath == ""
    assert args.config_file is None
    assert args.playback == "True"
    assert args.save_filepath == ""
    assert args.save_formats is None
    assert args.load_filepath == ""
    assert args.time_length == 10
    assert args.layers == 3
    assert args.mode == "major"
    assert args.base_note == "A3"
    assert args.motif_length == 24
    assert args.layer_offsets is None
    assert args.sophistication == 1
    assert args.variations == 50000
    assert args.motifs == 250
    assert args.volume == 1


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--generate-config abc", "abc"),
        ("-g a", "a"),
    ],
)
def test_generate_config(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.config_filepath == expected


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--config-file test", "test"),
        ("-c a", "a"),
    ],
)
def test_config_file(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.config_file == expected


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--playback True", "True"),
        ("--playback False", "False"),
        ("-p False", "False"),
    ],
)
def test_playback(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.playback == expected


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--save savefile", "savefile"),
        ("-s we", "we"),
    ],
)
def test_save(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.save_filepath == expected


@pytest.mark.parametrize(
    "input_args,expected",
    [
        ("--format json", ["json"]),
        ("-f wav", ["wav"]),
        ("--format json wav", ["json", "wav"]),
        ("--format", []),
        ("--format json wav json", ["json", "wav", "json"]),
    ],
)
def test_format(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.save_formats == expected


def test_format_fail():
    parser = cli.construct_parser()
    with pytest.raises(SystemExit):
        parser.parse_args("--format a".split())


def test_load():
    parser = cli.construct_parser()
    args = parser.parse_args("--load ert.json".split())
    assert args.load_filepath == "ert.json"


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--time-length 11", 11),
        ("--time 0", 0),
        ("-ti 23", 23),
    ],
)
def test_time_length(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.time_length == expected


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--layers 2", 2),
        ("-l 5", 5),
    ],
)
def test_layers(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.layers == expected


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--tempo 200", 200),
        ("-t 5", 5),
    ],
)
def test_tempo(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.tempo == expected


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--mode major", "major"),
        ("-m minor", "minor"),
    ],
)
def test_mode(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.mode == expected


def test_mode_fails():
    parser = cli.construct_parser()
    with pytest.raises(SystemExit):
        parser.parse_args("--mode a".split())


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--base-note A5", "A5"),
        ("-b E4", "E4"),
    ],
)
def test_base_note(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.base_note == expected


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--motif-length 5", 5),
        ("-ml 3", 3),
    ],
)
def test_motif_length(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.motif_length == expected


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--layer-offsets 3 5 7", [3, 5, 7]),
        ("-o 2 7", [2, 7]),
        ("-o", []),
    ],
)
def test_layer_offsets(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.layer_offsets == expected


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--sophistication 5", 5),
        ("-so 6", 6),
    ],
)
def test_sophistication(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.sophistication == expected


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--variations 12", 12),
        ("-va 3", 3),
    ],
)
def test_variations(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.variations == expected


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--motifs 20", 20),
    ],
)
def test_motifs(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.motifs == expected


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--volume 20", 20),
        ("-v 2", 2),
    ],
)
def test_motifs(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.volume == expected


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ("--seed 20", 20),
        ("-se 252", 252),
    ],
)
def test_motifs(input_args, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(input_args.split())
    assert args.seed == expected
