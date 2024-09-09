# Установка

## Необходимые условия

- Python 3.10+
- Tassistant (`pip install tassistant-bot`)
- Git (`sudo apt install git`)

## Шаги для установки версии для разработки

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/kinsoRick/tassistant/tree/main && cd tassistant
   ```

2. Установите необходимые зависимости:
   ```bash
   poetry install
   ```

3. Настройте файл `.env` для вашего окружения.

4. Заполните необходимые значения в вашем файле `.env` (например, API-ключи).

5. Соберите проект:
   ```bash
   poetry build \
   ```

6. Запустите бота:
   ```bash
   poetry run python -m tassistant_bot
   ```

---
