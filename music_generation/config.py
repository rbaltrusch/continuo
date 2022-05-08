# -*- coding: utf-8 -*-
"""Configuration file handling"""

import json
from typing import Any, List, Dict
from music_generation.music_algorithm import MusicGenerator


class ConfigurationError(Exception):
    """ConfigurationError to be thrown for invalid config files"""


def read_configuration_file(
    filepath: str, required_fields: List[str]
) -> Dict[str, Any]:
    """Reads in the specified configuration file.
    Raises a ConfigurationError if configuration file does not contain all required fields.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        contents: Dict[str, Any] = json.load(file)

    for field in required_fields:
        if field not in contents:
            raise ConfigurationError(
                f"Invalid configuration file, missing required field {field}"
            )

    for name, value in contents.items():
        if isinstance(value, dict):
            contents[name] = {
                (int(k) if k.isnumeric() else k): v for k, v in value.items()
            }

    return contents


def write_configuration_file(filepath: str, music_generator: MusicGenerator) -> None:
    """Writes the attributes of the specified music generator to the filepath provided."""
    dict_ = {k: v for k, v in music_generator.__dict__.items() if not callable(v)}
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(dict_, file, indent=4)
