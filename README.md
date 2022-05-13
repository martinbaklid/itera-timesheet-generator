# Itera Timesheet Generator
## Instalation
`pip install git+https://github.com/martinbaklid/itera-timesheet-generator.git`

## CLI

### `timesheet-from-json` JSON_TIMESHEET XLSX_TIMESHEET
Arguments:
 - `JSON_TIMESHEET`: the input timesheet in json format

```shell
timesheet-from-json <json timesheet>.json <xslx file>.xlsx
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
Example:
`timesheet-from-toggl --toggl-api-key <key> --this-week --workspace-name "Itera 2022" --xlsx-output-file 2022-05-13.xlsx`
