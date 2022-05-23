# Itera Timesheet Generator
## Instalation
`pip install git+https://github.com/martinbaklid/itera-timesheet-generator.git`

## CLI

### `timesheet-from-json` JSON_TIMESHEET XLSX_TIMESHEET
```
usage: timesheet-from-json [-h] json_file xlsx_file

positional arguments:
  json_file   The json file to generate timesheet from
  xlsx_file   The output xlsx file (itera dynamics xlsx timesheet)

optional arguments:
  -h, --help  show this help message and exit
```

Example json file:
``` json
[
    {
        "legal_entity": "str",
        "project": "str",
        "activity": "str",
        "monday_hours": 0,
        "tuesday_hours": 0,
        "wedensday_hours": 0,
        "thursday_hours": 0,
        "friday_hours": 0,
        "saterday_hours": 0,
        "sunday_hours": 0,
        "monday_comments": "str",
        "tuesday_comments": "str",
        "wedensday_comments": "str",
        "thursday_comments": "str",
        "friday_comments": "str",
        "saterday_comments": "str",
        "sunday_comments": "str"
    }
]
```

### `timesheet-from-toggl`
```
usage: timesheet-from-toggl [-h] --workspace-name WORKSPACE_NAME --xlsx-output-file XLSX_OUTPUT_FILE [--toggl-api-key TOGGL_API_KEY] [--this-week | --last-week]
                            [--group-by-project-and-description | --group-by-project]

optional arguments:
  -h, --help            show this help message and exit
  --workspace-name WORKSPACE_NAME
                        Toggl workspace name to use
  --xlsx-output-file XLSX_OUTPUT_FILE
                        The output xlsx file (itera dynamics xlsx timesheet)
  --toggl-api-key TOGGL_API_KEY
                        The toggl api key (see tinyurl.com/toggl-api-key)
  --this-week           Generate timesheet for this week (default)
  --last-week           Generate timesheet for last week
  --group-by-project-and-description
                        Group time entires by toggl project name and the toggl descriptions
  --group-by-project    Group time entries by toggl project name (note: this will not create timesheet comments)
```
