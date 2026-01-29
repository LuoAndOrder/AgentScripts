# Workspace

> An example workspace object:

```
{
  "created_at": "2024-10-19T10:00:00.123456Z",
  "creator_id": "123",
  "current_active_projects": 5,
  "current_member_count": 2,
  "current_template_count": 0,
  "description": "Workspace description",
  "desktop_workspace_modal": null,
  "domain_discovery": false,
  "domain_name": null,
  "id": "1234",
  "invite_code": "ptoh4SICUu4",
  "is_collapsed": false,
  "is_deleted": false,
  "is_guest_allowed": true,
  "is_link_sharing_enabled": true,
  "is_trial_pending": false,
  "limits": {
    "current": {
      "admin_tools": false,
      "advanced_permissions": false,
      "automatic_backups": false,
      "calendar_layout": false,
      "durations": false,
      "max_collaborators": 250,
      "max_folders_per_workspace": 1000,
      "max_guests_per_workspace": 1000,
      "max_projects": 5,
      "max_workspace_templates": 100,
      "max_workspace_users": 1000,
      "max_workspaces": 50,
      "plan_name": "teams_workspaces_starter",
      "reminders": false,
      "reminders_at_due": true,
      "security_controls": false,
      "team_activity": true,
      "team_activity_plus": false,
      "upload_limit_mb": 5
    },
    "next": {
      "admin_tools": true,
      "advanced_permissions": true,
      "automatic_backups": true,
      "max_collaborators": 250,
      "max_guests_per_workspace": 1000,
      "max_projects": 1000,
      "max_workspace_users": 1000,
      "plan_name": "teams_workspaces_business",
      "reminders": true,
      "security_controls": true,
      "upload_limit_mb": 100
    }
  },
  "logo_big": "https://...",
  "logo_medium": "https://...",
  "logo_s640": "https://...",
  "logo_small": "https://...",
  "member_count_by_type": {
    "admin_count": 2,
    "guest_count": 0,
    "member_count": 0
  },
  "name": "Workspace name",
  "pending_invitations": [
    "pending@doist.com"
  ],
  "pending_invites_by_type": {
    "admin_count": 1,
    "guest_count": 0,
    "member_count": 0
  },
  "plan": "STARTER",
  "properties": {},
  "restrict_email_domains": false,
  "role": "MEMBER"
}
```

#### Properties

| Property                          | Description                                                                                                                                                                                                                                                                                                                                                                                                                     |
|-----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id _String_                       | The ID of the workspace.                                                                                                                                                                                                                                                                                                                                                                                                        |
| name _String_                     | The name of the workspace (up to 255 characters).                                                                                                                                                                                                                                                                                                                                                                               |
| description _String_              | The description of the workspace.                                                                                                                                                                                                                                                                                                                                                                                               |
| plan _String_                     | The subscription plan this workspace is currently on, either `STARTER` or `BUSINESS`.                                                                                                                                                                                                                                                                                                                                           |
| is_link_sharing_enabled _Boolean_ | True if users are allowed to join the workspace using an invitation link. Default value is True. _For guests, this field will be set to `null` as guests are not allowed to have access to this field._                                                                                                                                                                                                                         |
| is_guest_allowed _Boolean_        | True if users from outside the workspace are allowed to join or be invited to workspace projects. Default value is True.                                                                                                                                                                                                                                                                                                        |
| invite_code _String_              | The invitation code used to generate an invitation link. If `is_link_sharing_enabled` is True, anyone can join the workspace using this code. _For guests, this field will be set to `null` as guests are not allowed to have access to this field._                                                                                                                                                                            |
| role _String_                     | The role of the requesting user in this workspace. Possible values are: `ADMIN`, `MEMBER` or `GUEST`. A guest is someone who is a collaborator of a workspace project, without being an actual member of the workspace. This field can be `null` if the requesting user is not part of the workspace. For example, when receiving the workspace deletion related sync update when a user leaves or is removed from a workspace. |
| logo_big _String_                 | The URL for the big workspace logo image.                                                                                                                                                                                                                                                                                                                                                                                       |
| logo_medium _String_              | The URL for the medium workspace logo image.                                                                                                                                                                                                                                                                                                                                                                                    |
| logo_small _String_               | The URL for the small workspace logo image.                                                                                                                                                                                                                                                                                                                                                                                     |
| logo_s640 _String_                | The URL for the square 640px workspace logo image.                                                                                                                                                                                                                                                                                                                                                                              |
| limits _Object_                   | A list of restrictions for the workspace based on it's current plan, denoting what features are enabled and limits are imposed.                                                                                                                                                                                                                                                                                                 |
| creator_id _String_               | The ID of the user who created the workspace.                                                                                                                                                                                                                                                                                                                                                                                   |
| created_at _String_               | The date when the workspace was created.                                                                                                                                                                                                                                                                                                                                                                                        |
| is_deleted _Boolean_              | True if it is a deleted workspace.                                                                                                                                                                                                                                                                                                                                                                                              |
| is_collapsed _Boolean_            | True if the workspace is collapsed. This is a user-specific attribute and will reflect the requesting userâs `is_collapsed` state.                                                                                                                                                                                                                                                                                              |
| domain_name _String_              | The domain name of the workspace.                                                                                                                                                                                                                                                                                                                                                                                               |
| domain_discovery _Boolean_        | True if users with e-mail addresses in the workspace domain can join the workspace without an invitation.                                                                                                                                                                                                                                                                                                                       |
| restrict_email_domains _Boolean_  | True if only users with e-mail addresses in the workspace domain can join the workspace.                                                                                                                                                                                                                                                                                                                                        |
| properties _Object_               | Configuration properties for the workspace. See [Workspace Properties](#workspace-properties) below for detailed structure.                                                                                                                                                                                                                                                                                                     |
| default_collaborators _Object_    | Default collaborators that are automatically added to new projects in this workspace. Contains `user_ids` (array of user IDs) and `predefined_group_ids` (array of predefined group names).                                                                                                                      |
| desktop_workspace_modal _String_   | Enum value indicating when desktop should show workspace modal. Currently only supports `TRIAL_OFFER` for trial offers. `null` when no modal should be shown. This field is automatically set by the backend when mobile devices are registered and trial eligibility criteria are met. |

### Workspace Properties

The `properties` object contains configuration settings for the workspace:

| Property             | Type      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|----------------------|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| industry             | _String_  | The industry of the workspace. Possible values: `agriculture`, `arts_entertainment`, `automotive`, `banking_financial_services`, `construction`, `consulting`, `consumer_goods`, `education`, `energy_utilities`, `food_beverages`, `government_public_sector`, `healthcare_life_sciences`, `information_technology`, `insurance`, `legal_services`, `manufacturing`, `media_communications`, `non_profit`, `pharmaceuticals`, `real_estate`, `retail_wholesale`, `telecommunications`, `transportation_logistics`, `travel_hospitality`, `other`. |
| department           | _String_  | The department of the workspace. Possible values: `administration`, `customer_service`, `finance_accounting`, `human_resources`, `information_technology`, `legal`, `marketing`, `operations`, `product_development`, `research_development`, `sales`, `supply_chain_management`, `engineering`, `quality_assurance`, `executive_management`, `other`.                                                                                                                                                                                             |
| organization_size    | _String_  | The size of the organization. Possible values: `size_1`, `size_2_to_10`, `size_11_to_50`, `size_51_to_100`, `size_101_to_250`, `size_51_to_250`, `more_than_250`.                                                                                                                                                                                                                                                                                                                                                                                  |
| creator_role         | _String_  | The role of the workspace creator. Possible values: `owner_founder`, `leader`, `individual_contributor`.                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| region               | _String_  | 2 digit continent code. Possible values: `AF`, `AS`, `EU`, `NA`, `SA`, `OC`, `AN`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| country              | _String_  | 2 digit ISO 3166-1 alpha-2 country code.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| default_access_level | _String_  | Default access level for new projects in the workspace. Possible values: `restricted`, `team` (default).                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| beta_enabled         | _Boolean_ | Indicates whether beta features are enabled for this workspace. Default value is `false`.                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| acquisition_source   | _String_  | The marketing channel or source that led to workspace creation. Possible values: `high_paid_channel`                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| hdyhau               | _String_  | How did you hear about us - marketing attribution field. Possible values: `friend`, `social_media`, `ai_chatbot`, `search_engine`, `app_store`, `other`                                                                                                                                                                                                                                                                                                                                                                                            |

## Add a workspace

> Example add workspace request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "workspace_add",
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",
        "args": {
            "name": "Fellowship Workspace"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  "temp_id_mapping": {"4ff1e388-5ca6-453a-b0e8-662ebf373b6b": "6X6WMG4rmqx6FXQ9"},
  ...
}
```

Add a new workspace.

#### Command arguments

| Argument                          | Required | Description                                                                                                                                                                                                                                      |
|-----------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name _String_                     | Yes      | The name of the workspace.                                                                                                                                                                                                                       |
| description _String_              | No       | The description of the workspace (up to 1024 characters).                                                                                                                                                                                        |
| is_link_sharing_enabled _Boolean_ | No       | Indicates if users are allowed to join the workspace using an invitation link. Default value is True.                                                                                                                                            |
| is_guest_allowed _Boolean_        | No       | Indicates if users from outside the workspace are allowed to join or be invited to workspace projects. Default value is True.                                                                                                                    |
| domain_name _String_              | No       | The domain name of the workspace.                                                                                                                                                                                                                |
| domain_discovery _Boolean_        | No       | True if users with e-mail addresses in the workspace domain can join the workspace without an invitation.                                                                                                                                        |
| restrict_email_domains _Boolean_  | No       | True if only users with e-mail addresses in the workspace domain can join the workspace.                                                                                                                                                         |
| properties _Object_               | No       | Configuration properties for the workspace. See [Workspace Properties](#workspace-properties) for detailed structure.                                                                                                                            |
| default_collaborators _Object_    | No       | Default collaborators for new projects. Object with `user_ids` (array of integers) and `predefined_group_ids` (array of strings). If not provided or set to `null` then by default all workspace members are added as the default collaborators. |

## Update a workspace

> Example update workspace request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "workspace_update",
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",
        "args": {
            "id": "12345",
            "description": "Where magic happens"
        }
    }]'
```

> Example response:

```shell
{
  ...
  "sync_status": {"32774db9-a1da-4550-8d9d-910372124fa4": "ok"},
  "temp_id_mapping": {"4ff1e388-5ca6-453a-b0e8-662ebf373b6b": "6X6WMMqgq2PWxjCX"},
  ...
}
```

Update an existing workspace.

#### Command arguments

| Argument                          | Required | Description                                                                                                                                                                                                                                      |
|-----------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id _String_                       | Yes      | Real or temp ID of the workspace                                                                                                                                                                                                                 |
| name _String_                     | No       | The name of the workspace.                                                                                                                                                                                                                       |
| description _String_              | No       | The description of the workspace (up to 1024 characters).                                                                                                                                                                                        |
| is_collapsed _Boolean_            | No       | The collapsed state of the workspace for the current user                                                                                                                                                                                        |
| is_link_sharing_enabled _Boolean_ | No       | Indicates if users are allowed to join the workspace using an invitation link.                                                                                                                                                                   |
| is_guest_allowed _Boolean_        | No       | Indicates if users from outside the workspace are allowed to join or be invited to workspace projects. Default value is True.                                                                                                                    |
| invite_code _String_              | No       | Regenerate the invite_code for the workspace. Any non-empty string value will regenerate a new code, the provided value with this argument is not significant, only an indication to regenerate the code.                                        |
| domain_name _String_              | No       | The domain name of the workspace.                                                                                                                                                                                                                |
| domain_discovery _Boolean_        | No       | True if users with e-mail addresses in the workspace domain can join the workspace without an invitation.                                                                                                                                        |
| restrict_email_domains _Boolean_  | No       | True if only users with e-mail addresses in the workspace domain can join the workspace.                                                                                                                                                         |
| properties _Object_               | No       | Configuration properties for the workspace. See [Workspace Properties](#workspace-properties) for detailed structure.                                                                                                                            |
| default_collaborators _Object_    | No       | Default collaborators for new projects. Object with `user_ids` (array of integers) and `predefined_group_ids` (array of strings). If not provided or set to `null` then by default all workspace members are added as the default collaborators. |

## Leave a workspace

> Example leave workspace request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "workspace_leave",
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",
        "args": {
            "id": "6X6WMMqgq2PWxjCX",
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

Remove self from a workspace. The user is also removed from any workspace project previously joined.

#### Command arguments

| Argument    | Required | Description                      |
|-------------|----------|----------------------------------|
| id _String_ | Yes      | Real or temp ID of the workspace |

_All workspace_users can leave a workspace by themselves._

## Delete a workspace

> Example delete workspace request:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "workspace_delete",
        "temp_id": "4ff1e388-5ca6-453a-b0e8-662ebf373b6b",
        "uuid": "32774db9-a1da-4550-8d9d-910372124fa4",
        "args": {
            "id": "6X6WMRPC43g2gHVx"
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

Delete an existing workspace.

_This command is only usable by workspace admins. Other users will get a âforbiddenâ error._

#### Command arguments

| Argument    | Required | Description             |
|-------------|----------|-------------------------|
| id _String_ | Yes      | The ID of the workspace |