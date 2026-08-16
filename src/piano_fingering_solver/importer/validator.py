from itertools import pairwise

from music21 import chord as music21_chord
from music21 import harmony as music21_harmony
from music21 import note as music21_note
from music21 import stream

from piano_fingering_solver.importer.exceptions import MusicXmlImportError
from piano_fingering_solver.models.note import Note


class MusicXmlValidator:
    @staticmethod
    def validate_score(source_score: stream.Score) -> None:
        if len(source_score.parts) != 1:
            raise MusicXmlImportError(
                "Only MusicXML files with exactly one part are supported."
            )

        part = source_score.parts[0]
        measures = part.recurse().getElementsByClass("Measure")

        if any(len(measure.voices) > 1 for measure in measures):
            raise MusicXmlImportError("Multiple voices are not supported.")

        MusicXmlValidator._validate_elements(part)

    @staticmethod
    def validate_melody(notes: list[Note]) -> None:
        for previous, current in pairwise(notes):
            if current.start < previous.end:
                raise MusicXmlImportError("Overlapping notes are not supported.")

    @staticmethod
    def _validate_elements(part: stream.Part) -> None:
        for element in part.flatten().notes:
            if isinstance(element, music21_harmony.Harmony):
                continue

            if isinstance(element, music21_chord.Chord):
                raise MusicXmlImportError("Chords are not supported yet.")

            if isinstance(element, music21_note.Unpitched):
                raise MusicXmlImportError("Unpitched notes are not supported.")

            if isinstance(element, music21_note.Note):
                if element.duration.isGrace:
                    raise MusicXmlImportError("Grace notes are not supported.")
                continue

            raise MusicXmlImportError(
                f"Unsupported musical element: {type(element).__name__}"
            )
