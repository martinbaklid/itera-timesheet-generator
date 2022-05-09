from __future__ import annotations

from dataclasses import astuple
from dataclasses import dataclass
from dataclasses import fields
from pathlib import Path
from typing import Any
from typing import Iterable

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from src.timesheet import Timesheet
from src.timesheet import TimesheetLine


@dataclass
class _IteraTimesheetLine:
    LineNum: int
    ProjectDataAreaId: str
    ProjId: str
    ACTIVITYNUMBER: str
    HOURS: float
    Hours2_: float
    Hours3_: float
    Hours4_: float
    Hours5_: float
    Hours6_: float
    Hours7_: float
    EXTERNALCOMMENTS: str
    ExternalComments2_: str
    ExternalComments3_: str
    ExternalComments4_: str
    ExternalComments5_: str
    ExternalComments6_: str
    ExternalComments7_: str

    def as_tuple(self) -> tuple[Any, ...]:
        return astuple(self)

    @staticmethod
    def column_names() -> list[str]:
        return [field.name for field in fields(_IteraTimesheetLine)]

    @staticmethod
    def from_timesheet_line(
        line_number: int,
        timesheet_line: TimesheetLine,
    ) -> _IteraTimesheetLine:
        return _IteraTimesheetLine(
            LineNum=line_number,
            ProjectDataAreaId=timesheet_line.legal_entity,
            ProjId=timesheet_line.project,
            ACTIVITYNUMBER=timesheet_line.activity,
            HOURS=timesheet_line.monday_hours,
            Hours2_=timesheet_line.tuesday_hours,
            Hours3_=timesheet_line.wedensday_hours,
            Hours4_=timesheet_line.thursday_hours,
            Hours5_=timesheet_line.friday_hours,
            Hours6_=timesheet_line.saterday_hours,
            Hours7_=timesheet_line.sunday_hours,
            EXTERNALCOMMENTS=timesheet_line.monday_comments,
            ExternalComments2_=timesheet_line.tuesday_comments,
            ExternalComments3_=timesheet_line.wedensday_comments,
            ExternalComments4_=timesheet_line.thursday_comments,
            ExternalComments5_=timesheet_line.friday_comments,
            ExternalComments6_=timesheet_line.saterday_comments,
            ExternalComments7_=timesheet_line.sunday_comments,
        )


class _IteraTimesheetWorkbook:

    def __init__(
        self,
        timesheet_lines: Iterable[_IteraTimesheetLine] = (),
    ) -> None:
        self._workbook: Workbook = Workbook()
        self._append_header()
        self._extend(timesheet_lines)

    def save(self, filename: Path) -> None:
        if filename.suffix != '.xlsx':
            raise ValueError(
                'Can only save timesheet to filename with extension .xlsx',
            )
        self._workbook.save(filename)

    @property
    def _worksheet(self) -> Worksheet:
        return self._workbook.active

    def _append_header(self) -> None:
        self._worksheet.append(_IteraTimesheetLine.column_names())

    def _extend(self, timesheet_lines: Iterable[_IteraTimesheetLine]) -> None:
        for timesheet_line in timesheet_lines:
            self._worksheet.append(timesheet_line.as_tuple())

    @staticmethod
    def from_timesheet(timesheet: Timesheet) -> _IteraTimesheetWorkbook:
        timesheet_lines = [
            _IteraTimesheetLine.from_timesheet_line(
                line_number, line,
            ) for line_number, line in enumerate(timesheet, start=1)
        ]
        return _IteraTimesheetWorkbook(timesheet_lines)
