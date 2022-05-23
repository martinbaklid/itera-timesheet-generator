from __future__ import annotations

import argparse
from pathlib import Path

from src.itera_timesheet_workbook import _IteraTimesheetWorkbook
from src.timesheet import Timesheet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'json_file',
        type=Path,
        help='The json file to generate timesheet from',
    )
    parser.add_argument(
        'xlsx_file',
        type=Path,
        help='The output xlsx file (itera dynamics xlsx timesheet)',
    )
    parser.parse_args()

    timesheet = Timesheet.from_json_file(parser.json_file)
    timesheet_workbook = _IteraTimesheetWorkbook.from_timesheet(timesheet)
    timesheet_workbook.save(parser.xlsx_file)


if __name__ == '__main__':
    main()
