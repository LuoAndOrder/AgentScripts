# Quick Add API

The Quick Add API provides a natural language interface for creating tasks. It parses text similar to the Quick Add feature in Todoist applications, extracting task content, due dates, labels, priorities, and project assignments from natural language input.


## Endpoint

```
POST https://api.todoist.com/api/v1/tasks/quick
```


Add a new task using the Quick Add implementation similar to that used in
the official clients


## Request Body

Content-Type: `application/json`


### Body_40158d1f


| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `text` | string | ✓ | The text of the task that is parsed. It can include a due date in free form text, a project name starting with the `#` character (without spaces), a label starting with the `@` character, an assignee starting with the `+` character, a priority (e.g., `p1`), a deadline between `{}` (e.g. {in 3 days}), or a description starting from `//` until the end of the text. |
| `note` | string |  |  |
| `reminder` | string |  | The reminder date in free form text. |
| `auto_reminder` | boolean |  | When this option is enabled, the default reminder will be added to the new item if it has a due date with time set. See also the [auto_reminder user option](#tag/Sync/User) for more info about the default reminder. |
| `meta` | boolean |  |  |


## Response

### 200 - Success

Successful Response


### 400 - Error

Bad Request


### 401 - Error

Unauthorized


### 403 - Error

Forbidden


### 404 - Error

Not Found


## Examples


### Basic Quick Add

```bash
curl -X POST "https://api.todoist.com/api/v1/tasks/quick" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Buy milk tomorrow at 5pm"}'
```

### Quick Add with Project and Labels

```bash
curl -X POST "https://api.todoist.com/api/v1/tasks/quick" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Review PR #shopping p1 tomorrow"}'
```

### Quick Add with Meta Information

```bash
curl -X POST "https://api.todoist.com/api/v1/tasks/quick" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Call John every Monday at 9am",
    "meta": true
  }'
```

When `meta` is true, the response includes additional parsing metadata.

## Natural Language Parsing

The Quick Add API understands various natural language patterns:

### Dates and Times
- "tomorrow", "today", "next week", "next Monday"
- "at 5pm", "at 14:00"
- "every day", "every Monday", "every 2 weeks"
- "Jan 15", "2024-01-15"

### Priority
- "p1", "p2", "p3" (or "!1", "!2", "!3")
- Higher priority = lower number (p1 is highest)

### Labels
- "@label_name" - adds a label
- Multiple labels: "@work @urgent"

### Project Assignment
- "#project_name" - assigns to a project
- Supports project hierarchy: "#Work/Subproject"
