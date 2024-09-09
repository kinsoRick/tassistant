# Config Class Overview

The `Config` class provides a way to manage application configuration using environment variables. It uses the Singleton pattern to ensure that only one instance of the configuration is created throughout the application.

## What is the `Config` Class?

The `Config` class is designed to handle configuration settings stored in a `.env` file. It allows you to:
- Load and manage configuration from the `.env` file.
- Retrieve and update configuration values.
- Save changes back to the `.env` file.

## Features

- **Singleton Pattern**: Ensures that only one instance of the configuration is used.
- **Environment Variable Management**: Loads, retrieves, updates, and saves configuration values.
- **Automatic File Management**: Updates the `.env` file when changes are made.

## How to Use

### 1. Initialize the `Config` Class

Create an instance of the `Config` class. By default, it will use a file named `.env` in the current working directory:

```python
from config import Config

# Initialize the Config class
config = Config(env_file=".env")

# Retrieve a configuration value with a default fallback
api_key = config.get("API_KEY", default="default_key")
print(api_key)  # Output: the value of API_KEY from the .env file or "default_key"
