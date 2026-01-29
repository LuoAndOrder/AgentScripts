# Authorization

<blockquote class="lang-specific shell">
    <p>An authenticated request with authorization header:</p>
</blockquote>

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d sync_token='*' \
    -d resource_types='["all"]'
```

In order to make authorized calls to the Sync API, your application must provide
an [authorization
header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization)
with the appropriate `Bearer $token`. For working through the examples, you can
obtain your personal API token from the [integrations
settings](https://app.todoist.com/prefs/integrations) for your account.

To authenticate other users, your application will need to obtain a token from
them using the OAuth protocol. For information on how to obtain a token from our
service using OAuth, please see the [authorization
guide](/guides/#authorization).

For the sake of simplicity the token is not listed on every parameter table but
please note that the **token parameter is required for every resource**.

## OAuth

OAuth is also available for token generation. It's especially useful for
external applications to obtain a user authorized API token via the OAuth2
protocol. Before getting started, developers need to create their applications
in the [App Management Console](https://app.todoist.com/app/settings/integrations/app-management)
and configure a valid OAuth2 redirect URL. A registered Todoist application is
assigned a unique `Client ID` and `Client Secret` which are needed for the
OAuth2 flow.

This procedure is comprised of 3 steps.

### Step 1: Authorization request

> An example of the URL to the authorization endpoint:

```shell
https://app.todoist.com/oauth/authorize?client_id=0123456789abcdef&scope=data:read,data:delete&state=secretstring
```

Redirect users to the authorization URL at the endpoint
`https://app.todoist.com/oauth/authorize`, with the specified request parameters.

#### Required parameters

| Name      | Description                                                                                                                                               |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| client_id | The unique Client ID of the Todoist application that you registered.                                                                                      |
| scope     | A comma separated list of permissions that you would like the users to grant to your application. See the below table for detail on the available scopes. |
| state     | A unique and unguessable string. It is used to protect you against cross-site request forgery attacks.                                                    |

#### Permission scopes

| Name            | Description                                                                                                                                              |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| task:add        | Grants permission to add new tasks (the application cannot read or modify any existing data).                                                            |
| data:read       | Grants read-only access to application data, including tasks, projects, labels, and filters.                                                             |
| data:read_write | Grants read and write access to application data, including tasks, projects, labels, and filters. This scope includes `task:add` and `data:read` scopes. |
| data:delete     | Grants permission to delete application data, including tasks, labels, and filters.                                                                      |
| project:delete  | Grants permission to delete projects.                                                                                                                    |
| backups:read  | Grants permission to list backups bypassing MFA requirements. |


#### Potential errors

| Error                               | Description                                                                                                                                                                                                                                                      |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| User Rejected Authorization Request | When the user denies your authorization request, Todoist will redirect the user to the configured redirect URI with the `error` parameter: `http://example.com?error=access_denied`.                                                                             |
| Redirect URI Not Configured         | This JSON error will be returned to the requester (your user's browser) if redirect URI is not configured in the App Management Console.                                                                                                                         |
| Invalid Application Status          | When your application exceeds the maximum token limit or when your application is being suspended due to abuse, Todoist will redirect the user to the configured redirect URI with the `error` parameter: `http://example.com?error=invalid_application_status`. |
| Invalid Scope                       | When the `scope` parameter is invalid, Todoist will redirect the user to the configured redirect URI with `error` parameter: `http://example.com?error=invalid_scope`.                                                                                           |

### Step 2: Redirection to your application site

When the user grants your authorization request, the user will be redirected to
the redirect URL configured for your application. The redirect request
will come with two query parameters attached: `code` and `state`.

The `code` parameter contains the authorization code that you will use to
exchange for an access token. The `state` parameter should match the `state`
parameter that you supplied in the previous step. If the `state` is unmatched,
your request has been compromised by other parties, and the process should be
aborted.

### Step 3: Token exchange

> An example of exchanging the token:

```shell
$ curl "https://api.todoist.com/oauth/access_token" \
    -d "client_id=0123456789abcdef" \
    -d "client_secret=secret" \
    -d "code=abcdef" \
    -d "redirect_uri=https://example.com"
```

> On success, Todoist returns HTTP 200 with token in JSON object format:

```json
{
    "access_token": "0123456789abcdef0123456789abcdef01234567",
    "token_type": "Bearer"
}
```

Once you have the authorization `code`, you can exchange it for the access token
by sending a `POST` request to the following endpoint:

`https://api.todoist.com/oauth/access_token`.

#### Required parameters

| Name          | Description                                                                          |
| ------------- | ------------------------------------------------------------------------------------ |
| client_id     | The Client ID of the Todoist application that you registered.                        |
| client_secret | The Client Secret of the Todoist application that you registered.                    |
| code          | The code that was sent in the query string to the redirect URL in the previous step. |

#### Potential errors

| Error                              | Description                                                                                                                           |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Bad Authorization Code Error       | Occurs when the `code` parameter does not match the code that is given in the redirect request: `{"error": "bad_authorization_code"}` |
| Incorrect Client Credentials Error | Occurs when the `client_id` or `client_secret` parameters are incorrect: `{"error": "incorrect_application_credentials"}`             |

## Cross Origin Resource Sharing

> CORS headers example:

```shell
$ curl https://api.todoist.com/api/v1/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -H "Origin: http://example.com"

HTTP/1.1 200 OK
Access-Control-Allow-Credentials: false
Access-Control-Allow-Origin: *
```

All API endpoints not related to the initial OAuth2 flow support Cross Origin Resource
Sharing (CORS) for requests from any origin. The header
`Access-Control-Allow-Origin: *` is set for successfully authenticated requests.
