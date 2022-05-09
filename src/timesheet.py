from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


@dataclass
class TimesheetLine:
    legal_entity: str
    project: str
    activity: str
    monday_hours: float = 0
    tuesday_hours: float = 0
    wedensday_hours: float = 0
    thursday_hours: float = 0
    friday_hours: float = 0
    saterday_hours: float = 0
    sunday_hours: float = 0
    monday_comments: str = ''
    tuesday_comments: str = ''
    wedensday_comments: str = ''
    thursday_comments: str = ''
    friday_comments: str = ''
    saterday_comments: str = ''
    sunday_comments: str = ''


class Timesheet:

    def __init__(self, timesheet_lines: list[TimesheetLine] = []) -> None:
        self._timesheet_lines: list[TimesheetLine] = timesheet_lines

    def __iter__(self) -> Iterator[TimesheetLine]:
        return iter(self._timesheet_lines)

    def append(self, timesheet_line: TimesheetLine) -> None:
        self._timesheet_lines.append(timesheet_line)

    @staticmethod
    def from_json_file(filename: Path) -> Timesheet:
        with open(filename) as fp:
            timesheet = json.load(fp)
            lines = [TimesheetLine(**line) for line in timesheet]
            return Timesheet(lines)
