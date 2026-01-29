# Labels

> An example personal label object:

```
{
    "id": "2156154810",
    "name": "Food",
    "color": "lime_green",
    "item_order": 0,
    "is_deleted": false,
    "is_favorite": false
}
```

There are two types of labels that can be added to Todoist tasks.
We refer to these as `personal` and `shared` labels.

#### Personal labels

Labels created by the current user will show up in their personal label list.
These labels can be customized and will stay in their account unless deleted.

A personal label can be converted to a shared label by the user if they no longer
require them to be stored against their account, but they still appear on
shared tasks.

#### Shared labels

A label created by a collaborator that doesn't share a name with an existing personal label
will appear in our clients as a shared label. These labels are gray by default and will
only stay in the shared labels list if there are any active tasks with this label.

A user can convert a shared label to a personal label at any time. The label will then become
customizable and will remain in the account even if not assigned to any active tasks.

Shared labels do not appear in the sync response for a user's account. They only appear
within the `labels` list of the [tasks](#tag/Sync/Tasks) that they are assigned to.

You can find more information on the differences between personal and shared labels in our [Help Center](https://www.todoist.com/help/articles/introduction-to-labels-dSo2eE#shared).

#### Properties (only applicable to personal labels)

| Property              | Description                                                                                               |
|-----------------------|-----------------------------------------------------------------------------------------------------------|
| id _String_           | The ID of the label.                                                                                      |
| name _String_         | The name of the label.                                                                                    |
| color _String_        | The color of the label icon. Refer to the `name` column in the [Colors](#tag/Colors) guide for more info. |
| item_order _Integer_  | Labelâs order in the label list (a number, where the smallest value should place the label at the top).   |
| is_deleted _Boolean_  | Whether the label is marked as deleted (a `true` or `false` value).                                       |
| is_favorite _Boolean_ | Whether the label is a favorite (a `true` or `false` value).                                              |

## Add a personal label

> Example add label request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "label_add",
        "temp_id": "f2f182ed-89fa-4bbb-8a42-ec6f7aa47fd0",
        "uuid": "ba204343-03a4-41ff-b964-95a102d12b35",
        "args": {"name": "Food"}
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"ba204343-03a4-41ff-b964-95a102d12b35": "ok"},
  "temp_id_mapping": {"f2f182ed-89fa-4bbb-8a42-ec6f7aa47fd0": "2156154810"},
  ...
}
```

#### Command arguments

| Argument              | Required | Description                                                                                               |
|-----------------------|----------|-----------------------------------------------------------------------------------------------------------|
| name _String_         | Yes      | The name of the label                                                                                     |
| color _String_        | No       | The color of the label icon. Refer to the `name` column in the [Colors](#tag/Colors) guide for more info. |
| item_order _Integer_  | No       | Labelâs order in the label list (a number, where the smallest value should place the label at the top).   |
| is_favorite _Boolean_ | No       | Whether the label is a favorite (a `true` or `false` value).                                              |

## Update a personal label

> Example update label request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "label_update",
        "uuid": "9c9a6e34-2382-4f43-a217-9ab017a83523",
        "args": {"id": "2156154810", "color": "berry_red"}
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"9c9a6e34-2382-4f43-a217-9ab017a83523": "ok"},
  ...
}
```

#### Command arguments

| Argument              | Required | Description                                                                                               |
|-----------------------|----------|-----------------------------------------------------------------------------------------------------------|
| id _String_           | Yes      | The ID of the label.                                                                                      |
| name _String_         | No       | The name of the label.                                                                                    |
| color _String_        | No       | The color of the label icon. Refer to the `name` column in the [Colors](#tag/Colors) guide for more info. |
| item_order _Integer_  | No       | Labelâs order in the label list.                                                                          |
| is_favorite _Boolean_ | No       | Whether the label is a favorite (a `true` or `false` value).                                              |

## Delete a personal label

> Example delete label request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "label_delete",
        "uuid": "aabaa5e0-b91b-439c-aa83-d1b35a5e9fb3",
        "args": {
            "id": "2156154810",
            "cascade": "all"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"aabaa5e0-b91b-439c-aa83-d1b35a5e9fb3": "ok"},
  ...
}
```

#### Command arguments

| Argument         | Required | Description                                                                                                                                                                                                                                                                                                                                                          |
|------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id _String_      | Yes      | The ID of the label.                                                                                                                                                                                                                                                                                                                                                 |
| cascade _String_ | No       | A string value, either `all` (default) or `none`. If no value or `all` is passed, the personal label will be removed and any instances of the label will also be removed from tasks (including tasks in shared projects). If `none` is passed, the personal label will be removed from the user's account but it will continue to appear on tasks as a shared label. |

## Rename a shared label

> Example rename shared label request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "label_rename",
        "uuid": "b863b0e5-2541-4a5a-a462-ce265ae2ff2d",
        "args": {
            "name_old": "Food",
            "name_new": "Drink"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"b863b0e5-2541-4a5a-a462-ce265ae2ff2d": "ok"},
  ...
}
```

This command enables renaming of shared labels. Any tasks containing a label matching the
value of `name_old` will be updated with the new label name.

#### Command arguments

| Argument          | Required | Description                              |
|-------------------|----------|------------------------------------------|
| name_old _String_ | Yes      | The current name of the label to modify. |
| name_new _String_ | Yes      | The new name for the label.              |

## Delete shared label occurrences

> Example delete shared label request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "label_delete_occurrences",
        "uuid": "6174264a-2842-410c-a8ff-603ec4d4736b",
        "args": {
            "name": "Shopping"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"6174264a-2842-410c-a8ff-603ec4d4736b": "ok"},
  ...
}
```

Deletes all occurrences of a shared label from any active tasks.

#### Command arguments

| Argument      | Required | Description                      |
|---------------|----------|----------------------------------|
| name _String_ | Yes      | The name of the label to remove. |

## Update multiple label orders

> Example update label orders request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands=[
    {
        "type": "label_update_orders",
        "uuid": "1402a911-5b7a-4beb-bb1f-fb9e1ed798fb",
        "args": {
            "id_order_mapping": {"2156154810":  1, "2156154820": 2}
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {
    "517560cc-f165-4ff6-947b-3adda8aef744": "ok"},
    ...
  },
  ...
}
```

#### Command arguments

| Argument                  | Required | Description                                                              |
|---------------------------|----------|--------------------------------------------------------------------------|
| id_order_mapping _Object_ | Yes      | A dictionary, where a label `id` is the key, and the `item_order` value. |