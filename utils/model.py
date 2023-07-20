
from dataclasses import dataclass


@dataclass
class Range:
    lower: int
    upper: int


@dataclass
class Region:
    anode: Range
    cathode: Range
