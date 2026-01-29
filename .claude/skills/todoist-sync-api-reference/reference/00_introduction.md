# Introduction

The Todoist Sync endpoint is specially designed for efficient data sync between
clients (e.g. our mobile apps) and Todoist.

Sync requests should be made in HTTP POST (`application/x-www-form-urlencoded`).
Sync responses, including errors, will be returned in JSON.

The Sync endpoint supports the following features:

- [Batching](#tag/Sync/Overview/Batching-commands): reading and writing of
  multiple resources can be done in a single HTTP request. Batch requests help
  clients reduce the number of network calls needed to sync resources.
- [Incremental sync](#tag/Sync/Overview/Incremental-sync): You only retrieve
  data that is updated since the last time you performed a sync request.

_Refer to [Request Limits](#tag/Request-limits) to learn more about the number of requests/commands
you have for the Sync API_