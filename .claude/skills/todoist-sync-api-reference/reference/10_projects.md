# Projects

> An example project object:

```
{
    "id": "6Jf8VQXxpwv56VQ7",
    "name": "Shopping List",
    "description": "Stuff to buy",
    "workspace_id": 12345,
    "is_invite_only": false,
    "status": "IN_PROGRESS",
    "is_link_sharing_enabled": true,
    "collaborator_role_default": "READ_WRITE",
    "color": "lime_green",
    "parent_id": null,
    "child_order": 1,
    "is_collapsed": false,
    "shared": false,
    "can_assign_tasks": false,
    "is_deleted": false,
    "is_archived": false,
    "is_favorite": false,
    "is_frozen": false,
    "view_style": "list",
    "role": "READ_WRITE"
    "inbox_project": true,
    "folder_id": null,
    "created_at": "2023-07-13T10:20:59Z",
    "updated_at": "2024-12-10T13:27:29Z",
    "is_pending_default_collaborator_invites: false,
}
```

#### Properties

| Property                                          | Description                                                                                                                                                                                                                                                                  |
|---------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id _String_                                       | The ID of the project.                                                                                                                                                                                                                                                       |
| name _String_                                     | The name of the project.                                                                                                                                                                                                                                                     |
| description _String_                              | Description for the project. _Only used for teams_                                                                                                                                                                                                                           |
| workspace_id _String_                             | Real or temp ID of the workspace the project. _Only used for teams_                                                                                                                                                                                                          |
| is_invite_only _Boolean_                          | Indicates if the project is invite-only or if it should be visible for everyone in the workspace. If missing or null, the default value from the workspace `is_invite_only_default` will be used. _Only used for teams_                                                      |
| status _String_                                   | The status of the project. Possible values: `PLANNED`, `IN_PROGRESS`, `PAUSED`, `COMPLETED`, `CANCELED`. _Only used for teams_                                                                                                                                               |
| is_link_sharing_enabled _Boolean_                 | If False, the project is invite-only and people can't join by link. If true, the project is visible to anyone with a link, and anyone can join it. _Only used for teams_                                                                                                     |
| collaborator_role_default _String_                | The role a user can have. Possible values: `CREATOR`, `ADMIN`, `READ_WRITE`, `EDIT_ONLY`, `COMPLETE_ONLY`. (`CREATOR` is equivalent to admin and is automatically set at project creation; it can't be set to anyone later). Defaults to `READ_WRITE`. _Only used for teams_ |
| color _String_                                    | The color of the project icon. Refer to the `name` column in the [Colors](#tag/Colors) guide for more info.                                                                                                                                                                  |
| parent_id _String_                                | The ID of the parent project. Set to `null` for root projects.                                                                                                                                                                                                               |
| child_order _Integer_                             | The order of the project. Defines the position of the project among all the projects with the same `parent_id`                                                                                                                                                               |
| is_collapsed _Boolean_                            | Whether the project's sub-projects are collapsed (a `true` or `false` value).                                                                                                                                                                                                |
| shared _Boolean_                                  | Whether the project is shared (a `true` or `false` value).                                                                                                                                                                                                                   |
| can_assign_tasks _Boolean_                        | Whether tasks in the project can be assigned to users (a `true` or `false` value).                                                                                                                                                                                           |
| is_deleted _Boolean_                              | Whether the project is marked as deleted (a `true` or `false` value).                                                                                                                                                                                                        |
| is_archived _Boolean_                             | Whether the project is marked as archived (a `true` or `false` value).                                                                                                                                                                                                       |
| is_favorite _Boolean_                             | Whether the project is a favorite (a `true` or `false` value).                                                                                                                                                                                                               |
| is_frozen _Boolean_                               | Workspace or personal projects from a cancelled subscription (a `true` or `false` value).                                                                                                                                                                                    |
| view_style _Enum_                                 | The mode in which to render tasks in this project. One of `list`, `board`, or `calendar`.                                                                                                                                                                                    |
| role _String_                                     | The role of the requesting user. Possible values: `CREATOR`, `ADMIN`, `READ_WRITE`, `EDIT_ONLY`, `COMPLETE_ONLY`. _Only used for teams_                                                                                                                                      |
| inbox_project _Boolean_                           | Whether the project is `Inbox` (`true` or otherwise this property is not sent).                                                                                                                                                                                              |
| folder_id _String_                                | The ID of the folder which this project is in.                                                                                                                                                                                                                               |
| created_at _String_                               | Project creation date in the format YYYY-MM-DDTHH:MM:SSZ date.                                                                                                                                                                                                               |
| updated_at _String_                               | Project update date in the format YYYY-MM-DDTHH:MM:SSZ date.                                                                                                                                                                                                                 |
| is_pending_default_collaborator_invites _Boolean_ | If true, we are still adding default collaborators to the project in background. _Only used for teams_                                                                                                                                                                       |
| access _Object_                                   | Project access configuration. Contains `visibility` (`"restricted"`, `"team"`, or `"public"`) and `configuration` object. For public projects, configuration includes `hide_collaborator_details` and `disable_duplication` booleans. _Only used for teams_                  |

**Note:** `project.view_style` takes precedence over
[`view_options.view_mode`](#tag/Sync/View-Options) for projects in Todoist
clients. The former is set per project, while the latter is set per user.

## Add a project

> Example add project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "project_add",
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",
        "args": {
            "name": "Shopping List"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  "temp_id_mapping": {"4ff1e388-5ca6-453a-b0e8-662ebf373b6b": "6Jf8VQXxpwv56VQ7"},
  ...
}
```

Add a new project.

#### Command arguments

| Argument                           | Required | Description                                                                                                                                                                                                                                            |
|------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name _String_                      | Yes      | The name of the project (a string value).                                                                                                                                                                                                              |
| color _String_                     | No       | The color of the project icon. Refer to the `name` column in the [Colors](#tag/Colors) guide for more info.                                                                                                                                            |
| parent_id _String_                 | No       | The ID of the parent project. Set to `null` for root projects                                                                                                                                                                                          |
| folder_id _String_                 | No       | The ID of the folder, when creating projects in workspaces. Set to `null` for root projects                                                                                                                                                            |
| child_order _Integer_              | No       | The order of the project. Defines the position of the project among all the projects with the same `parent_id`                                                                                                                                         |
| is_favorite _Boolean_              | No       | Whether the project is a favorite (a `true` or `false` value).                                                                                                                                                                                         |
| view_style _String_                | No       | A string value (either `list` or `board`, default is `list`). This determines the way the project is displayed within the Todoist clients.                                                                                                             |
| description _String_               | No       | Description for the project (up to 1024 characters). _Only used for teams_                                                                                                                                                                             |
| workspace_id _String_              | No       | Real or temp ID of the workspace the project should belong to                                                                                                                                                                                          |
| is_invite_only _Boolean_           | No       | Indicates if the project is invite-only or if it should be visible for everyone in the workspace. If missing or null, the default value from the workspace `is_invite_only_default` will be used. _Only used for teams_                                |
| status _String_                    | No       | The status of the project. Possible values: `PLANNED`, `IN_PROGRESS`, `PAUSED`, `COMPLETED`, `CANCELED`. _Only used for teams_                                                                                                                         |
| is_link_sharing_enabled _Boolean_  | No       | If False, the project is invite-only and people can't join by link. If true, the project is visible to anyone with a link, and anyone can join it. _Only used for teams_                                                                               |
| collaborator_role_default _String_ | No       | The role a user can have. Possible values: `CREATOR`, `ADMIN`, `READ_WRITE`, `EDIT_ONLY`, `COMPLETE_ONLY`. (`CREATOR` is equivalent to admin and is automatically set at project creation; it can't be set to anyone later). _Only used for teams_     |
| access _Object_                    | No       | Project access configuration with `visibility` (`"restricted"`, `"team"`, or `"public"`) and `configuration` object. For public projects, configuration includes `hide_collaborator_details` and `disable_duplication` booleans. _Only used for teams_ |

## Update a project

> Example update project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[
    {
        "type": "project_update",
        "uuid": "1ca42128-d12f-4a66-8413-4d6ff2838fde",
        "args": {
            "id": "6Jf8VQXxpwv56VQ7",
            "name": "Shopping"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"1ca42128-d12f-4a66-8413-4d6ff2838fde": "ok"},
  ...
}
```

Update an existing project.

#### Command arguments

| Argument                           | Required | Description                                                                                                                                                                                                                                                                  |
|------------------------------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id _String_                        | Yes      | The ID of the project (could be temp id).                                                                                                                                                                                                                                    |
| name _String_                      | No       | The name of the project (a string value).                                                                                                                                                                                                                                    |
| color _String_                     | No       | The color of the project icon. Refer to the `name` column in the [Colors](#tag/Colors) guide for more info.                                                                                                                                                                  |
| is_collapsed _Boolean_             | No       | Whether the project's sub-projects are collapsed (a `true` or `false` value).                                                                                                                                                                                                |
| is_favorite _Boolean_              | No       | Whether the project is a favorite (a `true` or `false` value).                                                                                                                                                                                                               |
| view_style _String_                | No       | A string value (either `list` or `board`). This determines the way the project is displayed within the Todoist clients.                                                                                                                                                      |
| description _String_               | No       | Description for the project (up to 1024 characters). _Only used for teams_                                                                                                                                                                                                   |
| status _String_                    | No       | The status of the project. Possible values: `PLANNED`, `IN_PROGRESS`, `PAUSED`, `COMPLETED`, `CANCELED`. _Only used for teams_                                                                                                                                               |
| is_link_sharing_enabled _Boolean_  | No       | If False, the project is invite-only and people can't join by link. If true, the project is visible to anyone with a link, and anyone can join it. _Only used for teams_                                                                                                     |
| collaborator_role_default _String_ | No       | The role a user can have. Possible values: `CREATOR`, `ADMIN`, `READ_WRITE`, `EDIT_ONLY`, `COMPLETE_ONLY`. (`CREATOR` is equivalent to admin and is automatically set at project creation; it can't be set to anyone later). Defaults to `READ_WRITE`. _Only used for teams_ |
| access _Object_                    | No       | Project access configuration with `visibility` (`"restricted"`, `"team"`, or `"public"`) and `configuration` object. For public projects, configuration includes `hide_collaborator_details` and `disable_duplication` booleans. _Only used for teams_                       |

## Move a project

> Example move project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[
    {
        "type": "project_move",
        "uuid": "1ca42128-d12f-4a66-8413-4d6ff2838fde",
        "args": {
            "id": "6Jf8VQXxpwv56VQ7",
            "parent_id": "6X7fphhgwcXVGccJ"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"1ca42128-d12f-4a66-8413-4d6ff2838fde": "ok"},
  ...
}
```

Update parent project relationships of the project.

#### Command arguments

| Argument           | Required | Description                                                                                               |
|--------------------|----------|-----------------------------------------------------------------------------------------------------------|
| id _String_        | Yes      | The ID of the project (could be a temp id).                                                               |
| parent_id _String_ | No       | The ID of the parent project (could be a temp id). If set to null, the project will be moved to the root. |

## Move a Project to a Workspace

> Example move project to workspace request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[
    {
        "type": "project_move_to_workspace",
        "uuid": "1ca42128-d12f-4a66-8413-4d6ff2838fde",
        "args": {
            "project_id": "6Jf8VQXxpwv56VQ7",
            "workspace_id": "220325187",
            "is_invite_only": false,
            "folder_id": null
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"1ca42128-d12f-4a66-8413-4d6ff2838fde": "ok"},
  ...
}
```

Moves a personal project into the target workspace.

A few notes about moving projects to a workspace:

- Moving a parent project to a workspace will also move all its child projects to that workspace.
- If no folder_id is supplied, child projects will be moved into a folder with the same name as the parent project being moved
- If a folder_id is supplied, the parent and child projects will be moved into that folder.
- At the moment, it is not possible to move a project to another workspace (changing its `workspace_id`), or to the user's personal workspace.
- Moving a project to a workspace affects all its collaborators. Collaborators who are not members of the target workspace will be added as guests, if guest members are allowed in the target workspace

#### Command arguments

| Argument                 | Required | Description                                                                                 |
|--------------------------|----------|---------------------------------------------------------------------------------------------|
| project_id _String_      | Yes      | The ID of the project (can be a temp id).                                                   |
| workspace_id _String_    | Yes      | The ID of the workspace the project will be moved into                                      |
| is_invite_only _Boolean_ | No       | If true the project will be restricted access, otherwise any workspace member could join it |
| folder_id _String_       | No       | If supplied, the project and any child projects will be moved into this workspace folder    |

## Move a Project out of a Workspace

> Example move project out of a workspace request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[
    {
        "type": "project_move_to_personal",
        "uuid": "1ca42128-d12f-4a66-8413-4d6ff2838fde",
        "args": {
            "project_id": "6Jf8VQXxpwv56VQ7",
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"1ca42128-d12f-4a66-8413-4d6ff2838fde": "ok"},
  ...
}
```

Moves a project inside a workspace out back into a users personal space.

Only the original creator of the workspace have permissions to do this, and only if they
are still currently an admin of said workspace.

#### Command arguments

| Argument            | Required | Description                                                |
|---------------------|----------|------------------------------------------------------------|
| project_id _String_ | Yes      | The ID of the project being moved back (can be a temp id). |

## Leave a project

> Example leave project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[
    {
        "type": "project_leave",
        "uuid": "1ca42128-d12f-4a66-8413-4d6ff2838fde",
        "args": {
            "project_id": "6Jf8VQXxpwv56VQ7",
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"1ca42128-d12f-4a66-8413-4d6ff2838fde": "ok"},
  ...
}
```

_Only used for teams_

This command is used to remove self from a workspace project. As this is a
v2-only command, it will only accept v2 project id.

#### Command arguments

| Argument            | Required | Description                                                                  |
|---------------------|----------|------------------------------------------------------------------------------|
| project_id _String_ | Yes      | The ID (`v2_id`) of the project to leave. It only accepts `v2_id` as the id. |

## Delete a project

> Example delete project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[
    {
        "type": "project_delete",
        "uuid": "367182ba-125f-4dbb-bff6-c1343fd751e4",
        "args": {
            "id": "6X7fphhgwcXVGccJ"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"367182ba-125f-4dbb-bff6-c1343fd751e4": "ok"},
  ...
}
```

Delete an existing project and all its descendants.
Workspace projects can only be deleted by `ADMIN`s and it must be archived first.

#### Command arguments

| Argument    | Required | Description                                       |
|-------------|----------|---------------------------------------------------|
| id _String_ | Yes      | ID of the project to delete (could be a temp id). |

## Archive a project

> Example archive project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[
    {
        "type": "project_archive",
        "uuid": "bbec1a60-2bdd-48ac-a623-c8eb968e1697",
        "args": {
            "id": "6X7fphhgwcXVGccJ"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"bbec1a60-2bdd-48ac-a623-c8eb968e1697": "ok"},
  ...
}
```

Archive a project and its descendants.

#### Command arguments

| Argument    | Required | Description                                        |
|-------------|----------|----------------------------------------------------|
| id _String_ | Yes      | ID of the project to archive (could be a temp id). |

## Unarchive a project

> Example unarchive project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[
    {
        "type": "project_unarchive",
        "uuid": "7d86f042-e098-4fa6-9c1f-a61fe8c39d74",
        "args": {
            "id": "6X7fphhgwcXVGccJ"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"7d86f042-e098-4fa6-9c1f-a61fe8c39d74": "ok"},
  ...
}
```

Unarchive a project. No ancestors will be unarchived along with the unarchived
project. Instead, the project is unarchived alone, loses any parent relationship
(becomes a root project), and is placed at the end of the list of other root
projects.

#### Command arguments

| Argument    | Required | Description                                          |
|-------------|----------|------------------------------------------------------|
| id _String_ | Yes      | ID of the project to unarchive (could be a temp id). |

## Reorder projects

> Example reorder projects request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[
    {
        "type": "project_reorder",
        "uuid": "bf0855a3-0138-4b76-b895-88cad8db9edc",
        "args": {
            "projects": [
                {
                    "id": "6Jf8VQXxpwv56VQ7",
                    "child_order": 1
                },
                {
                    "id": "6X7fphhgwcXVGccJ",
                    "child_order": 2
                }
            ]
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"bf0855a3-0138-4b76-b895-88cad8db9edc": "ok"},
  ...
}
```

The command updates `child_order` properties of projects in bulk.

#### Command arguments

| Argument                    | Required | Description                                                                                                                         |
|-----------------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------|
| projects _Array of Objects_ | Yes      | An array of objects to update. Each object contains two attributes: `id` of the project to update and `child_order`, the new order. |

## Change project role

> Example change project role request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[
    {
        "type": "project_change_role",
        "uuid": "bbec1a60-2bdd-48ac-a623-c8eb968e1697",
        "args": {
            "id": "6X7fphhgwcXVGccJ",
            "user_id": 12345678,
            "role": "EDIT_ONLY"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"bbec1a60-2bdd-48ac-a623-c8eb968e1697": "ok"},
  ...
}
```

Change the role a project member has within the project.

#### Command arguments

| Argument      | Required | Description                                                                                                                                                             |
|---------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id _String_   | Yes      | ID of the project to change the role for (could be a temp id).                                                                                                          |
| user_id _Int_ | Yes      | ID of the user whose role to change.                                                                                                                                    |
| role _String_ | Yes      | New role for the user. Valid values: `CREATOR`, `ADMIN`, `READ_WRITE`, `EDIT_ONLY`, `COMPLETE_ONLY`. Note: Only the project creator can be assigned the `CREATOR` role. |