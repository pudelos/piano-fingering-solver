import zipfile
from fractions import Fraction

import pytest
from music21 import note as music21_note
from music21 import stream

from piano_fingering_solver.importer.musicxml import MusicXmlImporter


@pytest.mark.parametrize("extension", [".xml", ".musicxml", ".mxl"])
@pytest.mark.parametrize(
    "pitches",
    [
        ["C4"],
        ["C4", "D4", "E4", "C2", "C4"],
    ],
)
def test_imports_notes(tmp_path, extension, pitches):
    source_score = stream.Score()
    part = stream.Part()

    for pitch in pitches:
        source_note = music21_note.Note(pitch)
        source_note.quarterLength = 1
        part.append(source_note)

    source_score.insert(0, part)

    musicxml_path = tmp_path / f"score{extension}"
    source_score.write("musicxml", fp=musicxml_path)

    if extension == ".mxl":
        assert zipfile.is_zipfile(musicxml_path)

    document = MusicXmlImporter().import_file(musicxml_path)

    assert isinstance(document.source_score, stream.Score)

    melody = document.melody

    assert len(melody.notes) == len(pitches)

    for index, imported_note in enumerate(melody.notes):
        assert imported_note.pitch == music21_note.Note(pitches[index]).pitch.midi
        assert imported_note.start == Fraction(index)
        assert imported_note.end == Fraction(index + 1)
