# Request Limits

### Payload Size

There is a 1MiB HTTP request body limit on POST requests.

The maximum payload size for an [attachment upload](#uploads) is dependent on the current user plan.
This value is indicated by the `upload_limit_mb` property of the [user plan limits](#user-plan-limits) object.

### Header Size

Total size of HTTP headers cannot exceed 65 KiB.

### Processing Timeouts

There are processing timeouts associated with each endpoint, and these vary
depending on the type of action being performed.

| Type             | Limit      |
| ---------------- | ---------- |
| Uploads          | 5 minutes  |
| Standard Request | 15 seconds |

### Rate Limiting

Limits are applied differently for full and partial syncs. You should ideally only make a full sync on your initial request and then subsequently perform incremental syncs as this is faster and more efficient.

See the sync section for further information on [incremental sync](#read-resources).

For each user, you can make a maximum of 1000 partial sync requests within a 15 minute period.

For each user, you can make a maximum of 100 full sync requests within a 15 minute period.

You can reduce the number of requests you make by batching up to 100 commands in each request and it will still count as one.
See the [Batching Commands](#batching-commands) section for further information.

### Maximum Sync Commands

The maximum number of commands is 100 per request. This restriction is applied to prevent
timeouts and other problems when dealing with large requests.
