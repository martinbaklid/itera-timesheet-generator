from collections import OrderedDict
from time import time
from openpyxl import Workbook
import json
import sys

DYNAMICS_KEY_ORDERED_MAPPING = OrderedDict({
    "line_number": "LineNum",
    "legal_entity": "ProjectDataAreaId",
    "project": "ProjId",
    "activity": "ACTIVITYNUMBER",
    "monday_hours": "HOURS",
    "tuesday_hours": "Hours2_",
    "wedensday_hours": "Hours3_",
    "thursday_hours": "Hours4_",
    "friday_hours": "Hours5_",
    "saterday_hours": "Hours6_",
    "sunday_hours": "Hours7_",
    "monday_comments": "EXTERNALCOMMENTS",
    "tuesday_comments": "ExternalComments2_",
    "wedensday_comments": "ExternalComments3_",
    "thursday_comments": "ExternalComments4_",
    "friday_comments": "ExternalComments5_",
    "saterday_comments": "ExternalComments6_",
    "sunday_comments": "ExternalComments7_",
})

class TimeSheet:
    
    def __init__(self) -> None:
        self._lines = []

    def add_all(self, lines: list) -> None:
        for line in lines:
            self._lines.append(line)
                
    def save(self, name: str) -> None:
        wb = Workbook()
        ws = wb.active
        ws.append(list(DYNAMICS_KEY_ORDERED_MAPPING.values()))
        for i, line in enumerate(self._lines, start=1):
            line["line_number"] = i
            ws.append([line[k] for k in DYNAMICS_KEY_ORDERED_MAPPING])
        wb.save(name)

def _read_json_timesheet(filename):
    with open(sys.argv[1]) as fp:
        return json.load(fp)
    
def main():
    json_file = sys.argv[1]
    excel_file = sys.argv[2]

    timesheet = TimeSheet()
    timesheet.add_all(_read_json_timesheet(json_file))
    timesheet.save(excel_file)

if __name__ == "__main__":
    main()
