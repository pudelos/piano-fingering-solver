from dataclasses import dataclass

from piano_fingering_solver.core.note import Note


@dataclass(slots=True)
class Melody:
    notes: list[Note]
