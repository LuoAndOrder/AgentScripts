# Live Notifications

> Examples of live notifications:

```
{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "1",
    "invitation_id": "456",
    "invitation_secret": "abcdefghijklmno",
    "notification_key": "notification_123",
    "notification_type": "share_invitation_sent",
    "seq_no": 12345567890,
    "state": "accepted"
}

{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "2",
    "invitation_id": "456",
    "notification_key": "notification_123",
    "notification_type": "share_invitation_accepted",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "seq_no": 1234567890
}

{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "3",
    "invitation_id": "456",
    "notification_key": "notification_123",
    "notification_type": "share_invitation_rejected",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "reject_email": "me@example.com",
    "seq_no": 1234567890
}

{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "4",
    "notification_key": "notification_123",
    "notification_type": "user_left_project",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "seq_no": 1234567890
}

{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "5",
    "notification_key": "notification_123",
    "notification_type": "user_removed_from_project",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "removed_name": "Example User",
    "removed_uid": "2671366",
    "seq_no": 1234567890
}

{
    "assigned_by_uid": "2671362",
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "6",
    "item_content": "NewTask",
    "item_id": "6X7gfV9G7rWm5hW8",
    "notification_key": "notification_123",
    "notification_type": "item_assigned",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "responsible_uid": "2671355",
    "seq_no": 1234567890
}

{
    "assigned_by_uid": "2671362",
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "7",
    "item_content": "NewTask",
    "item_id": "6X7gfV9G7rWm5hW8",
    "notification_key": "notification_123",
    "notification_type": "item_completed",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "responsible_uid": "2671355",
    "seq_no": 1234567890
}

{
    "assigned_by_uid": "2671362",
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "8",
    "item_id": "6X7gfV9G7rWm5hW8",
    "item_content": "NewTask",
    "notification_key": "notification_123",
    "notification_type": "item_uncompleted",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "responsible_uid": "321",
    "seq_no": 1234567890
}

{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "id": "9",
    "item_id": "6X7gfV9G7rWm5hW8",
    "note_content": "NewTask",
    "note_id": "6X7jp7j8x7JhWFC3",
    "notification_key": "notification_123",
    "notification_type": "note_added",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "seq_no": 1234567890
}

{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "count": 5,
    "goal": 5,
    "id": "18",
    "notification_key": "notification_123",
    "notification_type": "daily_goal_reached",
    "seq_no": 1234567890
}

{
    "created_at": "2021-05-10T09:59:36.000000Z",
    "is_unread": false,
    "from_uid": "2671362",
    "count": 50,
    "goal": 50,
    "id": "19",
    "notification_key": "notification_123",
    "notification_type": "weekly_goal_reached",
    "seq_no": 1234567890
}
```

#### Types

This is the list of notifications which can be issued by the system:

| Type                                      | Description                                                                                                                                                                                                                      |
|-------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| share_invitation_sent                     | Sent to the sharing invitation receiver.                                                                                                                                                                                         |
| share_invitation_accepted                 | Sent to the sharing invitation sender, when the receiver accepts the invitation.                                                                                                                                                 |
| share_invitation_rejected                 | Sent to the sharing invitation sender, when the receiver rejects the invitation.                                                                                                                                                 |
| user_left_project                         | Sent to everyone when somebody leaves the project.                                                                                                                                                                               |
| user_removed_from_project                 | Sent to everyone, when a person removes somebody from the project.                                                                                                                                                               |
| item_assigned                             | Sent to user who is responsible for the task. Optionally it's also sent to the user who created the task initially, if the assigner and the task creator is not the same person.                                                 |
| item_completed                            | Sent to the user who assigned the task when the task is completed. Optionally it's also sent to the user who is responsible for this task, if the responsible user and the user who completed the task is not the same person.   |
| item_uncompleted                          | Sent to the user who assigned the task when the task is uncompleted. Optionally it's also sent to the user who is responsible for this task, if the responsible user and the user who completed the task is not the same person. |
| note_added                                | Sent to all members of the shared project, whenever someone adds a note to the task.                                                                                                                                             |
| workspace_invitation_created              | Sent to the invitee (if existing user) when invited to a workspace.                                                                                                                                                              |
| workspace_invitation_accepted             | Sent to the inviter, and admins of paid workspaces, when the workspace invitation is accepted.                                                                                                                                   |
| workspace_invitation_rejected             | Sent to the inviter when the workspace invitation is declined.                                                                                                                                                                   |
| project_archived                          | Sent to project collaborators when the project is archived. _Only for workspace projects at the moment._                                                                                                                         |
| removed_from_workspace                    | Sent to removed user when removed from a workspace.                                                                                                                                                                              |
| workspace_deleted                         | Sent to every workspace admin, member and guest.                                                                                                                                                                                 |
| teams_workspace_upgraded                  | Sent to workspace admins and members when workspace is upgraded to paid plan (access to paid features).                                                                                                                          |
| teams_workspace_canceled                  | Sent to workspace admins and members when workspace is back on Starter plan (no access to paid features).                                                                                                                        |
| teams_workspace_payment_failed            | Sent to the workspace billing admin on the web when a payment failed since it requires their action.                                                                                                                             |
| karma_level                               | Sent when a new karma level is reached                                                                                                                                                                                           |
| share_invitation_blocked_by_project_limit | Sent when the invitation is blocked because the user reached the project limits                                                                                                                                                  |
| workspace_user_joined_by_domain           | Sent when a user join a new workspace by domain                                                                                                                                                                                  |

#### Common properties

Some properties are common for all types of notifications, whereas some others
depend on the notification type.

Every live notification has the following properties:

| Property                   | Description                                                                                                |
|----------------------------|------------------------------------------------------------------------------------------------------------|
| id _String_                | The ID of the live notification.                                                                           |
| created_at _String_        | Live notification creation date.                                                                           |
| from_uid _String_          | The ID of the user who initiated this live notification.                                                   |
| notification_key _String_  | Unique notification key.                                                                                   |
| notification_type _String_ | Type of notification. Different notification type define different extra fields which are described below. |
| seq_no _Integer_           | Notification sequence number.                                                                              |
| is_unread _Boolean_        | Whether the notification is marked as unread (a `true` or `false` value).                                  |

#### Specific properties

Here are the extra properties for the `*_invitation_*` types of live
notifications:

| Property                   | Description                                                                                              |
|----------------------------|----------------------------------------------------------------------------------------------------------|
| from_user _Object_         | User data, useful on `share_invitation_sent`.                                                            |
| project_name _String_      | The project name, useful for `share_invitation_*` where you may not have the project in the local model. |
| invitation_id _String_     | The invitation ID. Useful for accepting/rejecting invitations.                                           |
| invitation_secret _String_ | The invitation secret key. Useful for accepting/rejecting invitations.                                   |

Here are the extra properties for the `share_invitation_sent` type of live notifications:

| Property       | Description                                                                              |
|----------------|------------------------------------------------------------------------------------------|
| state _String_ | Invitation state. Initially `invited`, can change the state to `accepted` or `rejected`. |

Here are the extra properties for the `user_removed_from_project` type of live notifications:

| Property              | Description                   |
|-----------------------|-------------------------------|
| removed_name _String_ | The name of the user removed. |
| removed_uid _String_  | The uid of the user removed.  |

Here are the extra properties for the `workspace_invitation_created` types of live
notifications:

| Property                   | Description                                                                              |
|----------------------------|------------------------------------------------------------------------------------------|
| from_user _Object_         | User data, same as in `share_invitation_sent`.                                           |
| workspace_id _Integer_     | The ID of the workspace.                                                                 |
| workspace_name _String_    | Name of the workspace.                                                                   |
| invitation_id _String_     | The invitation ID. Useful for accepting/rejecting invitations.                           |
| invitation_secret _String_ | Invitation secret. Should be used to accept or reject invitation.                        |
| state _String_             | Invitation state. Initially `invited`, can change the state to `accepted` or `rejected`. |

Here are the extra properties for the `workspace_invitation_accepted` and `workspace_invitation_rejected` types of live
notifications:

| Property                | Description                                                    |
|-------------------------|----------------------------------------------------------------|
| from_user _Object_      | User data, same as in `share_invitation_sent`.                 |
| workspace_id _Integer_  | The ID of the workspace.                                       |
| workspace_name _String_ | Name of the workspace.                                         |
| invitation_id _String_  | The invitation ID. Useful for accepting/rejecting invitations. |

Here are the extra properties for the `removed_from_workspace` and `workspace_deleted` types of live
notifications:

| Property                | Description                                    |
|-------------------------|------------------------------------------------|
| from_user _Object_      | User data, same as in `share_invitation_sent`. |
| workspace_id _Integer_  | The ID of the workspace.                       |
| workspace_name _String_ | Name of the workspace.                         |

Here are the extra properties for the `teams_workspace_upgraded`, `teams_workspace_canceled` and `teams_workspace_payment_failed` types of live notifications:

| Property                | Description                                                                    |
|-------------------------|--------------------------------------------------------------------------------|
| workspace_id _Integer_  | The ID of the workspace.                                                       |
| workspace_name _String_ | Name of the workspace.                                                         |
| plan_type _String_      | Tariff plan name for the workspace. Valid values are `STARTER` and `BUSINESS`. |

Here are the extra properties for the `project_archived` types of live
notifications:

| Property              | Description                                    |
|-----------------------|------------------------------------------------|
| from_user _Object_    | User data, same as in `share_invitation_sent`. |
| project_id _Integer_  | The ID of the project.                         |
| project_name _String_ | Name of the project.                           |

## Set last known

> Example set last known notification request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "live_notifications_set_last_read",
        "uuid": "588b9ccf-29c0-4837-8bbc-fc858c0c6df8",
        "args": {"id": "1234"}
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"588b9ccf-29c0-4837-8bbc-fc858c0c6df8": "ok"},
  ...
}
```

Set the last known notification.

#### Command arguments

| Argument    | Required | Description                                                                         |
|-------------|----------|-------------------------------------------------------------------------------------|
| id _String_ | Yes      | The ID of the last known notification (a number or `0` or `null` to mark all read). |

## Mark as read

> Example mark notification read request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "live_notifications_mark_read",
        "uuid": "588b9ccf-29c0-4837-8bbc-fc858c0c6df8",
        "args": {"ids": ["1234"]}
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"588b9ccf-29c0-4837-8bbc-fc858c0c6df8": "ok"},
  ...
}
```

Mark the notifications as read.

#### Command arguments

| Argument              | Required | Description                   |
|-----------------------|----------|-------------------------------|
| ids _Array of String_ | Yes      | The IDs of the notifications. |

## Mark all as read

> Example mark all notifications read request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "live_notifications_mark_read_all",
        "uuid": "588b9ccf-29c0-4837-8bbc-fc858c0c6df8"
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"588b9ccf-29c0-4837-8bbc-fc858c0c6df8": "ok"},
  ...
}
```

Mark all notifications as read.

## Mark as unread

> Example mark notification unread request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "live_notifications_mark_unread",
        "uuid": "588b9ccf-29c0-4837-8bbc-fc858c0c6df8",
        "args": {"ids": ["1234"]}
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"588b9ccf-29c0-4837-8bbc-fc858c0c6df8": "ok"},
  ...
}
```

Mark the notifications as unread.

#### Command arguments

| Argument              | Required | Description                   |
|-----------------------|----------|-------------------------------|
| ids _Array of String_ | Yes      | The IDs of the notifications. |