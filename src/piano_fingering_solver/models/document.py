from dataclasses import dataclass

from music21.stream import Score

from piano_fingering_solver.models.melody import Melody


@dataclass(slots=True)
class MusicXmlDocument:
    melody: Melody
    source_score: Score
