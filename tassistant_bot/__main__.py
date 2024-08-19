# -*- coding: utf-8 -*-
import logging
import colorlog
import click

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
)

log_handler = colorlog.StreamHandler()
log_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.INFO)


@click.command()
@click.option("--api-id", default=None, help="Telegram API ID.")
@click.option("--session-string", default=None, help="Telegram Session String.")
@click.option("--api-hash", default=None, help="Telegram API Hash.")
@click.option("--use-core-module", default=True, help="Use default core pack")
@click.option("--log-level", default="INFO", help="Logging level.")
def main(api_id, api_hash, session_string, use_core_module, log_level):
    logger.setLevel(getattr(logging, log_level.upper()))

    config.set("TELEGRAM_API_ID", api_id)
    config.set("TELEGRAM_SESSION_STRING", session_string)
    config.set("TELEGRAM_API_HASH", api_hash)
    config.set("USE_CORE_MODULE", use_core_module)

    asyncio.run(run_main())


async def run_main():
    _ = I18n("ru").get

    if config.get("TELEGRAM_SESSION_STRING"):
        app = Client("my_account", session_string=config.get("TELEGRAM_SESSION_STRING"))
    else:
        app = Client(
            name="my_account",
            api_id=config.get("TELEGRAM_API_ID"),
            api_hash=config.get("TELEGRAM_API_HASH"),
        )

    await app.start()
    loader = ModuleLoader(client=app, command_prefix=".")
    loader.download_module(
        "https://github.com/kinsoRick/tassistant-core.git", "tassistant_core"
    )
    loader.update_all()
    loader.load_all_modules()

    await idle()


if __name__ == "__main__":
    main()
