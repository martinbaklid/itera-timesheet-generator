from __future__ import annotations

import json
from pathlib import Path

from src.timesheet import Timesheet
from src.timesheet import TimesheetLine


def test_loads_timesheet_from_json(tmp_path: Path) -> None:
    # Arange
    json_file_name = tmp_path / 'sample_week.json'
    timesheet = [
        {
            'legal_entity': '110',
            'project': '11000003.01',
            'activity': 'A110003534',
            'monday_hours': 1,
            'monday_comments': 'Hei mon',
            'tuesday_hours': 2,
            'tuesday_comments': 'Hei tue',
            'wedensday_hours': 3,
            'wedensday_comments': 'Hei wed',
            'thursday_hours': 4,
            'thursday_comments': 'Hei thur',
            'friday_hours': 5,
            'friday_comments': 'Hei fri',
            'saterday_hours': 6,
            'saterday_comments': 'Hei sat',
            'sunday_hours': 7,
            'sunday_comments': 'Hei sun',
        },
    ]
    with open(json_file_name, mode='w') as json_file:
        json.dump(timesheet, json_file)

    # Act
    timesheet = Timesheet.from_json_file(json_file_name)

    # Assert
    expected_timesheet = TimesheetLine(
        legal_entity='110',
        project='11000003.01',
        activity='A110003534',
        monday_hours=1,
        monday_comments='Hei mon',
        tuesday_hours=2,
        tuesday_comments='Hei tue',
        wedensday_hours=3,
        wedensday_comments='Hei wed',
        thursday_hours=4,
        thursday_comments='Hei thur',
        friday_hours=5,
        friday_comments='Hei fri',
        saterday_hours=6,
        saterday_comments='Hei sat',
        sunday_hours=7,
        sunday_comments='Hei sun',
    )
    for timesheet_line in timesheet:
        assert timesheet_line == expected_timesheet
