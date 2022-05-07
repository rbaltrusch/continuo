[![Pylint](https://github.com/rbaltrusch/music_generation/actions/workflows/pylint.yml/badge.svg)](https://github.com/rbaltrusch/music_generation/actions/workflows/pylint.yml)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

# Music Generation

This tool procedurally generates music based on codified Western classical music principles.

## Getting started

To get a copy of this repository, simply open up git bash in an empty folder and use the command:

    $ git clone https://github.com/rbaltrusch/music_generation

To install the music_generation module and all python dependencies, run the following in your command line:

    python -m pip install -e .
    python -m pip install -r requirements.txt

To run the music generator, run the package from the project root folder:

    python -m music_generation

## Example music

Example music can be found [here](example_music).

## Parameterization

Custom parameterization is possible over the command line interface or an external configuration file, but currently not consolidated into one config file.

### Command line interface

The application supports configuration of almost every configurable setting directly over the command line interface.

A full list of the available arguments is listed below:

```
usage: __main__.py [-h] [--generate-config [CONFIG_FILEPATH]] [--config-file CONFIG_FILE] [--time-length TIME_LENGTH]
                   [--layers LAYERS] [--tempo TEMPO] [--mode {major,minor}] [--base-note BASE_NOTE]
                   [--motif-length MOTIF_LENGTH] [--layer-offsets [LAYER_OFFSETS [LAYER_OFFSETS ...]]]
                   [--sophistication SOPHISTICATION] [--variations VARIATIONS] [--motifs MOTIFS]

optional arguments:
  -h, --help            show this help message and exit
  --generate-config [CONFIG_FILEPATH], -g [CONFIG_FILEPATH]
                        Generates a template music configuration file under the specified filepath
  --config-file CONFIG_FILE, -c CONFIG_FILE
                        The filepath of a music configuration file
  --time-length TIME_LENGTH, --time TIME_LENGTH
                        The length of time the generated music should last
  --layers LAYERS, -l LAYERS
                        The amount of layers to be generated
  --tempo TEMPO, -t TEMPO
                        The tempo of the generated music
  --mode {major,minor}, -m {major,minor}
                        The mode of the generated music
  --base-note BASE_NOTE, -b BASE_NOTE
                        The lowest note used in the generated music (e.g. A3)
  --motif-length MOTIF_LENGTH
                        The length of the generated motifs
  --layer-offsets [LAYER_OFFSETS [LAYER_OFFSETS ...]], -o [LAYER_OFFSETS [LAYER_OFFSETS ...]]
                        The amount of semitones layers should be offset from base note
  --sophistication SOPHISTICATION, -s SOPHISTICATION
                        The amount of options that should be considered when generating new notes
  --variations VARIATIONS, -v VARIATIONS
                        The amount of motif variations to be considered
  --motifs MOTIFS       The amount of motifs to be considered
```

The help message can be brought up by running:

```
python -m music_generation -h
```

### Configuration file

Advanced settings, such as intervals, harmonies and consonance mappings can not be directly provided over the command line interface, but may be provided in an external configuration file.

Generate a template configuration file by running:

```
python -m music_generation --generate-config <filename>
```

To run the music generator with a configuration file, run:

```
python -m music_generation --config-file <filename>
```

The configuration file currently supports 4 main advanced settings:
- "momentums": a list of non-unique integers that are used to factorise note intervals to decide direction. This should only contain -1, 0 or 1, but may technically contain anything.
- "intervals": a list of non-unique integers that will be chosen from by the music generator when generating motifs.
- "consonance_dict": a mapping of integer intervals to the respective (float) consonance (the lower, the more dissonant the interval is treated as and will be avoided).
- "harmony_dict": a mapping of integer intervals to a list of integer intervals, representing all possible continuations from one note to another.

An example configuration file could look like this:
```json
{
    "momentums": [-1, 0, 1],
    "intervals": [0, 0, 1, 1, 2, 3],
    "consonance_dict": {
        "0": 0.25,
        "1": -0.25,
        "2": 1,
        "3": 0.5,
        "4": 0.5,
        "5": 0.5,
        "6": -0.25
    },
    "harmony_dict": {
        "0": [6, 1, 3],
        "1": [4],
        "2": [1, 3],
        "3": [4],
        "4": [0, 5],
        "5": [4, 1],
        "6": [0]
    }
}
```

## Contributions

All contributions are welcome! Please read the [contribution guidelines](CONTRIBUTING.md).

## Python

Written in Python 3.8.3.

## License

This repository is open-source software available under the [AGPL-3.0 License](https://github.com/rbaltrusch/music_generation/blob/master/LICENSE).

## Contact

Please raise an issue for code changes. To reach out, please send an email to richard@baltrusch.net.
