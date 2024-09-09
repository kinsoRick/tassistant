import os
import json
import re

from logging import getLogger
from typing import Dict

logger = getLogger()


def process_json_file(file_path: str) -> Dict:
    """
    Processes a JSON file and returns its data as a dictionary.

    :param file_path: Path to the JSON file.
    :return: Data from the JSON file as a dictionary.
    :example: process_json_file(os.path.join(os.getcwd(), "file.json"))
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        logger.debug(f"| I18N | process_json_file: {file_path} | {data}")
        return data


def process_txt_file(file_path: str) -> str:
    """
    Processes a text file and returns its content as a string.


    :param file_path: Path to the text file.
    :return: Content of the text file as a string.
    :example: process_txt_file(os.path.join(os.getcwd(), "file.txt"))
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
        logger.debug(f"| I18N | process_txt_file: {file_path}:\n{data}\n")
        return data


def get_locales(locale_dir: str) -> Dict[str, Dict[str, str]]:
    """
    Loads locales from the specified directory.

    Walks through all files in the directory and subdirectories. JSON files
    are processed as dictionaries, and text files are processed as strings.

    :param locale_dir: Path to the directory containing locale files.
    :return: A dictionary where keys are directory names (name of language) and values are dictionaries of locales.
    :example: get_locales(os.path.join(os.getcwd(), "locales"))
    """
    locales = {}
    for root, dirs, files in os.walk(locale_dir):
        logger.debug(f"| I18N | dirs/files | {dirs} | {files}")
        for file in files:
            dir_name = re.findall(r"[^\\/]+", root)[-1]
            file_path = os.path.join(root, file)

            if dir_name not in locales:
                locales[dir_name] = {}

            if file.endswith(".json"):
                locales[dir_name].update(process_json_file(file_path))
            elif file.endswith(".txt"):
                file_name = file.replace(".txt", "").upper()
                locales[dir_name][file_name] = process_txt_file(file_path)

    logger.debug(f"| I18N | {locales}")
    logger.info(f"| I18N | {len(locales)} locales loaded")
    return locales
