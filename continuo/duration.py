# -*- coding: utf-8 -*-
"""Duration module"""

import math
from dataclasses import dataclass


@dataclass
class Duration:
    """Duration class, holds information on tempo on time length"""

    time_length: int = 45
    tempo: int = 40
    motif_length: int = 24

    def __post_init__(self):
        self.eigth = (60 / self.tempo) / 2
        self.length = math.ceil(self.time_length / (self.eigth * self.motif_length))
