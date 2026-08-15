from fractions import Fraction
from pathlib import Path

from piano_fingering_solver.core.note import Note
from piano_fingering_solver.importer.musicxml import MusicXmlImporter

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def test_imports_real_musicxml_file():
    path = FIXTURES_DIR / "simple.musicxml"

    document = MusicXmlImporter().import_file(path)

    assert document.melody.notes == [
        Note(Fraction(0), Fraction(1, 2), 67),
        Note(Fraction(1, 2), Fraction(5, 4), 65),
        Note(Fraction(5, 4), Fraction(3, 2), 64),
        Note(Fraction(3, 2), Fraction(2), 64),
        Note(Fraction(2), Fraction(9, 4), 71),
        Note(Fraction(9, 4), Fraction(5, 2), 67),
    ]

    assert len(document.source_score.parts) == 1
