from fractions import Fraction
from pathlib import Path

from music21 import chord as music21_chord
from music21 import converter
from music21 import note as music21_note

from piano_fingering_solver.core.melody import Melody
from piano_fingering_solver.core.note import Note
from piano_fingering_solver.importer.document import MusicXmlDocument
from piano_fingering_solver.importer.exceptions import MusicXmlImportError


class MusicXmlImporter:
    SUPPORTED_EXTENSIONS = frozenset(
        {
            ".musicxml",
            ".xml",
            ".mxl",
        }
    )

    def import_file(self, path: str | Path) -> MusicXmlDocument:
        path = Path(path)

        if not path.is_file():
            raise MusicXmlImportError(f"MusicXML file not found: {path}")

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise MusicXmlImportError(f"Unsupported file extension: {path.suffix}")

        try:
            source_score = converter.parse(path)
        except Exception as error:
            raise MusicXmlImportError(
                f"Could not parse MusicXML file: {path}"
            ) from error

        if len(source_score.parts) != 1:
            raise MusicXmlImportError(
                "Only MusicXML files with exactly one part are supported."
            )

        imported_notes: list[Note] = []
        part = source_score.parts[0]

        for element in part.flatten().notes:
            if isinstance(element, music21_chord.Chord):
                raise MusicXmlImportError("Chords are not supported yet.")

            if not isinstance(element, music21_note.Note):
                continue

            start = Fraction(str(element.offset))
            duration = Fraction(str(element.quarterLength))
            end = start + duration

            imported_notes.append(
                Note(
                    start=start,
                    end=end,
                    pitch=element.pitch.midi,
                )
            )

        return MusicXmlDocument(
            melody=Melody(notes=imported_notes),
            source_score=source_score,
        )
