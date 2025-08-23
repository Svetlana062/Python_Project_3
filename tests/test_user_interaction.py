import unittest
from unittest.mock import mock_open, patch

from src.user_interaction import UserInteraction


class TestUserInteraction(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1}, {"id": 2}]')
    def test_load_companies_success(self, mock_file):
        user_interaction = UserInteraction()
        companies = user_interaction.load_companies("data/employer_ids.json")

        # Проверяем, что данные загружены правильно
        expected_companies = [{"id": 1}, {"id": 2}]
        self.assertEqual(companies, expected_companies)

    @patch("os.path.exists", return_value=False)
    def test_load_companies_file_not_found(self, mock_exists):
        user_interaction = UserInteraction()
        companies = user_interaction.load_companies("data/non_existent_file.json")

        # Проверяем, что возвращается пустой список при отсутствии файла
        self.assertEqual(companies, [])


if __name__ == "__main__":
    unittest.main()
