from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from toggl.TogglPy import Toggl

from src.itera_timesheet_workbook import _IteraTimesheetWorkbook
from src.timesheet import Timesheet
from src.timesheet import TimesheetLine


def main() -> None:
    toggl_api_key = os.environ['TIMESHEET_TOGGL_API_KEY']
    workspace_name = sys.argv[1]
    xlsx_file = Path(sys.argv[2])

    toggl = Toggl()
    toggl.setAPIKey(toggl_api_key)
    workspace = toggl.getWorkspace(name=workspace_name)
    data = {
        'workspace_id': workspace['id'],
        'since': '2022-05-02',
    }
    weekly_report = toggl.getWeeklyReport(data)
    report = weekly_report['data']
    timesheet = Timesheet()
    for project_report in report:
        project_name = project_report['title']['project']

        if matches := re.match(r'^\[(.*)-(.*)\]', project_name):
            project_id = matches.group(1)
            activity_id = matches.group(2)
        else:
            raise ValueError(
                'Project names in toggl need to be prefixed with '
                '[<project_id>-<activitiy_id>]',
            )
        day_totals = [
            0 if ms is None else round(ms / 1000 / 60 / 60, ndigits=1)
            for ms in project_report['totals']
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
        )
        timesheet.append(timesheet_line)
    workbook = _IteraTimesheetWorkbook.from_timesheet(timesheet)
    workbook.save(xlsx_file)


if __name__ == '__main__':
    main()
