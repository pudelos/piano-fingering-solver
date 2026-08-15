import pytest
from music21 import chord as music21_chord
from music21 import note as music21_note
from music21 import stream

from piano_fingering_solver.importer.exceptions import MusicXmlImportError
from piano_fingering_solver.importer.musicxml import MusicXmlImporter


def test_missing_file(tmp_path):
    missing_path = tmp_path / "does-not-exist.musicxml"

    with pytest.raises(MusicXmlImportError):
        MusicXmlImporter().import_file(missing_path)


def test_unsupported_file_extension(tmp_path):
    invalid_path = tmp_path / "score.pdf"
    invalid_path.touch()

    with pytest.raises(MusicXmlImportError):
        MusicXmlImporter().import_file(invalid_path)


def test_invalid_musicxml_content(tmp_path):
    invalid_path = tmp_path / "invalid.musicxml"
    invalid_path.write_text("This is not a MusicXML file.")

    with pytest.raises(MusicXmlImportError):
        MusicXmlImporter().import_file(invalid_path)


def test_chord_is_rejected(tmp_path):
    source_score = stream.Score()
    part = stream.Part()

    source_note = music21_note.Note("E")
    source_note.quarterLength = 1
    part.append(source_note)

    source_chord = music21_chord.Chord(["D", "F#", "A"])
    source_chord.quarterLength = 1
    part.append(source_chord)

    source_score.insert(0, part)

    musicxml_path = tmp_path / "score.musicxml"
    source_score.write("musicxml", fp=musicxml_path)

    with pytest.raises(MusicXmlImportError):
        MusicXmlImporter().import_file(musicxml_path)
