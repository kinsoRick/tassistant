# I18n Class Overview

The `I18n` class is designed to handle internationalization (i18n) in Python applications using the Pyrogram library. It supports multiple locales and follows the Singleton pattern to ensure a single instance manages locale data throughout the application.

## What is the `I18n` Class?

The `I18n` class provides methods to manage and retrieve localized strings. It allows you to:
- Load locale data from a directory.
- Update and organize locale data.
- Retrieve localized strings with optional placeholder replacement.

## Features

- **Singleton Pattern**: Ensures only one instance of the class is created.
- **Locale Management**: Supports multiple locales and allows updating data dynamically.
- **Placeholder Replacement**: Formats localized strings with dynamic data.

## How to Use

Create an instance of the `I18n` class by specifying the desired locale and locale directory:

```python
from i18n import I18n

i18n = I18n(locale_dir="locale")

locales = {
    "ru": {
        "example": "Пример"
    }
}
i18n.update_locales(locales)

_ = i18n.get

print(_("example")) # Пример
