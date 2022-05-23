from __future__ import annotations

import re
from collections import defaultdict
from datetime import datetime

from toggl.TogglPy import Toggl

from src.timesheet import Timesheet
from src.timesheet import TimesheetLine
from src.timesheet import TimesheetPeriod


class TogglTimesheetLine:

    def __init__(self) -> None:
        self.project_name = ''
        self.description = ''
        self.project_id = 0
        self.activity_id = 0
        self.duration = [0, 0, 0, 0, 0, 0, 0]

    def add_for_weekday(self, duration_ms: int, weekday: int) -> None:
        assert weekday <= 6
        if duration_ms == 0:
            return
        duration = round(duration_ms / 1000 / 60 / 60, ndigits=1)
        self.duration[weekday] += duration

    def __repr__(self) -> str:
        return f'{self.project_name=}, {self.description=}, {self.duration=}'


def _parse_proj_and_act_id(project_name):
    if matches := re.match(r'^\[(.*)-(.*)\]', project_name):
        project_id = matches.group(1)
        activity_id = matches.group(2)
    return project_id, activity_id


class ToggleTimesheet:

    def __init__(self, toggl_api_key, workspace_name) -> None:
        self.toggl = Toggl()
        self.toggl.setAPIKey(toggl_api_key)
        self.workspace_name = workspace_name

    def get_timesheet(
        self,
        timesheet_period: TimesheetPeriod,
        group_by_func,
        create_description_func=lambda group: group[0]['description'],
    ) -> Timesheet:
        timesheet_lines = self._toggl_timesheet_lines(
            timesheet_period,
            group_by_func,
            create_description_func,
        )
        timesheet = Timesheet()
        for summary in timesheet_lines:
            description = summary.description
            duration = summary.duration
            timesheet_line = TimesheetLine(
                legal_entity=110,
                project=summary.project_id,
                activity=summary.activity_id,
                monday_hours=duration[0],
                tuesday_hours=duration[1],
                wedensday_hours=duration[2],
                thursday_hours=duration[3],
                friday_hours=duration[4],
                saterday_hours=duration[5],
                sunday_hours=duration[6],
                monday_comments=description if duration[0] else '',
                tuesday_comments=description if duration[1] else '',
                wedensday_comments=description if duration[2] else '',
                thursday_comments=description if duration[3] else '',
                friday_comments=description if duration[4] else '',
                saterday_comments=description if duration[5] else '',
                sunday_comments=description if duration[6] else '',
            )
            timesheet.append(timesheet_line)
        return timesheet

    def _toggl_timesheet_lines(
        self,
        timesheet_period: TimesheetPeriod,
        group_by_func,
        create_description_func=lambda group: group[0]['description'],
    ) -> list[TimesheetLine]:

        groups: dict[str, list[dict]] = defaultdict(list)
        for entry in self._get_weekly_report(timesheet_period):
            groups[group_by_func(entry)].append(entry)

        timesheet_lines = []
        for group_name, group in groups.items():
            timesheet_line = TogglTimesheetLine()
            project_id, activity_id = _parse_proj_and_act_id(group_name)
            timesheet_line.project_id = project_id
            timesheet_line.activity_id = activity_id
            timesheet_line.description = create_description_func(group)
            for entry in group:
                weekday = datetime.fromisoformat(entry['start']).weekday()
                timesheet_line.add_for_weekday(entry['dur'], weekday)
            timesheet_lines.append(timesheet_line)
        return timesheet_lines

    def _get_weekly_report(self, timesheet_period: TimesheetPeriod):
        workspace = self.toggl.getWorkspace(
            name=self.workspace_name,
        )
        return self.toggl.getDetailedReport({
            'workspace_id': workspace['id'],
            'since': timesheet_period.start,
            'until': timesheet_period.end,
        })['data']
