from dataclasses import dataclass

from music21 import note as music21_note
from music21.stream import Score

from piano_fingering_solver.models.melody import Melody


@dataclass(slots=True)
class MusicXmlDocument:
    melody: Melody
    source_score: Score
    melody_source_notes: list[music21_note.Note]
