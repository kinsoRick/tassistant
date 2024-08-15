import unittest
from unittest.mock import patch, mock_open

from tassistant_bot.helpers import (
    process_json_file,
    process_txt_file,
    I18n,
)


class TestI18nFunctions(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_process_json_file(self, mock_file):
        file_path = "/some/path/file.json"
        result = process_json_file(file_path)
        self.assertEqual(result, {"key": "value"})
        mock_file.assert_called_once_with(file_path, "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data="some text content")
    def test_process_txt_file(self, mock_file):
        file_path = "/some/path/file.txt"
        result = process_txt_file(file_path)
        self.assertEqual(result, "some text content")
        mock_file.assert_called_once_with(file_path, "r", encoding="utf-8")


class TestI18n(unittest.TestCase):
    def test_update_locales(self):
        i18n = I18n()
        initial_locales = {"ru": {"HELLO": "Привет"}, "en": {"HELLO": "Hello"}}
        i18n._locales = initial_locales

        new_locales = {"ru": {"GOODBYE": "До свидания"}, "en": {"GOODBYE": "Goodbye"}}
        i18n.update_locales(new_locales)

        expected_locales = {
            "ru": {"HELLO": "Привет", "GOODBYE": "До свидания"},
            "en": {"HELLO": "Hello", "GOODBYE": "Goodbye"},
        }
        self.assertEqual(i18n._locales, expected_locales)

    def test_get(self):
        i18n = I18n()
        i18n._locales = {
            "ru": {"HELLO": "Привет", "GOODBYE": "До свидания"},
            "en": {"HELLO": "Hello", "GOODBYE": "Goodbye"},
        }
        i18n._current_locale = "ru"

        result = i18n.get("HELLO")
        self.assertEqual(result, "Привет")

        result = i18n.get("GOODBYE")
        self.assertEqual(result, "До свидания")

        # Test with data replacement
        i18n._locales["ru"]["WELCOME"] = "Добро пожаловать, %name%!"
        result = i18n.get("WELCOME", data={"name": "Алексей"})
        self.assertEqual(result, "Добро пожаловать, Алексей!")

        # Test missing key
        result = i18n.get("UNKNOWN_KEY")
        self.assertEqual(result, "UNKNOWN_KEY")


if __name__ == "__main__":
    unittest.main()
