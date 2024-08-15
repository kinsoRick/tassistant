# -*- coding: utf-8 -*-
import logging
import colorlog

from pyrogram import Client, idle
import asyncio

from tassistant_bot.helpers import config, I18n
from tassistant_bot.loader import ModuleLoader


formatter = colorlog.ColoredFormatter(
    "| %(log_color)s%(asctime)s%(reset)s | %(log_color)s%(levelname)s%(reset)s | %(log_color)s%(name)s%(reset)s, "
    "%(log_color)s%(funcName)s:%(lineno)d%(reset)s: %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
    secondary_log_colors={},
    style="%",
)

log_handler = colorlog.StreamHandler()
log_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.INFO)


async def run_main():
    _ = I18n("ru").get

    app = Client(
        name="my_account",
        api_id=config.get("TELEGRAM_API_ID"),
        api_hash=config.get("TELEGRAM_API_HASH"),
    )

    # Module loader
    loader = ModuleLoader(client=app, command_prefix=".")
    loader.load_all_modules()

    await app.start()
    await app.send_message("me", _("WELCOME_MESSAGE"))
    await idle()


def run_from_poetry():
    asyncio.run(run_main())


if __name__ == "__main__":
    asyncio.run(run_main())
