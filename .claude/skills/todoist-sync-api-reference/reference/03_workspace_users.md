# Workspace Users

**`workspace_users` are not returned in full sync responses, only in incremental sync**. To keep a list of workspace users up-to-date, clients should first [list all workspace users](#tag/Workspace/operation/get_workspaces_users_api_v1_workspaces_users_get), then use incremental sync to update that initial list as needed.

`workspace_users` are not the same as collaborators. Two users can be members of a common workspace without having a common shared project, so they will both âseeâ each other in `workspace_users` but not in collaborators.

Guests will not receive `workspace_users` sync events or resources.

> An example workspace_users object:

```
{
    "user_id": "1855581",
    "workspace_id": "424876",
    "user_email": "you@example.com",
    "full_name": "Example User",
    "timezone": "GMT +3:00",
    "avatar_big": "https://*.cloudfront.net/*_big.jpg",
    "avatar_medium": "https://*.cloudfront.net/*_medium.jpg",
    "avatar_s640": "https://*.cloudfront.net/*_s640.jpg",
    "avatar_small": "https://*.cloudfront.net/*_small.jpg",
    "image_id": "d160009dfd52b991030d55227003450f",
    "role": "MEMBER"
    "is_deleted": false,
}
```

#### Properties

| Property               | Description                                                                                                                                                                                          |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| user_id _String_       | The user ID.                                                                                                                                                                                         |
| workspace_id _String_  | The workspace ID for this user.                                                                                                                                                                      |
| user_email _String_    | The user email.                                                                                                                                                                                      |
| full_name _String_     | The full name of the user.                                                                                                                                                                           |
| timezone _String_      | The timezone of the user.                                                                                                                                                                            |
| image_id _String_      | The ID of the user's avatar.                                                                                                                                                                         |
| role _String_          | The role of the user in this workspace. Possible values are: ADMIN, MEMBER, GUEST. A guest is someone who is a collaborator of a workspace project, without being an actual member of the workspace. |
| avatar_big _String_    | The link to a 195x195 pixels image of the user's avatar.                                                                                                                                             |
| avatar_medium _String_ | The link to a 60x60 pixels image of the user's avatar.                                                                                                                                               |
| avatar_s640 _String_   | The link to a 640x640 pixels image of the user's avatar.                                                                                                                                             |
| avatar_small _String_  | The link to a 35x35 pixels image of the user's avatar.                                                                                                                                               |
| is_deleted _Boolean_   | Whether the workspace user is marked as deleted.                                                                                                                                                     |

Avatar URLs are only available if the user has an avatar, in other words, when the `image_id` is not `null`.

## Change user role

> Example role change for a workspace user request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "workspace_update_user",
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",
        "args": {
            "workspace_id": "12345,
            "user_email": "user@acme.com",
            "role": "ADMIN"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  "temp_id_mapping": {"4ff1e388-5ca6-453a-b0e8-662ebf373b6b": "12345"},
  ...
}
```

Change the role of a workspace user.

_Admins or members can not be downgraded to guests._

_This command is only usable by workspace admins. Other users will get a âforbiddenâ error._

#### Command arguments

| Argument            | Required | Description                                                                                |
|---------------------|----------|--------------------------------------------------------------------------------------------|
| id _String_         | Yes      | Real or temp ID of the workspace                                                           |
| user_email _String_ | Yes      | The new member's email                                                                     |
| role _String_       | Yes      | The role to be assigned to the new member. Valid values are `GUEST`, `MEMBER` and `ADMIN`. |

## Update user sidebar preference

> Example sidebar preference update for a workspace user request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "workspace_update_user_sidebar_preference",
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",
        "args": {
            "workspace_id": "12345",
            "sidebar_preference": "A_TO_Z"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  "temp_id_mapping": {"4ff1e388-5ca6-453a-b0e8-662ebf373b6b": "12345"},
  "workspaces": [
    {
      "id": "12345",
      "sidebar_preference": "A_TO_Z",
      ...
    }
  ],
  ...
}
```

Update the sidebar preference for the requesting user in a workspace. This defines the order projects and folders are sorted in the Workspace Overview and Sidebar.

_Any workspace user can update their own sidebar preference._

#### Command arguments

| Argument                    | Required | Description                                                                |
|-----------------------------|----------|----------------------------------------------------------------------------|
| workspace_id _String_       | Yes      | Real or temp ID of the workspace                                           |
| sidebar_preference _String_ | Yes      | The sidebar preference. Valid values are `MANUAL`, `A_TO_Z`, and `Z_TO_A`. |

## Delete workspace user

> Example delete workspace user request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "workspace_delete_user",
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",
        "args": {
            "workspace_id": "12345",
            "user_email": "user@acme.com"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  ...
}
```

Remove a user from a workspace. That user is also removed from any workspace project they joined.

_This command is only usable by workspace admins. Other users will get a âforbiddenâ error._

_Admins can use this command to remove themselves from a workspace, unless they are the last admin in the workspace. In that case, a âforbiddenâ error will be returned._

#### Command arguments

| Argument            | Required | Description                           |
|---------------------|----------|---------------------------------------|
| id _String_         | Yes      | Real or temp ID of the workspace      |
| user_email _String_ | Yes      | The email of the member to be deleted |

## Invite Users to a Workspace

> Example request to invite users to a workspace through the Sync API:

```shell
$ curl https://api.todoist.com/sync/v10/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
      {
        "type": "workspace_invite",
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",
        "args": {
            "id": "12345",
            "email_list": ["foo@example.com", "bar@example.com"],
            "role": "MEMBER"
        }
      }]
    '
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  ...
}
```

This will create workspace invitations for a list of email addresses. Usable by all workspace members and admins.

#### Command arguments

| Argument                    | Required | Description                                                                                                                                                                                                                                                                  |
|-----------------------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id _String_                 | Yes      | ID of the workspace.                                                                                                                                                                                                                                                         |
| email_list _List of String_ | Yes      | A list of emails to be invited to the workspace.                                                                                                                                                                                                                             |
| role _String_               | No       | The role the user will be given if they accept the invite. Possible values are `ADMIN`, `MEMBER`, and `GUEST`. If not provided, the default value according to the plan will be used. For Starter plans, the default is ADMIN and for Business plans, the default is MEMBER. |