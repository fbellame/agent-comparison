
### Setup composio

To get started with using Composio’s Gmail tool, we need to create an integration between Composio and Gmail. This can be done using a simple command -

```sh
composio add gmail
```

To set up a trigger(basically a listener) for new emails -
``` sh
composio triggers enable gmail_new_gmail_message
```