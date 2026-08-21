from pathlib import Path

import pytest

from piano_fingering_solver.exporter.exceptions import MusicXmlExportError
from piano_fingering_solver.exporter.musicxml import MusicXmlExporter
from piano_fingering_solver.importer.musicxml import MusicXmlImporter
from piano_fingering_solver.models.fingering import Fingering

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
SAMPLE_FINGERING_NUMEBRS = (1, 2, 3, 4, 5, 1)


def test_rejects_incorrect_number_of_fingers(tmp_path):
    document = MusicXmlImporter().import_file(FIXTURES_DIR / "simple.musicxml")

    with pytest.raises(MusicXmlExportError):
        MusicXmlExporter().export_file(
            document=document,
            fingering=Fingering(fingers=(2, 3)),
            path=tmp_path / "result.musicxml",
        )


def test_rejects_unsupported_extension(tmp_path):
    document = MusicXmlImporter().import_file(FIXTURES_DIR / "simple.musicxml")

    with pytest.raises(MusicXmlExportError):
        MusicXmlExporter().export_file(
            document=document,
            fingering=Fingering(fingers=SAMPLE_FINGERING_NUMEBRS),
            path=tmp_path / "result.pdf",
        )


def test_raises_export_error_when_file_write_fails(tmp_path):
    document = MusicXmlImporter().import_file(FIXTURES_DIR / "simple.musicxml")
    wrong_output_path = tmp_path / "missing_directory" / "result.musicxml"

    with pytest.raises(MusicXmlExportError):
        MusicXmlExporter().export_file(
            document=document,
            fingering=Fingering(fingers=SAMPLE_FINGERING_NUMEBRS),
            path=wrong_output_path,
        )
