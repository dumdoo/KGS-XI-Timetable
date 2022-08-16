from __future__ import annotations
from dataclasses import dataclass
import json
from copy import deepcopy


@dataclass
class Lesson:
    name: str
    location: str

    @classmethod
    def get_lessons(
        cls, day: str, section: str, optionals: list[str], remedial_urdu: bool = False
    ) -> list[Lesson]:
        with open("data.json") as f:
            data = json.load(f)
        if len(optionals) != 4:
            raise ValueError("All four optionals must be specified")
        if section.upper() not in "KGSTLRMW":
            raise ValueError(f"Invalid section {section}")

        if day in ["SAT", "SUN"]:
            day = "MON"

        lessons = data[day]["lesson-order"]
        for i, lesson_map in enumerate(data[day]["comp-lessons"]):
            if lesson_map is None:
                continue

            lesson = lesson_map[section]
            if remedial_urdu and lesson[0].upper() == "URDU":
                lesson = lesson_map["RC"]

            lessons[i] = lesson

        for opt, optional in zip(["OPT-A", "OPT-B", "OPT-C", "OPT-D"], optionals):
            if opt not in lessons:
                continue
            i = lessons.index(opt)
            opt_list = data[opt]
            lessons[i] = [optional, opt_list[optional]]

        return [cls(*lesson) for lesson in lessons]
