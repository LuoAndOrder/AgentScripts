# User

> An example user:

```
{
    "activated_user": false,
    "auto_reminder": 0,
    "avatar_big": "https://*.cloudfront.net/*_big.jpg",
    "avatar_medium": "https://*.cloudfront.net/*_medium.jpg",
    "avatar_s640": "https://*.cloudfront.net/*_s640.jpg",
    "avatar_small": "https://*.cloudfront.net/*_small.jpg",
    "business_account_id": "1",
    "daily_goal": 15,
    "date_format": 0,
    "days_off": [6, 7],
    "email": "me@example.com",
    "feature_identifier": "2671355_0123456789abcdef70123456789abcdefe0123456789abcdefd0123456789abc",
    "features": {
        "beta": 1,
        "dateist_inline_disabled": false,
        "dateist_lang": null,
        "global.teams": true,
        "has_push_reminders": true,
        "karma_disabled": false,
        "karma_vacation": false,
        "kisa_consent_timestamp": null,
        "restriction": 3
    },
    "full_name": "Example User",
    "has_password": true,
    "id": "2671355",
    "image_id": "d160009dfd52b991030d55227003450f",
    "inbox_project_id": "6X7fqH39MwjmwV4q",
    "is_celebrations_enabled": true,
    "is_premium": true,
    "joinable_workspace": null,
    "joined_at": "2015-07-31T18:32:06.000000Z",
    "karma": 37504,
    "karma_trend": "up",
    "lang": "en",
    "mfa_enabled": false,
    "next_week": 1,
    "premium_status": "current_personal_plan",
    "premium_until": null,
    "share_limit": 51,
    "sort_order": 0,
    "start_day": 1,
    "start_page": "project?id=2203306141",
    "theme_id": "11",
    "time_format": 0,
    "token": "0123456789abcdef0123456789abcdef01234567",
    "tz_info": {
        "gmt_string": "-03:00",
        "hours": -3,
        "is_dst": 0,
        "minutes": 0,
        "timezone": "America/Sao_Paulo"
    },
    "verification_status": "legacy",
    "weekend_start_day": 6,
    "weekly_goal": 30
}
```

A Todoist user is represented by a JSON object. The dates will be in the UTC
timezone. Typically, a user object will have the following properties:

#### Properties

| Property                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| auto_reminder _Integer_      | The default time in minutes for the automatic reminders set, whenever a due date has been specified for a task.                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| avatar_big _String_          | The link to a 195x195 pixels image of the user's avatar.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| avatar_medium _String_       | The link to a 60x60 pixels image of the user's avatar.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| avatar_s640 _String_         | The link to a 640x640 pixels image of the user's avatar.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| avatar_small _String_        | The link to a 35x35 pixels image of the user's avatar.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| business_account_id _String_ | The ID of the user's business account.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| daily_goal _Integer_         | The daily goal number of completed tasks for karma.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| date_format _Integer_        | Whether to use the `DD-MM-YYYY` date format (if set to `0`), or the `MM-DD-YYYY` format (if set to `1`).                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| dateist_lang _String_        | The language expected for date recognition instead of the user's `lang` (`null` if the user's `lang` determines this), one of the following values: `da`, `de`, `en`, `es`, `fi`, `fr`, `it`, `ja`, `ko`, `nl`, `pl`, `pt_BR`, `ru`, `sv`, `tr`, `zh_CN`, `zh_TW`.                                                                                                                                                                                                                                                                                                 |
| days_off _Array_             | Array of integers representing user's days off (between `1` and `7`, where `1` is `Monday` and `7` is `Sunday`).                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| email _String_               | The user's email.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| feature_identifier _String_  | An opaque id used internally to handle features for the user.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| features _Object_            | Used internally for any special features that apply to the user. Current special features include whether the user has enabled `beta`, whether `dateist_inline_disabled` that is inline date parsing support is disabled, whether the `dateist_lang` is set which overrides the date parsing language, whether the `gold_theme` has been awarded to the user, whether the user `has_push_reminders` enabled, whether the user has `karma_disabled`, whether the user has `karma_vacation` mode enabled, and whether any special `restriction` applies to the user. |
| full_name _String_           | The user's real name formatted as `Firstname Lastname`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| has_password _Boolean_       | Whether the user has a password set on the account. It will be `false` if they have only authenticated without a password (e.g. using Google, Facebook, etc.)                                                                                                                                                                                                                                                                                                                                                                                                      |
| id _String_                  | The user's ID.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| image_id _String_            | The ID of the user's avatar.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| inbox_project_id _String_    | The ID of the user's `Inbox` project.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| is_premium _Boolean_         | Whether the user has a Todoist Pro subscription (a `true` or `false` value).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| joined_at _String_           | The date when the user joined Todoist.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| karma _Integer_              | The user's karma score.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| karma_trend _String_         | The user's karma trend (for example `up`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| lang _String_                | The user's language, which can take one of the following values: `da`, `de`, `en`, `es`, `fi`, `fr`, `it`, `ja`, `ko`, `nl`, `pl`, `pt_BR`, `ru`, `sv`, `tr`, `zh_CN`, `zh_TW`.                                                                                                                                                                                                                                                                                                                                                                                    |
| next_week _Integer_          | The day of the next week, that tasks will be postponed to (between `1` and `7`, where `1` is `Monday` and `7` is `Sunday`).                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| premium_status _String_      | Outlines why a user is premium, possible values are: `not_premium`, `current_personal_plan`, `legacy_personal_plan` or `teams_business_member`.                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| premium_until _String_       | The date when the user's Todoist Pro subscription ends (`null` if not a Todoist Pro user). This should be used for informational purposes only as this does not include the grace period upon expiration. As a result, avoid using this to determine whether someone has a Todoist Pro subscription and use `is_premium` instead.                                                                                                                                                                                                                                  |
| sort_order _Integer_         | Whether to show projects in an `oldest dates first` order (if set to `0`, or a `oldest dates last` order (if set to `1`).                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| start_day _Integer_          | The first day of the week (between `1` and `7`, where `1` is `Monday` and `7` is `Sunday`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| start_page _String_          | The user's default view on Todoist. The start page can be one of the following: `inbox`, `teaminbox`, `today`, `next7days`, `project?id=1234` to open a project, `label?name=abc` to open a label, `filter?id=1234` to open a personal filter or `workspace_filter?id=1234` to open a workspace filter.                                                                                                                                                                                                                                                            |
| theme_id _String_            | The currently selected Todoist theme (a number between `0` and `10`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| time_format _Integer_        | Whether to use a `24h` format such as `13:00` (if set to `0`) when displaying time, or a `12h` format such as `1:00pm` (if set to `1`).                                                                                                                                                                                                                                                                                                                                                                                                                            |
| token _String_               | The user's token that should be used to call the other API methods.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| tz_info _Object_             | The user's timezone (a dictionary structure), which includes the following elements: the `timezone` as a string value, the `hours` and `minutes` difference from GMT, whether daylight saving time applies denoted by `is_dst`, and a string value of the time difference from GMT that is `gmt_string`.                                                                                                                                                                                                                                                           |
| weekend_start_day _Integer_  | The day used when a user chooses to schedule a task for the 'Weekend' (between 1 and 7, where 1 is Monday and 7 is Sunday).                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| verification_status _String_ | Describes if the user has verified their e-mail address or not. Possible values are:                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

- `unverified`, for users that have just signed up. Those users cannot use any of Todoist's social features like sharing projects or accepting project invitations.
- `verified`, for users that have verified themselves somehow. Clicking on the verification link inside the account confirmation e-mail is one such way alongside signing up through a social account.
- `blocked`, for users that have failed to verify themselves in 7 days. Those users will have restricted usage of Todoist.
- `legacy`, for users that have signed up before August, 2022 weekly_goal _Integer_ | The target number of tasks to complete per week.

## Update user's properties

> Example update user request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "user_update",
        "uuid": "52f83009-7e27-4b9f-9943-1c5e3d1e6889",
        "args": {
            "current_password": "fke4iorij",
            "email": "mynewemail@example.com"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"52f83009-7e27-4b9f-9943-1c5e3d1e6889": "ok"},
  ...
}
```

#### Command arguments

| Argument                       | Required                                 | Description                                                                                                                                                                                                                                                                         |
|--------------------------------|------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| current_password _String_      | Yes (if modifying `email` or `password`) | The user's current password. This must be provided if the request is modifying the user's password or email address and the user already has a password set (indicated by `has_password` in the [user](#tag/Sync/User) object). For amending other properties this is not required. |
| email _String_                 | No                                       | The user's email.                                                                                                                                                                                                                                                                   |
| full_name _String_             | No                                       | The user's name.                                                                                                                                                                                                                                                                    |
| password _String_              | No                                       | The user's updated password. Must contain at least 8 characters and not be a common or easily guessed password.                                                                                                                                                                     |
| timezone _String_              | No                                       | The user's timezone (a string value such as `UTC`, `Europe/Lisbon`, `US/Eastern`, `Asia/Taipei`).                                                                                                                                                                                   |
| start_page _String_            | No                                       | The user's default view on Todoist. The start page can be one of the following: `inbox`, `teaminbox`, `today`, `next7days`, `project?id=1234` to open a project, `label?name=abc` to open a label, `filter?id=1234` to open a personal filter or `workspace_filter?id=1234` to open a workspace filter.                                                     |
| start_day _Integer_            | No                                       | The first day of the week (between `1` and `7`, where `1` is `Monday` and `7` is `Sunday`).                                                                                                                                                                                         |
| next_week _Integer_            | No                                       | The day of the next week, that tasks will be postponed to (between `1` and `7`, where `1` is `Monday` and `7` is `Sunday`).                                                                                                                                                         |
| time_format _Integer_          | No                                       | Whether to use a `24h` format such as `13:00` (if set to `0`) when displaying time, or a `12h` format such as `1:00pm` (if set to `1`).                                                                                                                                             |
| date_format _Integer_          | No                                       | Whether to use the `DD-MM-YYYY` date format (if set to `0`), or the `MM-DD-YYYY` format (if set to `1`).                                                                                                                                                                            |
| sort_order _Integer_           | No                                       | Whether to show projects in an `oldest dates first` order (if set to `0`, or a `oldest dates last` order (if set to `1`).                                                                                                                                                           |
| auto_reminder _Integer_        | No                                       | The default time in minutes for the automatic reminders set, whenever a due date has been specified for a task.                                                                                                                                                                     |
| theme _Integer_                | No                                       | The currently selected Todoist theme (between `0` and `10`).                                                                                                                                                                                                                        |
| weekend_start_day _Integer_    | No                                       | The day used when a user chooses to schedule a task for the 'Weekend' (between 1 and 7, where 1 is Monday and 7 is Sunday).                                                                                                                                                         |
| beta _Boolean_                 | No                                       | Whether the user is included in the beta testing group.                                                                                                                                                                                                                             |
| onboarding_completed _Boolean_ | No                                       | For first-party clients usage only. This attribute may be removed or changed without notice, so we strongly advise not to rely on it.                                                                                                                                               |
| onboarding_initiated _Boolean_ | No                                       | For first-party clients usage only. This attribute may be removed or changed without notice, so we strongly advise not to rely on it.                                                                                                                                               |
| onboarding_level _String_      | No                                       | For first-party clients usage only. The onboarding level (`pro`, `intermediate`, `beginner`). This attribute may be removed or changed without notice, so we strongly advise not to rely on it.                                                                                     |
| onboarding_persona _String_    | No                                       | For first-party clients usage only. The onboarding persona (`analog`, `tasks`, `calendar`, `organic`). This attribute may be removed or changed without notice, so we strongly advise not to rely on it.                                                                            |
| onboarding_role _String_       | No                                       | For first-party clients usage only. The onboarding role (`leader`, `founder`, `ic`). This attribute may be removed or changed without notice, so we strongly advise not to rely on it.                                                                                              |
| onboarding_skipped _Boolean_   | No                                       | For first-party clients usage only. This attribute may be removed or changed without notice, so we strongly advise not to rely on it.                                                                                                                                               |
| onboarding_started _Boolean_   | No                                       | For first-party clients usage only. This attribute may be removed or changed without notice, so we strongly advise not to rely on it.                                                                                                                                               |
| onboarding_team_mode _Boolean_ | No                                       | For first-party clients usage only. This attribute may be removed or changed without notice, so we strongly advise not to rely on it.                                                                                                                                               |
| onboarding_use_cases _Array_   | No                                       | For first-party clients usage only. JSON array of onboarding use cases (`personal`, `work`, `education`, `teamwork`, `solo`, `teamcreator`, `simple`, `teamjoiner`). This attribute may be removed or changed without notice, so we strongly advise not to rely on it.              |
| completed_guide_project_id _String_ | No                                   | For first-party clients usage only. Mark a Getting Started Guide project as completed by providing its project ID. This attribute may be removed or changed without notice, so we strongly advise not to rely on it.                                                                   |
| closed_guide_project_id _String_   | No                                   | For first-party clients usage only. Mark a Getting Started Guide project as closed (dismissed) by providing its project ID. This attribute may be removed or changed without notice, so we strongly advise not to rely on it.                                                        |
| getting_started_guide_projects _String_ | No                                       | For first-party clients usage only. JSON array of Getting Started guide projects with completion tracking. Each project contains `project_id`, `onboarding_use_case`, `completed`, and `closed` status. This attribute may be removed or changed without notice, so we strongly advise not to rely on it. |

#### Error codes

| Error Tag                 | Description                                                                                              |
|---------------------------|----------------------------------------------------------------------------------------------------------|
| `PASSWORD_REQUIRED`       | The command attempted to modify `password` or `email`, but no value was provided for `current_password`. |
| `AUTHENTICATION_ERROR`    | The value for `current_password` was incorrect.                                                          |
| `PASSWORD_TOO_SHORT`      | The value for `password` was shorter than the minimum 8 characters.                                      |
| `COMMON_PASSWORD`         | The value for `password` was matched against a common password list and rejected.                        |
| `PASSWORD_CONTAINS_EMAIL` | The value for password was matched against the user's email address or a part of the address.            |
| `INVALID_EMAIL`           | The value for `email` was not a valid email address.                                                     |

## Update karma goals

> Example update karma goals request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "update_goals",
        "uuid": "b9bbeaf8-9db6-452a-a843-a192f1542892",
        "args": {"vacation_mode": 1}
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"b9bbeaf8-9db6-452a-a843-a192f1542892": "ok"},
  ...
}
```

Update the karma goals of the user.

#### Command arguments

| Argument                 | Required | Description                                                                                       |
|--------------------------|----------|---------------------------------------------------------------------------------------------------|
| daily_goal _Integer_     | No       | The target number of tasks to complete per day.                                                   |
| weekly_goal _Integer_    | No       | The target number of tasks to complete per week.                                                  |
| ignore_days _Integer_    | No       | A list with the days of the week to ignore (`1` for `Monday` and `7` for `Sunday`).               |
| vacation_mode _Integer_  | No       | Marks the user as being on vacation (where `1` is true and `0` is false).                         |
| karma_disabled _Integer_ | No       | Whether to disable the karma and goals measuring altogether (where `1` is true and `0` is false). |

## User plan limits

> An example user plan limits sync response

```
{
    "user_plan_limits": {
        "current": {
            "plan_name": "free",
            ...details of the current user plan
        },
        "next": {
            "plan_name": "pro",
            ...details of a potential upgrade
        }
    }
}
```

The `user_plan_limits` sync resource type describes the available features and
limits applicable to the current user plan. The user plan info object (detailed
in the next section) returned within the `current` property shows the values
that are currently applied to the user.

If there is an upgrade available, the `next` property will show the values that will apply if the user chooses
to upgrade. If there is no available upgrade, the `next` value will be null.

#### Properties

| Property         | Description                                                                                                                     |
|------------------|---------------------------------------------------------------------------------------------------------------------------------|
| current _Object_ | A user plan info object representing the available functionality and limits for the user's current plan.                        |
| next _Object_    | A user plan info object representing the plan available for upgrade. If there is no available upgrade, this value will be null. |

### User plan info

> An example user plan info object

```
{
    "activity_log": true,
    "activity_log_limit": 7,
    "advanced_permissions": true,
    "automatic_backups": false,
    "calendar_feeds": true,
    "calendar_layout": true,
    "comments": true,
    "completed_tasks": true,
    "custom_app_icon": false,
    "customization_color": false,
    "deadlines": true,
    "durations": true,
    "email_forwarding": true,
    "filters": true,
    "labels": true,
    "max_calendar_accounts": 1,
    "max_collaborators": 5,
    "max_filters": 3,
    "max_folders_per_workspace": 25,
    "max_workspace_filters": 3,
    "workspace_filters": true,
    "max_free_workspaces_created": 1,
    "max_guests_per_workspace": 25,
    "max_labels": 500,
    "max_projects": 5,
    "max_projects_joined": 500,
    "max_reminders_location": 300,
    "max_reminders_time": 700,
    "max_sections": 20,
    "max_tasks": 300,
    "max_user_templates": 100,
    "plan_name": "free",
    "reminders": false,
    "reminders_at_due": true,
    "templates": true,
    "upload_limit_mb": 5,
    "uploads": true,
    "weekly_trends": true
}
```

The user plan info object describes the availability of features and any limitations applied for a given user plan.

#### Properties

| Property                         | Description                                                                                                                 |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| plan_name _String_               | The name of the plan.                                                                                                       |
| activity_log _Boolean_           | Whether the user can view the [activity log](#tag/Activity).                                                                |
| activity_log_limit _Integer_     | The number of days of history that will be displayed within the activity log. If there is no limit, the value will be `-1`. |
| automatic_backups _Boolean_      | Whether [backups](#tag/Backups) will be automatically created for the user's account and available for download.            |
| calendar_feeds _Boolean_         | Whether calendar feeds can be enabled for the user's projects.                                                              |
| comments _Boolean_               | Whether the user can add [comments](#tag/Sync/Comments).                                                                    |
| completed_tasks _Boolean_        | Whether the user can search in the completed tasks archive or access the completed tasks overview.                          |
| custom_app_icon _Boolean_        | Whether the user can set a custom app icon on the iOS app.                                                                  |
| customization_color _Boolean_    | Whether the user can use special themes or other visual customization.                                                      |
| email_forwarding _Boolean_       | Whether the user can add tasks or comments via [email](#tag/Emails).                                                        |
| filters _Boolean_                | Whether the user can add and update [filters](#tag/Sync/Filters).                                                           |
| max_filters _Integer_            | The maximum number of filters a user can have.                                                                              |
| workspace_filters _Boolean_      | Whether the user can add and update [workspace filters](#tag/Sync/Workspace-Filters) (Business/Enterprise plans only).      |
| max_workspace_filters _Integer_  | The maximum number of workspace filters a user can have per workspace.                                                      |
| labels _Boolean_                 | Whether the user can add [labels](#tag/Sync/Labels).                                                                        |
| max_labels _Integer_             | The maximum number of labels a user can have.                                                                               |
| reminders _Boolean_              | Whether the user can add [reminders](#tag/Sync/Reminders).                                                                  |
| max_reminders_location _Integer_ | The maximum number of location reminders a user can have.                                                                   |
| max_reminders_time _Integer_     | The maximum number of time-based reminders a user can have.                                                                 |
| templates _Boolean_              | Whether the user can import and export [project templates](#tag/Templates).                                                 |
| uploads _Boolean_                | Whether the user can [upload attachments](#tag/Uploads).                                                                    |
| upload_limit_mb _Integer_        | The maximum size of an individual file the user can upload.                                                                 |
| weekly_trends _Boolean_          | Whether the user can view [productivity stats](#tag/Sync/User).                                                             |
| max_projects _Integer_           | The maximum number of active [projects](#tag/Sync/Projects) a user can have.                                                |
| max_sections _Integer_           | The maximum number of active [sections](#tag/Sync/Sections) a user can have.                                                |
| max_tasks _Integer_              | The maximum number of active [tasks](#tag/Sync/Tasks) a user can have.                                                      |
| max_collaborators _Integer_      | The maximum number of [collaborators](#tag/Sync/Sharing/Collaborators) a user can add to a project.                         |

## User settings

> Example user settings object:

```
{
    "reminder_push": true,
    "reminder_desktop": true,
    "reminder_email": true,
    "completed_sound_desktop": true,
    "completed_sound_mobile": true
}
```

_Availability of reminders functionality is dependent on the current user plan.
This value is indicated by the `reminders` property of the [user plan limits](#tag/Sync/User/User-plan-limits) object.
These settings will have no effect if the user is not eligible for reminders._

#### Properties

| Property                          | Description                                                                      |
|-----------------------------------|----------------------------------------------------------------------------------|
| reminder_push _Boolean_           | Set to true to send reminders as push notifications.                             |
| reminder_desktop _Boolean_        | Set to true to show reminders in desktop applications.                           |
| reminder_email _Boolean_          | Set to true to send reminders by email.                                          |
| completed_sound_desktop _Boolean_ | Set to true to enable sound when a task is completed in Todoist desktop clients. |
| completed_sound_mobile _Boolean_  | Set to true to enable sound when a task is completed in Todoist mobile clients.  |

## User productivity stats

> Example stats object:

```json
{
  "completed_count": 123,
  "days_items": [
    {
      "date": "2025-10-17",
      "total_completed": 5
    }
  ],
  "week_items": [
    {
      "from": "2025-10-13",
      "to": "2025-10-19",
      "total_completed": 12
    }
  ]
}
```

#### Properties

| Property                     | Description                                                                                                |
|------------------------------|------------------------------------------------------------------------------------------------------------|
| completed_count _Integer_    | The total number of tasks the user has completed across all time.                                          |
| days_items _Array_           | An array containing completion statistics for today. Each item contains `date` and `total_completed`.      |
| week_items _Array_           | An array containing completion statistics for the current week. Each item contains `from`, `to`, and `total_completed`. |

### Update user settings

> Example update user settings request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "user_settings_update",
        "temp_id": "e24ad822-a0df-4b7d-840f-83a5424a484a",
        "uuid": "41e59a76-3430-4e44-92b9-09d114be0d49",
        "args": {"reminder_desktop": false}
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"41e59a76-3430-4e44-92b9-09d114be0d49": "ok"},
  ...
}
```

Update one or more user settings.

#### Command arguments

| Argument                          | Required | Description                                                                      |
|-----------------------------------|----------|----------------------------------------------------------------------------------|
| reminder_push _Boolean_           | No       | Set to true to send reminders as push notifications.                             |
| reminder_desktop _Boolean_        | No       | Set to true to show reminders in desktop applications.                           |
| reminder_email _Boolean_          | No       | Set to true to send reminders by email.                                          |
| completed_sound_desktop _Boolean_ | No       | Set to true to enable sound when a task is completed in Todoist desktop clients. |
| completed_sound_mobile _Boolean_  | No       | Set to true to enable sound when a task is completed in Todoist mobile clients.  |