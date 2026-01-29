# Reminders

> An example reminder:

```
{
  "id": "6X7Vfq5rqPMM5j5q",
  "notify_uid": "2671355",
  "item_id": "6RP2hmPwM3q4WGfW",
  "type": "absolute",
  "due": {
    "date": "2016-08-05T07:00:00.000000Z",
    "timezone": null,
    "is_recurring": false,
    "string": "tomorrow at 10:00",
    "lang": "en"
  },
  "minute_offset": 180,
  "is_deleted": false
}
```

_Availability of reminders functionality and the maximum number of stored reminders are dependent
on the current user plan. These values are indicated by the `reminders`, `max_reminders_time` and
`max_reminders_location` properties of the [user plan limits](#tag/Sync/User/User-plan-limits) object._

#### Properties

| Property                | Description                                                                                                                                                                                                                   |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id _String_             | The ID of the reminder.                                                                                                                                                                                                       |
| notify_uid _String_     | The user ID which should be notified of the reminder, typically the current user ID creating the reminder.                                                                                                                    |
| item_id _String_        | The item ID for which the reminder is about.                                                                                                                                                                                  |
| type _String_           | The type of the reminder: `relative` for a time-based reminder specified in minutes from now, `absolute` for a time-based reminder with a specific time and date in the future, and `location` for a location-based reminder. |
| due _Object_            | The due date of the reminder. See the [Due dates](#tag/Due-dates) section for more details. Note that reminders only support due dates with time, since full-day reminders don't make sense.                                  |
| minute_offset _Integer_ | The relative time in minutes before the due date of the item, in which the reminder should be triggered. Note that the item should have a due date with time set in order to add a relative reminder.                         |
| name _String_           | An alias name for the location.                                                                                                                                                                                               |
| loc_lat _String_        | The location latitude.                                                                                                                                                                                                        |
| loc_long _String_       | The location longitude.                                                                                                                                                                                                       |
| loc_trigger _String_    | What should trigger the reminder: `on_enter` for entering the location, or `on_leave` for leaving the location.                                                                                                               |
| radius _Integer_        | The radius around the location that is still considered as part of the location (in meters).                                                                                                                                  |
| is_deleted _Boolean_    | Whether the reminder is marked as deleted (a `true` or `false` value).                                                                                                                                                        |

## Add a reminder

> Example of adding relative reminder:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "reminder_add",
        "temp_id": "e24ad822-a0df-4b7d-840f-83a5424a484a",
        "uuid": "41e59a76-3430-4e44-92b9-09d114be0d49",
        "args": {
            "item_id": "6RP2hmPwM3q4WGfW",
            "minute_offset": 30,
            "type": "absolute"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"41e59a76-3430-4e44-92b9-09d114be0d49": "ok"},
  "temp_id_mapping": {"e24ad822-a0df-4b7d-840f-83a5424a484a": "2992683215"},
  ...
}
```

> Example of adding an absolute reminder:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "reminder_add",
        "temp_id": "952a365e-4965-4113-b4f4-80cdfcada172u",
        "uuid": "e7c8be2d-f484-4852-9422-a9984c58b1cd",
        "args": {
            "item_id": "6RP2hmPwM3q4WGfW",
            "due": {
                "date": "2014-10-15T11:00:00.000000Z"
            },
            "type": "absolute"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"e7c8be2d-f484-4852-9422-a9984c58b1cd": "ok"},
  "temp_id_mapping": {"952a365e-4965-4113-b4f4-80cdfcada172": "2992683215"},
  ...
}
```

> Example of adding a location reminder:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "reminder_add",
        "temp_id": "7ad9609d-579f-4828-95c5-3600acdb2c81",
        "uuid": "830cf409-daba-479c-a624-68eb0c07d01c",
        "args": {
            "item_id": "6RP2hmPwM3q4WGfW",
            "type": "location",
            "name": "Aliados",
            "loc_lat": "41.148581",
            "loc_long":"-8.610945000000015",
            "loc_trigger":"on_enter",
            "radius": 100
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"830cf409-daba-479c-a624-68eb0c07d01c": "ok"},
  "temp_id_mapping": {"7ad9609d-579f-4828-95c5-3600acdb2c81": "2992683215"},
  ...
}
```

Add a new reminder to the user account related to the API credentials.

#### Command arguments

| Argument                | Required | Description                                                                                                                                                                                                                   |
|-------------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| item_id _String_        | Yes      | The item ID for which the reminder is about.                                                                                                                                                                                  |
| type _String_           | Yes      | The type of the reminder: `relative` for a time-based reminder specified in minutes from now, `absolute` for a time-based reminder with a specific time and date in the future, and `location` for a location-based reminder. |
| notify_uid _String_     | No       | The user ID which should be notified of the reminder, typically the current user ID creating the reminder.                                                                                                                    |
| due _Object_            | No       | The due date of the reminder. See the [Due dates](#tag/Due-dates) section for more details. Note that reminders only support due dates with time, since full-day reminders don't make sense.                                  |
| minute_offset _Integer_ | No       | The relative time in minutes before the due date of the item, in which the reminder should be triggered. Note, that the item should have a due date with time set in order to add a relative reminder.                        |
| name _String_           | No       | An alias name for the location.                                                                                                                                                                                               |
| loc_lat _String_        | No       | The location latitude.                                                                                                                                                                                                        |
| loc_long _String_       | No       | The location longitude.                                                                                                                                                                                                       |
| loc_trigger _String_    | No       | What should trigger the reminder: `on_enter` for entering the location, or `on_leave` for leaving the location.                                                                                                               |
| radius _Integer_        | No       | The radius around the location that is still considered as part of the location (in meters).                                                                                                                                  |

## Update a reminder

> Example update reminder request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "reminder_update",
        "uuid": "b0e7562e-ea9f-4c84-87ee-9cbf9c103234",
        "args": {
            "id": "6X7VrXrqjX6642cv",
            "due": {
                "date": "2014-10-10T15:00:00.000000"
            }
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"b0e7562e-ea9f-4c84-87ee-9cbf9c103234": "ok"},
  ...
}
```

Update a reminder from the user account related to the API credentials.

#### Command arguments

| Argument                | Required | Description                                                                                                                                                                                                                   |
|-------------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id _String_             | Yes      | The ID of the reminder.                                                                                                                                                                                                       |
| notify_uid _String_     | No       | The user ID which should be notified of the reminder, typically the current user ID creating the reminder.                                                                                                                    |
| type _String_           | No       | The type of the reminder: `relative` for a time-based reminder specified in minutes from now, `absolute` for a time-based reminder with a specific time and date in the future, and `location` for a location-based reminder. |
| due _Object_            | No       | The due date of the reminder. See the [Due dates](#tag/Due-dates) section for more details. Note that reminders only support due dates with time, since full-day reminders don't make sense.                                  |
| minute_offset _Integer_ | No       | The relative time in minutes before the due date of the item, in which the reminder should be triggered. Note, that the item should have a due date with time set in order to add a relative reminder.                        |
| name _String_           | No       | An alias name for the location.                                                                                                                                                                                               |
| loc_lat _String_        | No       | The location latitude.                                                                                                                                                                                                        |
| loc_long _String_       | No       | The location longitude.                                                                                                                                                                                                       |
| loc_trigger _String_    | No       | What should trigger the reminder: `on_enter` for entering the location, or `on_leave` for leaving the location.                                                                                                               |
| radius _Integer_        | No       | The radius around the location that is still considered as part of the location (in meters).                                                                                                                                  |

## Delete a reminder

> Example delete reminder request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "reminder_delete",
        "uuid": "0896d03b-eb90-49f7-9020-5ed3fd09df2d",
        "args": {"id": "6X7VrXrqjX6642cv"}
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"0896d03b-eb90-49f7-9020-5ed3fd09df2d": "ok"},
  ...
}
```

Delete a reminder from the current user account.

#### Command arguments

| Argument    | Required | Description           |
|-------------|----------|-----------------------|
| id _String_ | Yes      | The ID of the filter. |

## Locations

Locations are a top-level entity in the sync model. They contain a list of all
locations that are used within user's current location reminders.

> An example location object

```
["Shibuya-ku, Japan", "35.6623001098633", "139.706527709961"]
```

#### Properties

The location object is specific, as it's not an object, but an ordered array.

| Array index | Description           |
|-------------|-----------------------|
| 0 _String_  | Name of the location. |
| 1 _String_  | Location latitude.    |
| 2 _String_  | Location longitude.   |

### Clear locations

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[{"type": "clear_locations", "uuid": "d285ae02-80c6-477c-bfa9-45272d7bddfb", "args": {}}]'

{
  ...
  "sync_status": {"d285ae02-80c6-477c-bfa9-45272d7bddfb": "ok"},
  ...
}
```

Clears the locations list, which is used for location reminders.