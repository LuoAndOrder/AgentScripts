---
name: todoist-sync-api-reference
description: Reference documentation for the Todoist Sync API. Use this skill when building integrations with Todoist, implementing sync functionality, or needing to understand Todoist API endpoints for tasks, projects, labels, filters, reminders, comments, workspaces, and user management. Load the relevant reference file(s) based on the resource type you're working with.
---

# Todoist Sync API Reference

Complete reference documentation for the Todoist Sync API v1. The Sync API is designed for efficient data synchronization between clients and Todoist, supporting batching, incremental sync, and temporary resource IDs.

## API Endpoint

```
POST https://api.todoist.com/api/v1/sync
```

All requests use `application/x-www-form-urlencoded` format. Responses are JSON.

## Authentication

Include the Authorization header:
```
Authorization: Bearer YOUR_API_TOKEN
```

---

## Quick Reference: When to Load What

### Authentication & Authorization
| Task | Reference File |
|------|----------------|
| OAuth flow | [17_authorization.md](reference/17_authorization.md) |
| Permission scopes | [17_authorization.md](reference/17_authorization.md) |
| Token exchange | [17_authorization.md](reference/17_authorization.md) |
| Token migration | [17_authorization.md](reference/17_authorization.md) |
| CORS | [17_authorization.md](reference/17_authorization.md) |

### Core Concepts
| Task | Reference File |
|------|----------------|
| Understanding the Sync API | [01_overview.md](reference/01_overview.md) |
| Read/Write resources | [01_overview.md](reference/01_overview.md) |
| Batching commands | [01_overview.md](reference/01_overview.md) |
| Incremental sync | [01_overview.md](reference/01_overview.md) |
| Command UUIDs & Temp IDs | [01_overview.md](reference/01_overview.md) |

### Resource Types
| Resource | Reference File |
|----------|----------------|
| Tasks (items) | [14_tasks.md](reference/14_tasks.md) |
| Projects | [10_projects.md](reference/10_projects.md) |
| Sections | [08_sections.md](reference/08_sections.md) |
| Labels | [13_labels.md](reference/13_labels.md) |
| Filters | [15_filters.md](reference/15_filters.md) |
| Reminders | [09_reminders.md](reference/09_reminders.md) |
| Comments | [11_comments.md](reference/11_comments.md) |
| User settings | [06_user.md](reference/06_user.md) |
| Quick Add (natural language) | [24_quick_add.md](reference/24_quick_add.md) |

### Collaboration & Sharing
| Task | Reference File |
|------|----------------|
| Sharing projects | [07_sharing.md](reference/07_sharing.md) |
| Collaborators | [07_sharing.md](reference/07_sharing.md) |
| Workspaces | [02_workspace.md](reference/02_workspace.md) |
| Workspace users | [03_workspace_users.md](reference/03_workspace_users.md) |
| Workspace filters | [16_workspace_filters.md](reference/16_workspace_filters.md) |

### User & Notifications
| Task | Reference File |
|------|----------------|
| User properties | [06_user.md](reference/06_user.md) |
| User settings | [06_user.md](reference/06_user.md) |
| Productivity stats | [06_user.md](reference/06_user.md) |
| Live notifications | [12_live_notifications.md](reference/12_live_notifications.md) |

### View Configuration
| Task | Reference File |
|------|----------------|
| View options | [04_view_options.md](reference/04_view_options.md) |
| Project view defaults | [05_project_view_options_defaults.md](reference/05_project_view_options_defaults.md) |

### Data Formats & Limits
| Task | Reference File |
|------|----------------|
| Due date formats | [22_due_dates.md](reference/22_due_dates.md) |
| Deadline formats | [23_deadlines.md](reference/23_deadlines.md) |
| Color values | [18_colors.md](reference/18_colors.md) |
| File uploads | [19_uploads.md](reference/19_uploads.md) |
| Rate limits | [20_request_limits.md](reference/20_request_limits.md) |
| Pagination | [21_pagination.md](reference/21_pagination.md) |

---

## Common Operations

### Reading Resources
```bash
curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer $TOKEN" \
    -d sync_token='*' \
    -d resource_types='["all"]'
```

### Writing Resources (Commands)
```bash
curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer $TOKEN" \
    -d commands='[{
        "type": "item_add",
        "temp_id": "unique-temp-id",
        "uuid": "unique-command-uuid",
        "args": {"content": "Task name", "project_id": "project-id"}
    }]'
```

### Available Resource Types
`labels`, `projects`, `items`, `notes`, `sections`, `filters`, `reminders`, `reminders_location`, `locations`, `user`, `live_notifications`, `collaborators`, `user_settings`, `notification_settings`, `user_plan_limits`, `completed_info`, `stats`, `workspaces`, `workspace_users`, `workspace_filters`, `view_options`, `project_view_options_defaults`, `role_actions`

Use `"all"` to fetch everything, or prefix with `-` to exclude (e.g., `"-projects"`).

---

## Command Types by Resource

### Tasks
- `item_add` - Add a task
- `item_update` - Update a task
- `item_move` - Move a task
- `item_reorder` - Reorder tasks
- `item_delete` - Delete tasks
- `item_complete` - Complete a task
- `item_uncomplete` - Uncomplete a task
- `item_complete_recurring` - Complete recurring task
- `item_close` - Close a task
- `item_update_day_orders` - Update day orders

### Projects
- `project_add` - Add a project
- `project_update` - Update a project
- `project_move` - Move a project
- `project_delete` - Delete a project
- `project_archive` - Archive a project
- `project_unarchive` - Unarchive a project
- `project_reorder` - Reorder projects

### Sections
- `section_add` - Add a section
- `section_update` - Update a section
- `section_move` - Move a section
- `section_reorder` - Reorder sections
- `section_delete` - Delete a section
- `section_archive` - Archive a section
- `section_unarchive` - Unarchive a section

### Labels
- `label_add` - Add a personal label
- `label_update` - Update a personal label
- `label_delete` - Delete a personal label
- `label_rename` - Rename a shared label
- `label_delete_occurrences` - Delete shared label occurrences
- `label_update_orders` - Update label orders

### Filters
- `filter_add` - Add a filter
- `filter_update` - Update a filter
- `filter_delete` - Delete a filter
- `filter_update_orders` - Update filter orders

### Reminders
- `reminder_add` - Add a reminder
- `reminder_update` - Update a reminder
- `reminder_delete` - Delete a reminder

### Comments
- `note_add` - Add a task comment
- `note_update` - Update a task comment
- `note_delete` - Delete a task comment
- `project_note_add` - Add a project comment
- `project_note_update` - Update a project comment
- `project_note_delete` - Delete a project comment

---

## All Reference Files

- [00_introduction.md](reference/00_introduction.md) - Introduction to the Sync API
- [01_overview.md](reference/01_overview.md) - Overview (read/write, batching, incremental sync)
- [02_workspace.md](reference/02_workspace.md) - Workspace operations
- [03_workspace_users.md](reference/03_workspace_users.md) - Workspace user management
- [04_view_options.md](reference/04_view_options.md) - View options configuration
- [05_project_view_options_defaults.md](reference/05_project_view_options_defaults.md) - Project view defaults
- [06_user.md](reference/06_user.md) - User properties, settings, stats
- [07_sharing.md](reference/07_sharing.md) - Sharing and collaborators
- [08_sections.md](reference/08_sections.md) - Section operations
- [09_reminders.md](reference/09_reminders.md) - Reminder operations
- [10_projects.md](reference/10_projects.md) - Project operations
- [11_comments.md](reference/11_comments.md) - Task and project comments
- [12_live_notifications.md](reference/12_live_notifications.md) - Live notifications
- [13_labels.md](reference/13_labels.md) - Label operations
- [14_tasks.md](reference/14_tasks.md) - Task (item) operations
- [15_filters.md](reference/15_filters.md) - Filter operations
- [16_workspace_filters.md](reference/16_workspace_filters.md) - Workspace filter operations
- [17_authorization.md](reference/17_authorization.md) - OAuth, scopes, token exchange, CORS
- [18_colors.md](reference/18_colors.md) - Color values for projects, labels, filters
- [19_uploads.md](reference/19_uploads.md) - File upload limits
- [20_request_limits.md](reference/20_request_limits.md) - Rate limits and payload sizes
- [21_pagination.md](reference/21_pagination.md) - Cursor-based pagination
- [22_due_dates.md](reference/22_due_dates.md) - Due date formats and parsing
- [23_deadlines.md](reference/23_deadlines.md) - Deadline formats
- [24_quick_add.md](reference/24_quick_add.md) - Quick Add API (natural language task creation)
