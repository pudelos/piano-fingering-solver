from itertools import pairwise

from music21 import chord as music21_chord
from music21 import stream

from piano_fingering_solver.core.note import Note
from piano_fingering_solver.importer.exceptions import MusicXmlImportError


class MusicXmlValidator:
    @staticmethod
    def validate_score(source_score: stream.Score) -> None:
        if len(source_score.parts) != 1:
            raise MusicXmlImportError(
                "Only MusicXML files with exactly one part are supported."
            )

        part = source_score.parts[0]
        measures = part.recurse().getElementsByClass("Measure")

        if any(measure.hasVoices() for measure in measures):
            raise MusicXmlImportError("Multiple voices are not supported.")

        if any(
            isinstance(element, music21_chord.Chord) for element in part.flatten().notes
        ):
            raise MusicXmlImportError("Chords are not supported yet.")

    @staticmethod
    def validate_melody(notes: list[Note]) -> None:
        for previous, current in pairwise(notes):
            if current.start < previous.end:
                raise MusicXmlImportError("Overlapping notes are not supported.")
