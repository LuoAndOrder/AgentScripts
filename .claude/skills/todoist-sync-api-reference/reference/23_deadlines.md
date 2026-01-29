# Deadlines

Similar to due dates, deadlines can be set on tasks, and can be used to differentiate
between when a task should be started, and when it must be done by.

Unlike due dates, deadlines only support non-recurring dates with no time component.

You can find our more information about
[deadlines](https://www.todoist.com/help/articles/introduction-to-deadlines-uMqbSLM6U) in
our Help Center.

## Example deadline object

```json
{
    "date": "2016-12-01"
}
```

#### Properties

| Property      | Description                                                                                                                                                                                                                                          |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| date _string_ | Deadline in the format of `YYYY-MM-DD` ([RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339)).                                                                                                                                                  |
| lang _string_ | Only returned on the output, for future compatibility reasons. Currently unused in the processing of the `date` property. Possible values are: `en`, `da`, `pl`, `zh`, `ko`, `de`, `pt`, `ja`, `it`, `fr`, `sv`, `ru`, `es`, `nl`, `fi`, `nb`, `tw`. |

## Create or update deadlines

Usually you create deadlines when you create a new task, or  you want to update a
deadline for an object. In both cases due date is provided as a `deadline` attribute of
an object.

#### Create or update deadline

> Input example

```json
"deadline": {"date":  "2024-01-25"}
```

> Output example

```json
"deadline": {
    "date": "2024-01-25",
    "lang": "en"
}
```

