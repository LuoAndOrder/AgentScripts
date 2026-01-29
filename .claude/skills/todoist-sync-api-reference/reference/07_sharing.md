# Sharing

Projects can be shared with other users, which are then referred to as collaborators.
This section describes the different commands that are related to sharing.

## Collaborators

> An example collaborator object:

```
{
    "id": "2671362",
    "email": "you@example.com",
    "full_name": "Example User",
    "timezone": "GMT +3:00",
    "image_id": null
}
```

There are two types of objects to get information about a userâs collaborators,
and their participation in shared projects: `collaborators` and
`collaborator_states`

Every user who shares at least one project with another user, has a
collaborators record in the API response. The record contains a restricted
subset of user-specific properties.

| Property           | Description                                                                                                                                                                                                                                                                                                                                                                                                                             |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id _String_        | The user ID of the collaborator.                                                                                                                                                                                                                                                                                                                                                                                                        |
| email _String_     | The email of the collaborator.                                                                                                                                                                                                                                                                                                                                                                                                          |
| full_name _String_ | The full name of the collaborator.                                                                                                                                                                                                                                                                                                                                                                                                      |
| timezone _String_  | The timezone of the collaborator.                                                                                                                                                                                                                                                                                                                                                                                                       |
| image_id _String_  | The image ID for the collaborator's avatar, which can be used to get an avatar from a specific URL. Specifically the `https://dcff1xvirvpfp.cloudfront.net/<image_id>_big.jpg` can be used for a big (`195x195` pixels) avatar, `https://dcff1xvirvpfp.cloudfront.net/<image_id>_medium.jpg` for a medium (`60x60` pixels) avatar, and `https://dcff1xvirvpfp.cloudfront.net/<image_id>_small.jpg` for a small (`35x35` pixels) avatar. |

Partial sync returns updated collaborator objects for users that have changed
their attributes, such as their name or email.

## Collaborator states

> An example collaborator state:

```
{
    "project_id": "6H2c63wj7x9hFJfX",
    "user_id": "2671362",
    "state": "active",
    "is_deleted": false,
    "role": "READ_WRITE",
}
```

The list of collaborators donât contain any information on how users are
connected to shared projects. To provide information about these connections,
the `collaborator_states` field should be used. Every collaborator state record
is a mere "user to shared project" mapping.

| Property             | Description                                                             |
|----------------------|-------------------------------------------------------------------------|
| project_id _String_  | The shared project ID of the user.                                      |
| user_id _String_     | The user ID of the collaborator.                                        |
| state _String_       | The status of the collaborator state, either `active` or `invited`.     |
| is_deleted _Boolean_ | Set to `true` when the collaborator leaves the shared project.          |
| role                 | The role of the collaborator in the project. _Only available for teams_ |

## Share a project

> Example share project request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "share_project",
        "temp_id": "854be9cd-965f-4ddd-a07e-6a1d4a6e6f7a",
        "uuid": "fe6637e3-03ce-4236-a202-8b28de2c8372",
        "args": {
            "project_id": "6H2c63wj7x9hFJfX",
            "email": "you@example.com"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"fe6637e3-03ce-4236-a202-8b28de2c8372": "ok"},
  ...
}
```

Share a project with another user.

_When sharing a teams project_

Workspace projects with `is_invite_only` set to true can only be shared by
workspace admins, or by project members with `ADMIN` or `CREATOR` role. Other
users will get a âforbiddenâ error. The role for the new collaborator cannot be
greater than the role of the person sharing the project.

#### Command arguments

| Argument            | Required | Description                                                                                                                                          |
|---------------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| project_id _String_ | Yes      | The project to be shared.                                                                                                                            |
| email _String_      | Yes      | The user email with whom to share the project.                                                                                                       |
| role _String_       | No       | The role of the new collaborator in the workspace project. If missing, the workspace `collaborator_role_default` will be used. _Only used for teams_ |

## Delete a collaborator

> Example delete collaborator request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "delete_collaborator",
        "uuid": "0ae55ac0-3b8d-4835-b7c3-59ba30e73ae4",
        "args": {
            "project_id": "6H2c63wj7x9hFJfX",
            "email": "you@example.com"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"0ae55ac0-3b8d-4835-b7c3-59ba30e73ae4": "ok"},
  ...
}
```

Remove a user from a shared project.
In Teams, only workspace admins or project members with `ADMIN` or `CREATOR` role can delete a collaborator. Other users will get a âforbiddenâ error.

#### Command arguments

| Argument            | Required | Description                                      |
|---------------------|----------|--------------------------------------------------|
| project_id _String_ | Yes      | The project to be affected.                      |
| email _String_      | Yes      | The user email with whom the project was shared. |

## Accept an invitation

> Example accept invitation request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "accept_invitation",
        "uuid": "4b254da4-fa2b-4a88-9439-b27903a90f7f",
        "args": {
            "invitation_id": "1234",
            "invitation_secret": "abcdefghijklmno"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"4b254da4-fa2b-4a88-9439-b27903a90f7f": "ok"},
  ...
}
```

Accept an invitation to join a shared project.

#### Command arguments

| Argument                   | Required | Description                                    |
|----------------------------|----------|------------------------------------------------|
| invitation_id _String_     | Yes      | The invitation ID.                             |
| invitation_secret _String_ | Yes      | The secret fetched from the live notification. |

## Reject an invitation

> Example reject invitation request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "reject_invitation",
        "uuid": "284fd900-c36f-44e5-ab92-ee93455e50e0",
        "args": {
            "invitation_id": "1234",
            "invitation_secret": "abcdefghijklmno"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"284fd900-c36f-44e5-ab92-ee93455e50e0": "ok"},
  ...
}
```

Reject an invitation to join a shared project.

#### Command arguments

| Argument                   | Required | Description                                    |
|----------------------------|----------|------------------------------------------------|
| invitation_id _String_     | Yes      | The invitation ID.                             |
| invitation_secret _String_ | Yes      | The secret fetched from the live notification. |

## Delete an invitation

> Example delete invitation request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "delete_invitation",
        "uuid": "399f6a8d-ddea-4146-ae8e-b41fb8ff6945",
        "args": {"invitation_id": "1234"}
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"399f6a8d-ddea-4146-ae8e-b41fb8ff6945": "ok"},
  ...
}
```

Delete an invitation to join a shared project.

#### Command arguments

| Argument               | Required | Description                   |
|------------------------|----------|-------------------------------|
| invitation_id _String_ | Yes      | The invitation to be deleted. |