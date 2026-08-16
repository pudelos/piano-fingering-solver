import zipfile
from fractions import Fraction

import pytest
from music21 import harmony as music21_harmony
from music21 import note as music21_note
from music21 import stream
from music21 import tie as music21_tie

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


def test_imports_tied_notes_as_single_note(tmp_path):
    source_score = stream.Score()
    part = stream.Part()

    note_a = music21_note.Note(60)
    note_a.quarterLength = 4
    note_a.tie = music21_tie.Tie("start")

    note_b = music21_note.Note(60)
    note_b.quarterLength = 4
    note_b.tie = music21_tie.Tie("stop")

    part.append(note_a)
    part.append(note_b)
    source_score.insert(0, part)

    musicxml_path = tmp_path / "tied.musicxml"
    source_score.write("musicxml", fp=musicxml_path)

    document = MusicXmlImporter().import_file(musicxml_path)

    assert len(document.melody.notes) == 1

    imported_note = document.melody.notes[0]

    assert imported_note.pitch == 60
    assert imported_note.start == Fraction(0)
    assert imported_note.end == Fraction(8)

    assert len(document.source_score.parts) == 1
    assert len(document.source_score.parts[0].flatten().notes) == 2


def test_chord_symbol_is_allowed(tmp_path):
    source_score = stream.Score()
    part = stream.Part()

    chord_symbol = music21_harmony.ChordSymbol("Cmaj7")
    note = music21_note.Note(60)
    note.quarterLength = 1

    part.insert(0, chord_symbol)
    part.insert(0, note)
    source_score.insert(0, part)

    musicxml_path = tmp_path / "chord-symbol.musicxml"
    source_score.write("musicxml", fp=musicxml_path)

    document = MusicXmlImporter().import_file(musicxml_path)

    assert len(document.melody.notes) == 1
    assert document.melody.notes[0].pitch == 60

    chord_symbols = document.source_score.recurse().getElementsByClass(
        music21_harmony.ChordSymbol
    )
    assert len(chord_symbols) == 1
