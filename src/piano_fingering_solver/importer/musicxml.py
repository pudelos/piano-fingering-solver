from fractions import Fraction
from pathlib import Path

from music21 import converter
from music21 import note as music21_note

from piano_fingering_solver.importer.exceptions import MusicXmlImportError
from piano_fingering_solver.importer.validator import MusicXmlValidator
from piano_fingering_solver.models.document import MusicXmlDocument
from piano_fingering_solver.models.melody import Melody
from piano_fingering_solver.models.note import Note


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

        MusicXmlValidator.validate_score(source_score)

        analysis_score = source_score.stripTies(inPlace=False)

        imported_notes: list[Note] = []
        part = analysis_score.parts[0]

        for element in part.flatten().notes:
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

        imported_notes.sort(key=lambda note: note.start)
        MusicXmlValidator.validate_melody(imported_notes)

        return MusicXmlDocument(
            melody=Melody(notes=imported_notes),
            source_score=source_score,
        )
