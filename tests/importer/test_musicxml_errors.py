from pathlib import Path

import pytest
from music21 import chord as music21_chord
from music21 import note as music21_note
from music21 import stream

from piano_fingering_solver.importer.exceptions import MusicXmlImportError
from piano_fingering_solver.importer.musicxml import MusicXmlImporter

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


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


def test_multiple_parts_is_rejected(tmp_path):
    source_score = stream.Score()

    first_part = stream.Part()
    first_note = music21_note.Note("C4")
    first_note.quarterLength = 1
    first_part.append(first_note)

    second_part = stream.Part()
    second_note = music21_note.Note("E4")
    second_note.quarterLength = 1
    second_part.append(second_note)

    source_score.insert(0, first_part)
    source_score.insert(0, second_part)

    musicxml_path = tmp_path / "multiple-parts.musicxml"
    source_score.write("musicxml", fp=musicxml_path)

    with pytest.raises(MusicXmlImportError):
        MusicXmlImporter().import_file(musicxml_path)


def test_multiple_voices_is_rejected(tmp_path):
    source_score = stream.Score()
    part = stream.Part()

    first_voice = stream.Voice(id="1")
    first_note = music21_note.Note("C4")
    first_note.quarterLength = 1
    first_voice.append(first_note)

    second_voice = stream.Voice(id="2")
    second_note = music21_note.Note("G3")
    second_note.quarterLength = 1
    second_voice.append(second_note)

    part.insert(0, first_voice)
    part.insert(0, second_voice)
    source_score.insert(0, part)

    musicxml_path = tmp_path / "multiple-voices.musicxml"
    source_score.write("musicxml", fp=musicxml_path)

    with pytest.raises(MusicXmlImportError):
        MusicXmlImporter().import_file(musicxml_path)


def test_overlapping_notes_is_rejected():
    path = FIXTURES_DIR / "overlapping.musicxml"

    with pytest.raises(MusicXmlImportError):
        MusicXmlImporter().import_file(path)
