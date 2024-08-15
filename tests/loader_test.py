import unittest
from unittest.mock import patch, MagicMock
import os

from tassistant_bot.loader import (
    Module,
    extract_repo_name,
    ModuleLoader,
)


class TestModuleLoaderFunctions(unittest.TestCase):
    def test_extract_repo_name(self):
        repo_url = "https://github.com/user/repo_name.git"
        repo_name = extract_repo_name(repo_url)
        self.assertEqual(repo_name, "repo_name")

        invalid_url = "https://github.com/user/"
        repo_name = extract_repo_name(invalid_url)
        self.assertIsNone(repo_name)


class TestModule(unittest.TestCase):
    @patch("tassistant_bot.loader.get_locales")
    def test_load_locale(self, mock_get_locales):
        mock_get_locales.return_value = {"en": {}, "ru": {}}
        base_path = "/some/path"
        module = Module(base_path)
        module.Meta.module_name = "test_module"

        module.load_locale()

        mock_get_locales.assert_called_once_with(os.path.join(base_path, "locale"))

    @patch("tassistant_bot.loader.load_directory_modules")
    def test_load_services(self, mock_load_directory_modules):
        base_path = "/some/path"
        module = Module(base_path)

        module.load_services()

        mock_load_directory_modules.assert_called_once_with(
            os.path.join(base_path, "services")
        )


class TestModuleLoader(unittest.TestCase):
    @patch("tassistant_bot.loader.Client")
    def setUp(self, mock_client):
        self.mock_client = mock_client
        self.module_loader = ModuleLoader(client=self.mock_client)

    @patch("git.Repo.clone_from")
    @patch("tassistant_bot.loader.extract_repo_name")
    @patch("os.path.exists")
    def test_download_module(
        self, mock_exists, mock_extract_repo_name, mock_clone_from
    ):
        mock_exists.return_value = False
        mock_extract_repo_name.return_value = "test_repo"

        self.module_loader.download_module("https://github.com/user/test_repo.git")

        mock_clone_from.assert_called_once()

    @patch("tassistant_bot.loader.inspect.getmembers")
    @patch("tassistant_bot.loader.importlib.util.spec_from_file_location")
    @patch("tassistant_bot.loader.importlib.util.module_from_spec")
    def test_load_module(
        self, mock_module_from_spec, mock_spec_from_file_location, mock_getmembers
    ):
        mock_module = MagicMock()
        mock_module_from_spec.return_value = mock_module
        mock_spec = MagicMock()
        mock_spec_from_file_location.return_value = mock_spec
        mock_class = MagicMock()
        mock_class.__name__ = "TestClass"
        mock_getmembers.return_value = [("TestClass", mock_class)]

        self.module_loader.load_module("test_module")

        mock_spec_from_file_location.assert_called_once()
        mock_module_from_spec.assert_called_once_with(mock_spec)
        mock_getmembers.assert_called_once()

    def test_get_command_prefix(self):
        prefix = self.module_loader.get_command_prefix()
        self.assertEqual(prefix, "/")

    @patch("os.path.exists")
    @patch("os.path.join")
    @patch("os.listdir")
    def test_load_modules(self, mock_listdir, mock_join, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ["module1", "module2"]

        self.module_loader.load_modules("test_module")

        mock_listdir.assert_called()
        mock_exists.assert_called()


if __name__ == "__main__":
    unittest.main()
