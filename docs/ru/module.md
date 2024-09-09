# Модули (как создавать)

Модули расширяют функциональность бота, предоставляя обработчики, сервисы и команды. Каждый модуль находится в отдельной директории и загружается динамически ботом.

### Структура модуля

Каждый модуль должен содержать:

- `module.py`: Основной файл, определяющий модуль.
- `locale/`: Папка, содержащая файлы локализации.
- `services/`: Опциональные сервисы, связанные с модулем.
- `handlers/`: Обработчики, которые обрабатывают различные типы сообщений или событий.

```
tassistant-core:
├───handlers                  # (обязательная папка)
│       <file>.py
│       __init__.py
│
├───locale                    # (обязательная папка)
│   └───<lang>
│           HELP_MODULE.txt   # (обязательный файл) выводит помощь модуля
│           <file>.json       # содержит код в качестве ключа, значение в качестве перевода
│           <file>.txt        # имя файла в качестве кода, содержит перевод
│
│
├───scenarios                 # (папка для сценариев, если есть)
└───module.py                 # (обязательный файл)
```

### Как создать модуль

Чтобы создать новый модуль, выполните следующие шаги:

- Создайте новую директорию (имя модуля) внутри папки `modules`.
- Внутри этой директории создайте файл `module.py` и определите ваш модуль, расширяя класс `Module`:

```python
from tassistant_bot.loader import Module
from tassistant_bot.i18n import I18n

_ = I18n().create_module_get("tassistant-core")

class MyCustomModule(Module):
    class Meta:
        name = "My Custom module"
        description = "Этот модуль делает что-то крутое."

    async def client_ready(self, client):
        await super().client_ready(client)
        # отправить приветственное сообщение из локализации в сохраненные сообщения (облако)
        await client.send_message("me", _("WELCOME_MESSAGE"))
```

- Добавьте свои обработчики в директорию `handlers/` и сервисы в директорию `services/`.

- (На стадии разработки) Загрузите модуль в бота, вызвав:

```python
module_loader = ModuleLoader(client=my_pyrogram_client)
module_loader.load_module("MyCustomModule") # имя репозитория или папки
```

### Управление модулями (На стадии разработки)

- **Скачать модуль**: Вы можете скачать модуль из репозитория GitHub, используя метод `download_module`:

```python
module_loader.download_module('https://github.com/username/repository.git')
```

- **Загрузить модуль**: Загрузите модуль, вызвав:

```python
module_loader.load_module("module_name")
```

- **Выгрузить модуль**: Вы можете выгрузить модуль, когда он больше не нужен:

```python
module_loader.unload_module("module_name")
```

- **Обновить модуль**: Чтобы проверить обновления и перезагрузить модуль:

```python
module_loader.update_module("module_name")
```

---

### Обработчики

Обработчики в этом проекте — это функции, которые обрабатывают определенные события чата, такие как команды или сообщения, с помощью `MessageHandler` из Pyrogram. Каждый обработчик отвечает за ответ на конкретную команду или шаблон сообщения. Обработчики определяются индивидуально и затем группируются в список `all_handlers` для регистрации.

#### Создание обработчика

Чтобы создать обработчик, выполните следующие шаги:

- **Определите функцию обработчика**: Функция должна быть асинхронной и принимать два параметра: `Client` из Pyrogram и объект `Message`.
```python
async def example_handler(client: Client, message: Message):
    # Ваш код здесь
    pass
```

- **Создайте объект `MessageHandler`**: После определения функции оберните её в `MessageHandler` вместе с необходимыми фильтрами.
```python
example_message_handler = MessageHandler(
    example_handler,
    filters.command("example_command", prefixes=ModuleLoader().get_command_prefix()) & filters.me
)
```

- **Добавьте обработчик в список `all_handlers`**: Этот список должен содержать все обработчики, которые будут зарегистрированы в боте.
```python
all_handlers = [
    example_message_handler,
    # Добавьте другие обработчики здесь
]
```

#### Пример обработчика

Вот пример обработчика, который слушает команду и удаляет сообщение после обработки:
```python
async def hello_handler(client: Client, message: Message):
    await message.delete()
    await client.send_message(message.chat.id, "Hello, world!")

hello_message_handler = MessageHandler(
    hello_handler,
    filters.command(
        "hello",

        # получает префикс от Tassistant
        prefixes=ModuleLoader().get_command_prefix()
    ) & filters.me
)

all_handlers = [
    hello_message_handler,
]
```

#### Регистрация обработчиков

После определения ваших обработчиков и добавления их в список `all_handlers`, они будут зарегистрированы и готовы к использованию, когда бот запустится.

Каждый файл обработчика содержит список `all_handlers` со всеми обработчиками.

---

### Сценарии

Сценарии — это пользовательские процессы обработки сообщений, которые расширяют базовый класс `BaseScenario`. Каждый сценарий может иметь свои собственные фильтры, состояние и обработчики сообщений.

#### Структура сценария

Класс сценария должен расширять `BaseScenario`, который предоставляет следующие методы:

- `configure()`: Для настройки сценария.
- `init_all_handlers()`: Для инициализации всех связанных обработчиков.
- `post_configure()`: Дополнительная обработка после настройки сценария (опционально).

#### Как создать сценарий

1. Создайте класс, который расширяет `BaseScenario`:

```py
from tassistant_bot.scenario import BaseScenario
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.types import Message

class MyScenario(BaseScenario):
    class Meta:
        name = "MyScenario"
        description = "Обрабатывает конкретные сценарии сообщений."

    def __init__(self, filters):
        super().__init__(filters=filters)
        self.chat = None

    async def echo_handler(self, client: Client, message: Message):
       await message.reply(f"echo -> {message.text}")

    # команда `/echo chat_name @username1, @username2, ...`
    async def configure(self, client: Client, message: Message):
        command = message.command[0]
        args = message.command[1:]

        title = args[0]
        users = [str(username).replace("@", "") for username in args[1:]]

        client_username = str(client.me.username)
        # кэширование чата в памяти
        self.chat = await client.create_group(title, users)

    async def init_all_handlers(self, client: Client):
        client.add_handler(MessageHandler(
           self.echo_handler,
           # фильтры, используя закэшированный chat.id
           filters.chat(self.chat.id)
        ))

    async def post_configure(self, client: Client, message: Message):
        await message.delete()
```

2. Зарегистрируйте сценарий в боте, добавив его в ваш модуль.

---

## Локализация

Локализация управляется через класс `I18n`. Модули могут предоставлять файлы локализации в директории `locale/`.

- **Загрузка локалей**: Модули загружают локали с помощью метода `load_locale()`.
- **Обновление локалей**: Экземпляр `I18n` динамически обновляет данные локализации.

```
├───locale
│   └───<lang>
│           HELP_MODULE.txt   # (обязательный файл) выводит помощь модуля
│           <file>.json       # содержит код в качестве ключа, значение в качестве перевода
│           <file>.txt        # имя файла в качестве кода, содержит перевод
```

---
