# Конфигурация

Конфигурация управляется через файл `.env`. Этот файл содержит пары "ключ-значение", которые определяют различные переменные окружения, используемые в боте.

### Пример файла `.env`

```ini
TELEGRAM_API_ID=123456
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
TELEGRAM_SESSION_STRING=abcdef1234567890abcdef1234567890 # Если у вас есть
LOG_LEVEL=INFO
```

### Доступ к значениям конфигурации

Класс `Config` загружает и управляет конфигурационным файлом.

#### Пример использования

```python
config = Config()
api_id = config.get("TELEGRAM_API_ID") # Значение переменной окружения TELEGRAM_API_ID
```

Вы также можете динамически обновлять значения конфигурации:

```python
config.set("NEW_KEY", "new_value")
config.update_env_file()  # Сохранить обновленную конфигурацию в файл .env
```

---
