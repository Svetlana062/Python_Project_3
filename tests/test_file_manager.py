import unittest
from unittest.mock import mock_open, patch

from src.file_manager import FileManager


class TestFileManager(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    @patch("os.path.exists", return_value=True)
    def test_load_from_file(self, mock_exists, mock_file):
        """Тестирование загрузки данных из файла."""
        filename = "test_vacancies.json"

        result = FileManager.load_from_file(filename)

        # Проверяем, что файл был открыт с правильным именем
        mock_file.assert_called_once_with(filename, "r", encoding="utf-8")

        # Проверяем, что данные были загружены правильно
        self.assertEqual(result, {"key": "value"})

    @patch("os.path.exists", return_value=False)
    def test_load_from_file_not_found(self, mock_exists):
        """Тестирование загрузки данных из несуществующего файла."""
        filename = "non_existent_file.json"

        result = FileManager.load_from_file(filename)

        # Проверяем, что возвращается пустой словарь при отсутствии файла
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
