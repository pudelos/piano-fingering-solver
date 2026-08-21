from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Fingering:
    fingers: tuple[int, ...]

    def __post_init__(self) -> None:
        if any(
            not isinstance(finger, int) or isinstance(finger, bool)
            for finger in self.fingers
        ):
            raise TypeError("Finger numbers must be integers.")

        if any(finger not in range(1, 6) for finger in self.fingers):
            raise ValueError("Finger numbers must be between 1 and 5.")
