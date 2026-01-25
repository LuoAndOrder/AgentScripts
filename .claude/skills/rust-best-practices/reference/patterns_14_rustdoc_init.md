# Easy Doc Initialization

Source: https://rust-unofficial.github.io/patterns/

# Easy doc initialization

## Description

If a struct takes significant effort to initialize when writing docs, it can be
quicker to wrap your example with a helper function which takes the struct as an
argument.

## Motivation

Sometimes there is a struct with multiple or complicated parameters and several
methods. Each of these methods should have examples.

For example:

```rust
struct Connection {
    name: String,
    stream: TcpStream,
}

impl Connection {
    /// Sends a request over the connection.
    ///
    /// # Example
    /// ```no_run
    /// # // Boilerplate are required to get an example working.
    /// # let stream = TcpStream::connect("127.0.0.1:34254");
    /// # let connection = Connection { name: "foo".to_owned(), stream };
    /// # let request = Request::new("RequestId", RequestType::Get, "payload");
    /// let response = connection.send_request(request);
    /// assert!(response.is_ok());
    /// ```
    fn send_request(&self, request: Request) -> Result<Status, SendErr> {
        // ...
    }

    /// Oh no, all that boilerplate needs to be repeated here!
    fn check_status(&self) -> Status {
        // ...
    }
}
```

## Example

Instead of typing all of this boilerplate to create aConnectionandRequest, it is easier to just create a wrapping helper function which takes
them as arguments:

```rust
struct Connection {
    name: String,
    stream: TcpStream,
}

impl Connection {
    /// Sends a request over the connection.
    ///
    /// # Example
    /// ```
    /// # fn call_send(connection: Connection, request: Request) {
    /// let response = connection.send_request(request);
    /// assert!(response.is_ok());
    /// # }
    /// ```
    fn send_request(&self, request: Request) -> Result<Status, SendErr> {
        // ...
    }
}
```

Notein the above example the lineassert!(response.is_ok());will not
actually run while testing because it is inside a function which is never
invoked.

## Advantages

This is much more concise and avoids repetitive code in examples.

## Disadvantages

As example is in a function, the code will not be tested. Though it will still
be checked to make sure it compiles when running acargo test. So this pattern
is most useful when you needno_run. With this, you do not need to addno_run.

## Discussion

If assertions are not required this pattern works well.

If they are, an alternative can be to create a public method to create a helper
instance which is annotated with#[doc(hidden)](so that users won’t see it).
Then this method can be called inside of rustdoc because it is part of the
crate’s public API.
