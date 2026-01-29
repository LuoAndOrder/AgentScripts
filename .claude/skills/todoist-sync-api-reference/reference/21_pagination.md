# Pagination

Many endpoints in the Todoist API return paginated results to handle large datasets efficiently. This guide explains how pagination works and how to use it effectively.

## How Pagination Works

Paginated endpoints use **cursor-based pagination**. Instead of using page numbers or offsets, you use an opaque cursor token to retrieve the next set of results.

### Response Format

Paginated endpoints return a response with two key fields:

- `results`: An array containing the requested objects
- `next_cursor`: A string token for fetching the next page, or `null` if there are no more results

Example response:

```json
{
  "results": [
    {"id": "abc123", "content": "Task 1"},
    {"id": "def456", "content": "Task 2"}
  ],
  "next_cursor": "eyJwYWdlIjoyLCJsaW1pdCI6NTB9.aGFzaA"
}
```

When `next_cursor` is `null`, you've reached the end of the results.

## Making Paginated Requests

### First Request

To fetch the first page of results, make a request without a cursor parameter:

```bash
curl "https://api.todoist.com/api/v1/tasks?limit=50" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Subsequent Requests

To fetch the next page, include the `cursor` parameter with the value from `next_cursor`:

```bash
curl "https://api.todoist.com/api/v1/tasks?cursor=eyJwYWdlIjoyLCJsaW1pdCI6NTB9.aGFzaA&limit=50" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Important**: Always use the same parameters (filters, sorting, etc.) when using a cursor. Changing parameters between paginated requests may result in unexpected behavior or errors.

## Pagination Parameters

### Parameter `limit`

The `limit` parameter controls how many objects to return per page.

- **Default**: 50
- **Maximum**: 200

If you specify a limit greater than 200, the API will return a validation error.

Example with custom limit:

```bash
curl "https://api.todoist.com/api/v1/tasks?limit=100" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Parameter `cursor`

The `cursor` parameter is an opaque token returned in the `next_cursor` field of the previous response.

Cursors are user-specific and parameter-dependent, meaning they can only be used by the same user with the same request parameters (filters, project_id, etc.). Do not attempt to decode, parse, or modify cursorsâpass them as-is from the previous response.

See [Best Practices](#best-practices) for handling common scenarios.

## Best Practices

1. **Handle concurrent modifications**: Todoist data may change while you're paginating (you or collaborators adding/removing items). This can cause items to appear twice or be skipped. If consistency is critical, implement deduplication logic in your application.

2. **Don't store cursors long-term**: Cursors are meant for immediate pagination sessions. Don't persist them in databases or configuration files.

3. **Process all pages or stop early**: If you need all results, continue fetching pages until `next_cursor` is `null`. Stop early if you've found what you need.

## Error Handling

### Invalid Cursor

If you provide a malformed or tampered cursor:

```json
{
  "error": "Invalid argument value",
  "error_code": 20,
  "error_extra": {
    "argument": "cursor",
  },
  "error_tag": "INVALID_ARGUMENT_VALUE",
  "http_code": 400
}
```

**Solution**: Use the cursor exactly as returned from the previous response, or restart pagination from the beginning without a cursor parameter.

### Invalid Limit Value

If you provide a limit greater than 200:

```json
{
  "error": "Invalid argument value",
  "error_code": 20,
  "error_extra": {
    "argument": "limit",
    "expected": "Input should be less than or equal to 200",
  },
  "error_tag": "INVALID_ARGUMENT_VALUE",
  "http_code": 400
}
```

**Solution**: Use a limit value of 200 or less.

## Example: Fetching All Tasks

Here's a Python example that fetches all tasks using pagination:

```python
import requests

token = "YOUR_TOKEN"
url = "https://api.todoist.com/api/v1/tasks"
headers = {"Authorization": f"Bearer {token}"}

all_tasks = []
cursor = None

while True:
    params = {"limit": 100}
    if cursor:
        params["cursor"] = cursor

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    all_tasks.extend(data["results"])

    cursor = data.get("next_cursor")
    if not cursor:
        break

print(f"Fetched {len(all_tasks)} tasks")
```

## Activity Log Pagination

The `/api/v1/activities` endpoint uses a different pagination mechanism than the cursor-based pagination described in this guide. See the [Activities documentation](#tag/Activity) for details on how to paginate activity log results.
