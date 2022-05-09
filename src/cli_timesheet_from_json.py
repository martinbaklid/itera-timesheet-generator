from __future__ import annotations

import sys
from pathlib import Path

from src.itera_timesheet_workbook import _IteraTimesheetWorkbook
from src.timesheet import Timesheet


def main() -> None:
    json_file = Path(sys.argv[1])
    xlsx_file = Path(sys.argv[2])
    timesheet = Timesheet.from_json_file(json_file)
    timesheet_workbook = _IteraTimesheetWorkbook.from_timesheet(timesheet)
    timesheet_workbook.save(xlsx_file)


if __name__ == '__main__':
    main()
