import zipfile
from pathlib import Path

import pytest
from music21 import articulations as music21_articulations
from music21 import converter, stream
from music21 import note as music21_note
from music21 import tie as music21_tie

from piano_fingering_solver.exporter.musicxml import MusicXmlExporter
from piano_fingering_solver.importer.musicxml import MusicXmlImporter
from piano_fingering_solver.models.fingering import Fingering

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
SAMPLE_FINGERING_NUMBERS = (1, 2, 3, 4, 5, 1)


def _get_notes(score: stream.Score) -> tuple[music21_note.Note, ...]:
    return tuple(score.parts[0].flatten().getElementsByClass(music21_note.Note))


def _get_note_finger_numbers(note: music21_note.Note) -> tuple[int, ...]:
    finger_numbers = tuple(
        articulation.fingerNumber
        for articulation in note.articulations
        if isinstance(
            articulation,
            music21_articulations.Fingering,
        )
    )

    assert len(finger_numbers) <= 1

    return finger_numbers


def _get_finger_numbers(score: stream.Score) -> tuple[int, ...]:
    return tuple(
        finger_number
        for note in _get_notes(score)
        for finger_number in _get_note_finger_numbers(note)
    )


@pytest.mark.parametrize(
    "extension",
    [
        ".xml",
        ".musicxml",
        ".mxl",
    ],
)
def test_exports_fingering(tmp_path, extension):
    document = MusicXmlImporter().import_file(FIXTURES_DIR / "simple.musicxml")
    fingering = Fingering(fingers=SAMPLE_FINGERING_NUMBERS)
    output_path = tmp_path / f"result{extension}"

    MusicXmlExporter().export_file(
        document=document, fingering=fingering, path=output_path
    )

    assert output_path.is_file()

    if extension == ".mxl":
        assert zipfile.is_zipfile(output_path)

    exported_score = converter.parse(output_path)

    assert _get_finger_numbers(exported_score) == SAMPLE_FINGERING_NUMBERS


def test_does_not_modify_source_document(tmp_path):
    document = MusicXmlImporter().import_file(FIXTURES_DIR / "simple.musicxml")
    original_finger_numbers = _get_finger_numbers(document.source_score)

    MusicXmlExporter().export_file(
        document=document,
        fingering=Fingering(fingers=SAMPLE_FINGERING_NUMBERS),
        path=tmp_path / "result.musicxml",
    )

    assert original_finger_numbers == ()
    assert _get_finger_numbers(document.source_score) == original_finger_numbers


def test_replaces_exisiting_fingering(tmp_path):
    document = MusicXmlImporter().import_file(FIXTURES_DIR / "simple.musicxml")

    first_source_note = document.melody_source_notes[0]
    first_source_note.articulations.append(music21_articulations.Staccato())
    first_source_note.articulations.append(music21_articulations.Fingering(5))

    output_path = tmp_path / "result.musicxml"

    MusicXmlExporter().export_file(
        document=document,
        fingering=Fingering(fingers=SAMPLE_FINGERING_NUMBERS),
        path=output_path,
    )

    exported_score = converter.parse(output_path)

    assert _get_finger_numbers(exported_score) == SAMPLE_FINGERING_NUMBERS

    exported_notes = _get_notes(exported_score)

    assert any(
        isinstance(articulation, music21_articulations.Staccato)
        for articulation in exported_notes[0].articulations
    )

    assert _get_finger_numbers(document.source_score) == (5,)


def test_exports_fingering_on_first_tied_note(tmp_path):
    source_score = stream.Score()
    part = stream.Part()

    first_note = music21_note.Note("C4")
    first_note.quarterLength = 1
    first_note.tie = music21_tie.Tie("start")

    second_note = music21_note.Note("C4")
    second_note.quarterLength = 1
    second_note.tie = music21_tie.Tie("stop")

    part.append(first_note)
    part.append(second_note)
    source_score.insert(0, part)

    input_path = tmp_path / "input.musicxml"
    output_path = tmp_path / "output.musicxml"

    source_score.write("musicxml", fp=input_path)

    document = MusicXmlImporter().import_file(input_path)

    assert len(document.melody.notes) == 1

    MusicXmlExporter().export_file(
        document=document,
        fingering=Fingering(fingers=(3,)),
        path=output_path,
    )

    exported_score = converter.parse(output_path)
    exported_notes = _get_notes(exported_score)

    assert len(exported_notes) == 2
    assert exported_notes[0].tie.type == "start"
    assert exported_notes[1].tie.type == "stop"

    assert _get_note_finger_numbers(exported_notes[0]) == (3,)
    assert _get_note_finger_numbers(exported_notes[1]) == ()
