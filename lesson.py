from dataclasses import dataclass

@dataclass(frozen=True)
class Lesson:
    name: str
    location: str