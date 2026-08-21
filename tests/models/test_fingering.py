import pytest

from piano_fingering_solver.models.fingering import Fingering


@pytest.mark.parametrize(
    "finger",
    [
        True,
        False,
        1.0,
        "1",
    ],
)
def test_rejects_non_integer_finger_number(finger):
    with pytest.raises(TypeError):
        Fingering(fingers=(finger,))


@pytest.mark.parametrize(
    "finger",
    [-1, 0, 6],
)
def test_rejects_finger_number_outside_valid_range(finger):
    with pytest.raises(ValueError):
        Fingering(fingers=(finger,))


@pytest.mark.parametrize(
    "finger",
    [1, 2, 3, 4, 5],
)
def test_accepts_valid_finger_number(finger):
    fingering = Fingering(fingers=(finger,))
    assert fingering.fingers == (finger,)
