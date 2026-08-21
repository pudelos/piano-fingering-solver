from copy import deepcopy
from pathlib import Path

from music21 import articulations as music21_articulations
from music21 import note as music21_note

from piano_fingering_solver.exporter.exceptions import MusicXmlExportError
from piano_fingering_solver.formats import MUSICXML_EXTENSIONS
from piano_fingering_solver.models.document import MusicXmlDocument
from piano_fingering_solver.models.fingering import Fingering


class MusicXmlExporter:
    def export_file(
        self, document: MusicXmlDocument, fingering: Fingering, path: str | Path
    ) -> None:
        path = Path(path)

        if path.suffix.lower() not in MUSICXML_EXTENSIONS:
            raise MusicXmlExportError(f"Unsupported file extension: {path.suffix}")

        if len(document.melody_source_notes) != len(fingering.fingers):
            raise MusicXmlExportError(
                "The number of fingers must match the number of melody notes."
            )

        output_document = deepcopy(document)

        source_notes = output_document.source_score.recurse().getElementsByClass(
            music21_note.Note
        )
        for source_note in source_notes:
            source_note.articulations = [
                articulation
                for articulation in source_note.articulations
                if not isinstance(articulation, music21_articulations.Fingering)
            ]

        for source_note, finger in zip(
            output_document.melody_source_notes, fingering.fingers, strict=True
        ):
            source_note.articulations.append(music21_articulations.Fingering(finger))

        try:
            output_document.source_score.write("musicxml", fp=path)
        except Exception as error:
            raise MusicXmlExportError(
                f"Could not export MusicXML file: {path}"
            ) from error
