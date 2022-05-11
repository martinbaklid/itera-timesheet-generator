from __future__ import annotations

import argparse
import os
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from datetime import datetime
from datetime import timedelta
from pathlib import Path

from toggl.TogglPy import Toggl

from src.itera_timesheet_workbook import _IteraTimesheetWorkbook
from src.timesheet import Timesheet
from src.timesheet import TimesheetLine


@dataclass
class TimesheetPeriod:
    start: date
    end: date

    @classmethod
    def this_week(cls) -> TimesheetPeriod:
        today = date.today()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return cls(start, end)

    @classmethod
    def last_week(cls) -> TimesheetPeriod:
        today = date.today()
        start = today - timedelta(days=today.weekday() + 7)
        end = start + timedelta(days=6)
        return cls(start, end)

    @classmethod
    def from_name(cls, name: str) -> TimesheetPeriod:
        return {
            'this_week': cls.this_week,
            'last_week': cls.last_week,
        }[name]()


class WeeklySummary:

    def __init__(self) -> None:
        self.project_name = ''
        self.description = ''
        self.duration = [0, 0, 0, 0, 0, 0]

    def add_for_weekday(self, duration: int, weekday: int) -> None:
        assert duration < 6
        self.duration[weekday] = duration


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--workspace-name',
        type=str,
        required=True,
    )
    parser.add_argument(
        '--xlsx-output-file',
        type=Path,
        required=True,
    )
    parser.add_argument(
        '--toggl-api-key',
        default=os.environ['TIMESHEET_TOGGL_API_KEY'],
    )
    week_group = parser.add_mutually_exclusive_group()
    week_group.add_argument(
        '--this-week',
        action='store_const',
        const='this_week',
        dest='period',
    )
    week_group.add_argument(
        '--last-week',
        action='store_const',
        const='last_week',
        dest='period',
    )
    args = parser.parse_args()

    toggl_api_key = args.toggl_api_key
    timesheet_period = TimesheetPeriod.from_name(args.period or 'this_week')
    workspace_name = args.workspace_name
    xlsx_file = args.xlsx_output_file

    toggl = Toggl()
    toggl.setAPIKey(toggl_api_key)
    workspace = toggl.getWorkspace(name=workspace_name)
    response = toggl.getDetailedReport({
        'workspace_id': workspace['id'],
        'since': timesheet_period.start,
        'until': timesheet_period.end,
    })['data']
    weekly_report = response['data']

    summary_by_proj_desc: dict[str, WeeklySummary] = defaultdict(WeeklySummary)
    for entry in weekly_report:
        group_key = f"{entry['project']}-{entry['description']}"
        summary = summary_by_proj_desc[group_key]
        weekday = datetime.fromisoformat(entry['start']).weekday()
        summary.add_for_weekday(entry['dur'], weekday)
        summary.project_name = entry['project']
        summary.description = entry['description']

    timesheet = Timesheet()
    for summary in summary_by_proj_desc.values():
        if matches := re.match(r'^\[(.*)-(.*)\]', summary.project_name):
            project_id = matches.group(1)
            activity_id = matches.group(2)
        else:
            raise ValueError(
                'Project names in toggl need to be prefixed with '
                '[<project_id>-<activitiy_id>]',
            )
        day_totals = [
            0 if ms is None else round(ms / 1000 / 60 / 60, ndigits=1)
            for ms in entry['dur']
        ]
        timesheet_line = TimesheetLine(
            legal_entity=110,
            project=project_id,
            activity=activity_id,
            monday_hours=day_totals[0],
            tuesday_hours=day_totals[1],
            wedensday_hours=day_totals[2],
            thursday_hours=day_totals[3],
            friday_hours=day_totals[4],
            saterday_hours=day_totals[5],
            sunday_hours=day_totals[6],
            monday_comments=summary.description if day_totals[0] else '',
            tuesday_comments=summary.description if day_totals[1] else '',
            wedensday_comments=summary.description if day_totals[2] else '',
            thursday_comments=summary.description if day_totals[3] else '',
            friday_comments=summary.description if day_totals[4] else '',
            saterday_comments=summary.description if day_totals[5] else '',
            sunday_comments=summary.description if day_totals[6] else '',
        )
        timesheet.append(timesheet_line)
    workbook = _IteraTimesheetWorkbook.from_timesheet(timesheet)
    workbook.save(xlsx_file)


if __name__ == '__main__':
    main()
