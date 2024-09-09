## Configuration

The configuration is managed through a `.env` file. This file contains key-value pairs that define various environment variables used throughout the bot.

### Example `.env`

```ini
TELEGRAM_API_ID=123456
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
TELEGRAM_SESSION_STRING=abcdef1234567890abcdef1234567890 #If you have
LOG_LEVEL=INFO
```

### Accessing Config Values

The `Config` class loads and manages the configuration file.

#### Example Usage

```python
config = Config()
api_id = config.get("TELEGRAM_API_ID") # TELEGRAM_API_ID env value
```

You can also dynamically update configuration values:

```python
config.set("NEW_KEY", "new_value")
config.update_env_file()  # Save the updated config to the .env file
```

---
