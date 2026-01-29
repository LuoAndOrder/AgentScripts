# Project View Options Defaults

Project View Options Defaults (PVODs) define the default view preferences for all users of a project. These settings serve as the baseline view configuration that applies to all project members unless they have their own personal view options set.

> An example Project View Options Default object:

```json
{
    "project_id": "2203306141",
    "view_mode": "list",
    "grouped_by": null,
    "sorted_by": "due_date",
    "sort_order": "asc",
    "show_completed_tasks": false,
    "filtered_by": null,
    "calendar_settings": null,
    "creator_uid": 1855589,
    "updater_uid": 1855589
}
```

### Properties

 Property             | Description
----------------------|----------------------------------------------------------------------------------------------------------------------------
 project_id           | The project ID these defaults apply to (string, required)
 view_mode            | The default view mode: `list`, `board`, or `calendar` (string, required)
 grouped_by           | How tasks are grouped: `due_date`, `created_at`, `label`, `assignee`, `priority`, or `project` (string or null)
 sorted_by            | How tasks are sorted: `due_date`, `created_at`, `task_order`, `assignee`, `alphabetically`, or `priority` (string or null)
 sort_order           | Sort direction: `asc` or `desc` (string, required)
 show_completed_tasks | Whether to show completed tasks by default (boolean, required)
 filtered_by          | JSON string with filter criteria (string or null)
 calendar_settings    | Calendar-specific settings when `view_mode` is `calendar` (object or null)
 creator_uid          | User ID who created these defaults (integer, required)
 updater_uid          | User ID who last updated these defaults (integer, required)

### Sync behavior

- PVODs are returned during full sync if the user has access to the project
- When a project is created, its PVOD is automatically created and included in the same sync response
- Updates to PVODs trigger sync events for all project members
- When a PVOD is deleted, a tombstone is returned with `is_deleted: true` and includes: `project_id`, `is_deleted`, `creator_uid`, `updater_uid`, `show_completed_tasks`, and all view option fields (`view_mode`, `grouped_by`, `sorted_by`, `sort_order`, `filtered_by`) set to empty strings. `calendar_settings` is set to `null`
- PVODs take precedence over legacy `project.view_style` settings

### Commands

#### project_view_options_defaults_set

Updates the default view options for a project. Only users with admin permissions on the project can update PVODs.

> Command arguments:

 Name                 | Required | Description
----------------------|----------|----------------------------------------------------------------------
 project_id           | Yes      | The project ID to update defaults for
 view_mode            | No       | The default view mode: `list`, `board`, or `calendar`
 grouped_by           | No       | How to group tasks (see properties above)
 sorted_by            | No       | How to sort tasks (see properties above)
 sort_order           | No       | Sort direction: `asc` or `desc`
 show_completed_tasks | No       | Whether to show completed tasks
 filtered_by          | No       | JSON string with filter criteria
 calendar_settings    | No       | Calendar-specific settings (required when `view_mode` is `calendar`)

> Example command:

```shell
$ curl -X POST \
    https://api.todoist.com/sync/v9/sync \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $token" \
    -d '[{
        "type": "project_view_options_defaults_set",
        "uuid": "bf0855a3-0138-44-b618-1cb8d3d7a869",
        "args": {
            "project_id": "2203306141",
            "view_mode": "board",
            "grouped_by": "priority",
            "sorted_by": "due_date",
            "sort_order": "asc",
            "show_completed_tasks": false
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"bf0855a3-0138-44-b618-1cb8d3d7a869": "ok"},
  ...
}
```