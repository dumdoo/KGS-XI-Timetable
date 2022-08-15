from __future__ import annotations
from dataclasses import dataclass
import json
from copy import deepcopy



@dataclass
class Lesson:
    name: str
    location: str

    @classmethod
    def get_lessons(cls, day: str, section: str, optionals: list[str]) -> list[Lesson]:
        with open('data.json') as f:
            data = json.load(f)
        if len(optionals) != 4:
            raise ValueError("All four optionals must be specified")
        if section.upper() not in "KGSTLRMW":
            raise ValueError(f"Invalid section {section}")

        if day in ["SAT", "SUN"]:
            day = "MON"


        lessons = data[day]["lesson-order"]
        for i, lesson in enumerate(data[day]["comp-lessons"]):
            if lesson is None:
                continue
            lessons[i] = lesson[section]

        for i, optional in enumerate(["OPT-A", "OPT-B", "OPT-C", "OPT-D"]):
            if data[day][optional] is not None:
                ii = lessons.index(optional)
                lessons[ii] = [optionals[i], data[day][optional][optionals[i]]]

        return [cls(*lesson) for lesson in lessons]
