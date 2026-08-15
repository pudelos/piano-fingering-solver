from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True, slots=True)
class Note:
    start: Fraction
    end: Fraction
    pitch: int
