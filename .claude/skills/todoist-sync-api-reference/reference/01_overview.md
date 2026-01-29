# Overview

## Read resources

> Example read resources request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d sync_token='*' \
    -d resource_types='["all"]'
```

> Example response:

```shell
{
  "completed_info": [ ... ],
  "collaborators": [ ... ],
  "collaborator_states": [ ... ],
  "day_orders": { ... },
  "filters": [ ... ],
  "full_sync": true,
  "items": [ ... ],
  "labels": [ ... ],
  "live_notifications": [ ... ],
  "live_notifications_last_read_id": "0",
  "locations": [ ... ],
  "notes": [ ... ],
  "project_notes": [ ... ],
  "projects": [ ... ],
  "project_view_options_defaults": [ ... ],
  "reminders": [ ... ],
  "role_actions": { ... },
  "sections": [ ... ],
  "stats": { ... },
  "settings_notifications": { ... },
  "sync_token": "TnYUZEpuzf2FMA9qzyY3j4xky6dXiYejmSO85S5paZ_a9y1FI85mBbIWZGpW",
  "temp_id_mapping": { ... },
  "user": { ... },
  "user_plan_limits": { ... },
  "user_settings": { ... },
  "view_options": [ ... ],
  "workspace_users": { ... }
}
```

To retrieve your user resources, make a Sync API request with the following
parameters:

#### Parameters

| Parameter                              | Required | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|----------------------------------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| sync_token _String_                    | Yes      | A special string, used to allow the client to perform incremental sync. Pass `*` to retrieve all active resource data. More details about this below.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| resource_types _JSON array of strings_ | Yes      | Used to specify what resources to fetch from the server. It should be a JSON-encoded array of strings. Here is a list of available resource types: `labels`, `projects`, `items`, `notes`, `sections`, `filters`, `reminders`, `reminders_location`, `locations`, `user`, `live_notifications`, `collaborators`, `user_settings`, `notification_settings`, `user_plan_limits`, `completed_info`, `stats`, `workspaces`, `workspace_users`, `workspace_filters`, `view_options`, `project_view_options_defaults`, `role_actions`. You may use `all` to include all the resource types. Resources can also be excluded by prefixing a `-` prior to the name, for example, `-projects` |

In order to fetch both types of reminders you must include both resource types in your request, for example: `resource_types=["reminders", "reminders_location"]` .

The `workspace_users` resource type will not be returned in full sync, but should be requested in incremental sync to keep data up-to-date once it's loaded from the REST endpoint.


#### Response

When the request succeeds, an HTTP 200 response will be returned with a JSON
object containing the requested resources and a new `sync_token`.

| Field                         | Description                                                                                                                                                                                                        |
|-------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| sync_token                    | A new synchronization token. Used by the client in the next sync request to perform an incremental sync.                                                                                                           |
| full_sync                     | Whether the response contains all data (a full synchronization) or just the incremental updates since the last sync.                                                                                               |
| full_sync_date_utc            | For full syncs, the time when the data was generated. For big accounts, the data may be returned with some delay, requiring an [incremental sync](#tag/Sync/Overview/Incremental-sync) to get up-to-date data.     |
| user                          | A user object.                                                                                                                                                                                                     |
| projects                      | An array of [project](#tag/Sync/Projects) objects.                                                                                                                                                                 |
| items                         | An array of [item](#tag/Sync/Items) objects.                                                                                                                                                                       |
| notes                         | An array of [task comments](#tag/Sync/Comments/Task-Comments) objects.                                                                                                                                             |
| project_notes                 | An array of [project comments](#tag/Sync/Comments/Project-Comments) objects.                                                                                                                                       |
| sections                      | An array of [section](#tag/Sync/Sections) objects.                                                                                                                                                                 |
| labels                        | An array of [personal label](#tag/Sync/Labels) objects.                                                                                                                                                            |
| filters                       | An array of [filter](#tag/Sync/Filters) objects.                                                                                                                                                                   |
| workspace_filters             | An array of [workspace filter](#tag/Sync/Workspace-Filters) objects.                                                                                                                                               |
| day_orders                    | A JSON object specifying the order of items in daily agenda.                                                                                                                                                       |
| reminders                     | An array of [reminder](#tag/Sync/Reminders) objects.                                                                                                                                                               |
| collaborators                 | A JSON object containing all [collaborators](#tag/Sync/Sharing/Collaborators) for all shared projects. The `projects` field contains the list of all shared projects, where the user acts as one of collaborators. |
| collaborators_states          | An array specifying the state of each collaborator in each project. The state can be invited, active, inactive, deleted.                                                                                           |
| completed_info                | An array of `completed` info objects indicating the number of completed items within an active project, section, or parent item. Projects will also include the number of archived sections.                       |
| live_notifications            | An array of `live_notification` objects.                                                                                                                                                                           |
| live_notifications_last_read  | What is the last live notification the user has seen? This is used to implement unread notifications.                                                                                                              |
| user_settings                 | A JSON object containing [user settings](#tag/Sync/User/User-settings).                                                                                                                                            |
| user_plan_limits              | A JSON object containing [user plan limits](#tag/Sync/User/User-plan-limits).                                                                                                                                      |
| stats                         | A JSON object containing [user productivity stats](#tag/Sync/User/User-productivity-stats) with completion counts for today and this week.                                                                         |
| view_options                  | An array of [view options](#tag/Sync/View-options) objects.                                                                                                                                                        |
| project_view_options_defaults | An array of [project view options defaults](#tag/Sync/Project-View-Options-Defaults) objects.                                                                                                                      |
| role_actions                  | The actions each role in the system are allowed to perform on a project                                                                                                                                            |
| workspaces                    | A JSON object containing [workspace](#tag/Sync/Workspace) objects.                                                                                                                                                 |
| workspace_users               | A JSON object containing [workspace_user](#tag/Sync/Workspace-users) objects. Only in incremental sync.                                                                                                            |

## Write resources

> Example create project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "project_add",
        "temp_id": "381e601f-0ef3-4ed6-bf95-58f896d1a314",
        "uuid": "ed1ce597-e4c7-4a88-ba48-e048d827c067",
        "args": {
            "name": "Shopping List",
            "color": "berry_red"
        }
    }]'
```

> Example response:

```shell
{
  "sync_token": "cdTUEvJoChiaMysD7vJ14UnhN-FRdP-IS3aisOUpl3aGlIQA9qosBgvMmhbn",
  "sync_status": {"ed1ce597-e4c7-4a88-ba48-e048d827c067": "ok"},
  "temp_id_mapping": {"381e601f-0ef3-4ed6-bf95-58f896d1a314": "6HWcc9PJCvPjCxC9"}
}
```

To write to your user's Todoist resources, make a Sync API request with the
following parameters:

#### Parameters

| Parameter       | Required | Description                                                                             |
|-----------------|----------|-----------------------------------------------------------------------------------------|
| commands _JSON_ | Yes      | A JSON array of Command objects. Each command will be processed in the specified order. |

#### Command object

| Field            | Description                                                                                                                                       |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| type _String_    | The type of the command.                                                                                                                          |
| args _Object_    | The parameters of the command.                                                                                                                    |
| uuid _String_    | Command UUID. More details about this below.                                                                                                      |
| temp_id _String_ | Temporary resource ID, Optional. Only specified for commands that create a new resource (e.g. `item_add` command). More details about this below. |

## Command UUID

Clients should generate a unique string ID for each command and specify it
in the `uuid` field. The Command UUID will be used for two purposes:

1. Command result mapping: Each command's result will be stored in the
   `sync_status` field of the response JSON object. The `sync_status` object has
   its key mapped to a command's `uuid` and its value containing the result of a
   command.
2. Command idempotency: Todoist will not execute a command that has same UUID as
   a previously executed command. This will allow clients to safely retry
   each command without accidentally performing the action twice.

## Temporary resource ID

> An example that shows how temporary IDs can be used and referenced:

```
[
    {
        "type": "project_add",
        "temp_id": "c7beb07f-b226-4eb1-bf63-30d782b07b1a",
        "args": {
            "name": "Shopping List"
        },
        "uuid": "ac417051-1cdc-4dc3-b4f8-14526d5bfd16"
    },
    {
        "type": "item_add",
        "temp_id": "43f7ed23-a038-46b5-b2c9-4abda9097ffa",
        "args": {
            "content": "Buy Milk",
            "project_id": "c7beb07f-b226-4eb1-bf63-30d782b07b1a"
        },
        "uuid": "849fff4e-8551-4abb-bd2a-838d092775d7"
    }
]
```

> You can see that the `project_add` command specified a `temp_id` property
> (`c7beb07f-b226-4eb1-bf63-30d782b07b1a`) as placeholder of the actual
> `project_id`. The `item_add` command can reference to this temporary project
> ID. The API will automatically resolve these IDs.

Some commands depend on the result of previous command. For instance, you have a
command sequence: `"project_add"` and `"item_add"` which first creates a project
and then add a new task to the newly created project. In order to run the later
`item_add` command, we need to obtain the project ID returned from the previous
command. Therefore, the normal approach would be to run these two commands in
two separate HTTP requests.

The temporary resource ID feature allows you to run two or more dependent
commands in a single HTTP request. For commands that are related to creation of
resources (i.e. `item_add`, `project_add`), you can specify an extra `temp_id`
as a placeholder for the actual ID of the resource. The other commands in the
same sequence could directly refer to `temp_id` if needed.

## Response / Error

> An example of a single request sync return value:

```
{
    "sync_status": { "863aca2c-65b4-480a-90ae-af160129abbd": "ok" }
}
```

> An example of a multiple requests sync return value:

```
{
    "sync_status": {
        "32eaa699-e9d7-47ed-91ea-e58d475791f1": "ok",
        "bec5b356-3cc1-462a-9887-fe145e3e1ebf": {
            "error_code": 15,
            "error": "Invalid temporary id"
        }
    }
}
```

The result of command executions will be stored in the following response JSON
object field:

| Data                     | Description                                                                                                                                                                   |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| temp_id_mapping _Object_ | A dictionary object that maps temporary resource IDs to real resource IDs.                                                                                                    |
| sync_status _Object_     | A dictionary object containing result of each command execution. The key will be the command's `uuid` field and the value will be the result status of the command execution. |

The status result of each command execution is in the `sync_status` dictionary
object. The key is a command `uuid` and the value will be the result status of
the command execution.

There are two possible values for each command status:

- An "ok" string which signals success of the command
- An error object containing error information of a command.

Please see the adjacent code examples for the possible format of the
`sync_status`.

## Response status codes

The server uses the HTTP status codes to indicate the success or failure of a
request. As is customary in web servers, a 2xx code indicates - success, a
4xx code - an error due to incorrect user provided information, and a 5xx code -
an internal, possibly temporary, error.

| Status code               | Description                                                               |
|---------------------------|---------------------------------------------------------------------------|
| 200 OK                    | The request was processed successfully.                                   |
| 400 Bad Request           | The request was incorrect.                                                |
| 401 Unauthorized          | Authentication is required, and has failed, or has not yet been provided. |
| 403 Forbidden             | The request was valid, but for something that is forbidden.               |
| 404 Not Found             | The requested resource could not be found.                                |
| 429 Too Many Requests     | The user has sent too many requests in a given amount of time.            |
| 500 Internal Server Error | The request failed due to a server error.                                 |
| 503 Service Unavailable   | The server is currently unable to handle the request.                     |

## Batching commands

> Example of batching multiple commands:

```shell
curl https://api.todoist.com/api/v1/sync \
  -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
  -d commands='[
  {
    "type": "project_add",
    "temp_id": "0a57a3db-2ff1-4d2d-adf6-12490c13c712",
    "uuid": "2c0f6e03-c372-46ba-8e85-d94af56abcf3",
    "args": { "name": "Shopping List" }
  },
  {
    "type": "item_add",
    "temp_id": "ef3d840e-84c9-4433-9a32-86ae9a1e7d42",
    "uuid": "49ede211-12f3-42e9-8345-4c0d2b29c08d",
    "args": { "content": "Buy Milk", "project_id": "0a57a3db-2ff1-4d2d-adf6-12490c13c712" }
  },
  {
    "type": "item_add",
    "temp_id": "8a23c8cb-1d76-469d-a2c0-80a28b3ea6f6",
    "uuid": "46619250-ae02-4ab0-bd31-3c9ab0307e53",
    "args": { "content": "Buy Coffee", "project_id": "0a57a3db-2ff1-4d2d-adf6-12490c13c712" }
  },
  {
    "type": "item_add",
    "temp_id": "bf087eaf-aea9-4cb1-ab57-85188a2d428f",
    "uuid": "d0a1666b-d615-4250-aac5-65c7ea89091a",
    "args": { "content": "Buy Sugar", "project_id": "0a57a3db-2ff1-4d2d-adf6-12490c13c712" }
  }]'
```

> Example response:

```shell
{
  "sync_status": {
    "2c0f6e03-c372-46ba-8e85-d94af56abcf3": "ok",
    "49ede211-12f3-42e9-8345-4c0d2b29c08d": "ok",
    "d0a1666b-d615-4250-aac5-65c7ea89091a": "ok",
    "46619250-ae02-4ab0-bd31-3c9ab0307e53": "ok"
  },
  "temp_id_mapping": {
    "8a23c8cb-1d76-469d-a2c0-80a28b3ea6f6": "6X6HrfVQvQq5WCXH",
    "0a57a3db-2ff1-4d2d-adf6-12490c13c712": "6X6HrhXfQ9857XVG",
    "bf087eaf-aea9-4cb1-ab57-85188a2d428f": "6X6HrjHFgc3jQM8H",
    "ef3d840e-84c9-4433-9a32-86ae9a1e7d42": "6X6HrmjgW88crvMC"
  },
  "full_sync": true,
  "sync_token": "GSg4kDBAKWU7TZA_a-gcuSpxmO1lXT5bhLqUGd1F-AH69_qKEdkN_fJoBq3c"
}
```

When working with the Sync API, changes can be **batched** into one commit.
In our example, we're batching the creation of a 'Shopping List' project with three
different items.

As we've committed the changes all at once, weâre significantly reducing the amount of
network calls that have to be made, as well as ensuring weâre not running into any rate
limiting issues.

## Incremental sync

The Sync API allows clients to retrieve only updated resources, and this is done
by using the `sync_token` in your Sync API request.

On your initial sync request, specify `sync_token=*` in your request, and all
the user's active resource data will be returned. The server will also
return a new `sync_token` in the Sync API response.

In your subsequent Sync request, use the `sync_token` that you received from
your previous sync response, and the Todoist API server will return only the
updated resource data.

### Full sync data delay

For big accounts, the data in the initial sync may be returned with some delay,
and newer objects and updates may seem to be missing. The `full_sync_date_utc`
attribute should be the same or very close to the current UTC date. If you notice a
bigger time difference, it's recommended to do an incremental sync using the
`sync_token` included in that initial sync response to get the latest updates.