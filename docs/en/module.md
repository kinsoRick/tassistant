# Modules (how to create)

Modules extend the bot’s functionality by providing handlers, services, and commands. Each module lives in a dedicated directory and is loaded dynamically by the bot.

### Module Structure

Each module should contain:

- `module.py`: The main file that defines the module.
- `locale/`: A folder containing localization files.
- `services/`: Optional services related to the module.
- `handlers/`: Handlers that process different types of messages or events.

```
tassistant-core:
├───handlers                  # (mandatory folder)
│       <file>.py
│       __init__.py
│
├───locale                    # (mandatory folder)
│   └───<lang>
│           HELP_MODULE.txt   # (mandatory file) prints help of module
│           <file>.json       # contains key as code, value as translation
│           <file>.txt        # name of file as code, contains translation
│
│
├───scenarios                 # (folder for scenarios if have)
└───module.py                 # (mandatory file)
```
### How to Create a Module

To create a new module, follow these steps:

- Create a new directory (name of module) inside the `modules` folder.
- Inside that directory, create a `module.py` file, and define your module by extending the `Module` class:

```python
from tassistant_bot.loader import Module
from tassistant_bot.i18n import I18n


_ = I18n().create_module_get("tassistant-core")

class MyCustomModule(Module):
    class Meta:
        name = "My Custom module"
        description = "This module does something cool."

    async def client_ready(self, client):
        await super().client_ready(client)
        # send welcome message from locale to saved messages (cloud)
        await client.send_message("me", _("WELCOME_MESSAGE"))
```

- Add your handlers in the `handlers/` directory and services in the `services/` directory.

- (In development) Load the module in your bot by calling:

```python
module_loader = ModuleLoader(client=my_pyrogram_client)
module_loader.load_module("MyCustomModule") # name of repo or folder
```

### Module Management (In development)

- **Download a module**: You can download a module from a GitHub repository using the `download_module` method:

```python
module_loader.download_module('https://github.com/username/repository.git')
```

- **Load a module**: Load the module by calling:

```python
module_loader.load_module("module_name")
```

- **Unload a module**: You can unload a module when it’s no longer needed:

```python
module_loader.unload_module("module_name")
```

- **Update a module**: To check for updates and reload a module:

```python
module_loader.update_module("module_name")
```

---


### Handlers

Handlers in this project are functions that handle specific chat events, such as commands or messages, using Pyrogram's `MessageHandler`. Each handler is responsible for responding to a particular command or message pattern. Handlers are defined individually and then grouped into the `all_handlers` list for registration.

#### Creating a Handler

To create a handler, follow these steps:

- **Define the handler function**: The function should be asynchronous and accept two parameters: the Pyrogram `Client` and a `Message` object.
```python
async def example_handler(client: Client, message: Message):
    # Your code here
    pass
```

- **Create the `MessageHandler` object**: After defining the function, wrap it in a `MessageHandler` along with the necessary filters.
```python
example_message_handler = MessageHandler(
    example_handler,
    filters.command("example_command", prefixes=ModuleLoader().get_command_prefix()) & filters.me
)
```

- **Add the handler to the `all_handlers` list**: This list should contain all the handlers that will be registered in the bot.
```python
all_handlers = [
    example_message_handler,
    # Add other handlers here
]
```

#### Example Handler

Here's an example of a handler that listens for a command and deletes the message after processing:
```python
async def hello_handler(client: Client, message: Message):
    await message.delete()
    await client.send_message(message.chat.id, "Hello, world!")

hello_message_handler = MessageHandler(
    hello_handler,
    filters.command(
        "hello",

        # gets prefix from Tassistant
        prefixes=ModuleLoader().get_command_prefix()
    ) & filters.me
)

all_handlers = [
    hello_message_handler,
]
```

#### Registering Handlers

After defining your handlers and adding them to the `all_handlers` list, they will be registered and ready to use when the bot starts.

Each handler file contain all_handlers lista with all handlers
___

### Scenarios

Scenarios are custom message handling processes that extend the base `BaseScenario` class. Each scenario can have its own filters, state, and message handlers.

#### Scenario Structure

A scenario class should extend `BaseScenario`, which provides the following methods:

- `configure()`: To configure the scenario.
- `init_all_handlers()`: To initialize all related handlers.
- `post_configure()`: Optional processing after the scenario is configured.

#### How to Create a Scenario

1. Create a class that extends `BaseScenario`:

```py
from tassistant_bot.scenario import BaseScenario
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.types import Message

class MyScenario(BaseScenario):
    class Meta:
        name = "MyScenario"
        description = "Handles specific message scenarios."

    def __init__(self, filters):
        super().__init__(filters=filters)
        self.chat = None

    async def echo_handler(self, client: Client, message: Message):
       await message.reply(f"echo -> {message.text}")

    # command `/echo chat_name @username1, @username2, ...`
    async def configure(self, client: Client, message: Message):
        command = message.command[0]
        args = message.command[1:]

        title = args[0]
        users = [str(username).replace("@", "") for username in args[1:]]

        client_username = str(client.me.username)
        # caching chat in memory
        self.chat = await client.create_group(title, users)

    async def init_all_handlers(self, client: Client):
        client.add_handler(MessageHandler(
           self.echo_handler,
           # filters using cached chat.id
           filters.chat(self.chat.id)
        ))

    async def post_configure(self, client: Client, message: Message):
        await message.delete()
```

2. Register the scenario with the bot by adding it to your module.

---

## Localization

Localization is handled through the `I18n` class. Modules can provide locale files in the `locale/` directory.

- **Load locales**: Modules load locales using the `load_locale()` method.
- **Update locales**: The `I18n` instance updates locale data dynamically.

```
├───locale
│   └───<lang>
│           HELP_MODULE.txt   # (mandatory file) prints help of module
│           <file>.json       # contains key as code, value as translation
│           <file>.txt        # name of file as code, contains translation
```

---
