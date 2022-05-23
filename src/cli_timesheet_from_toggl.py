from __future__ import annotations

import argparse
import os
from pathlib import Path

from src.itera_timesheet_workbook import _IteraTimesheetWorkbook
from src.timesheet import TimesheetPeriod
from src.toggl import ToggleTimesheet


def _group_by_project(entry: dict[any]) -> str:
    return f"{entry['project']}"


def _group_by_project_and_description(entry: dict[any]) -> str:
    return f"{entry['project']}-{entry['description']}"


_group_by_func_for = {
    'project': _group_by_project,
    'project_and_description': _group_by_project_and_description,
}


def _no_description(group) -> str:
    return ''


def _first_description(group) -> str:
    return group[0]['description']


_description_func_for = {
    'project': _no_description,
    'project_and_description': _first_description,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--workspace-name',
        type=str,
        required=True,
        help='Toggl workspace name to use',
    )
    parser.add_argument(
        '--xlsx-output-file',
        type=Path,
        required=True,
        help='The output xlsx file (itera dynamics xlsx timesheet)',
    )
    parser.add_argument(
        '--toggl-api-key',
        default=os.environ['TIMESHEET_TOGGL_API_KEY'],
        help='The toggl api key (see tinyurl.com/toggl-api-key)',
    )
    week_group = parser.add_mutually_exclusive_group()
    week_group.add_argument(
        '--this-week',
        action='store_const',
        const='this_week',
        dest='period',
        help='Generate timesheet for this week (default)',
    )
    week_group.add_argument(
        '--last-week',
        action='store_const',
        const='last_week',
        dest='period',
        help='Generate timesheet for last week',
    )
    group_by = parser.add_mutually_exclusive_group()
    group_by.add_argument(
        '--group-by-project-and-description',
        action='store_const',
        const='project_and_description',
        dest='group_by',
        help='Group time entires by toggl project name '
        'and the toggl descriptions',
    )
    group_by.add_argument(
        '--group-by-project',
        action='store_const',
        const='project',
        dest='group_by',
        help='Group time entries by toggl project name '
        '(note: this will not create timesheet comments)',
    )
    args = parser.parse_args()

    toggl_api_key = args.toggl_api_key
    timesheet_period = TimesheetPeriod.from_name(args.period or 'this_week')
    workspace_name = args.workspace_name
    xlsx_file = args.xlsx_output_file
    group_key_func = _group_by_func_for[
        args.group_by or 'project_and_description'
    ]
    description_func = _description_func_for[
        args.group_by or 'project_and_description'
    ]

    toggl_timesheet = ToggleTimesheet(toggl_api_key, workspace_name)
    timesheet = toggl_timesheet.get_timesheet(
        timesheet_period,
        group_key_func,
        description_func,
    )
    workbook = _IteraTimesheetWorkbook.from_timesheet(timesheet)
    workbook.save(xlsx_file)


if __name__ == '__main__':
    main()
