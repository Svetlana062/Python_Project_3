import unittest
from unittest.mock import Mock, patch

from src.vacancy_manager import VacancyManager  # Убедитесь, что путь к вашему классу правильный


class TestVacancyManager(unittest.TestCase):
    """Тесты для класса VacancyManager."""

    @patch("src.hhru_api.HeadHunterAPI.get_vacancies")
    @patch("src.file_manager.FileManager.save_to_file")
    def test_fetch_and_store_vacancies_no_results(self, mock_save_to_file, mock_get_vacancies):
        """
        Тест получения вакансий, когда API возвращает пустой список.
        """
        # Настраиваем мок-объект для получения пустого списка вакансий
        mock_get_vacancies.return_value = []

        # Создаем мок для db_manager
        mock_db_manager = Mock()

        # Создаем экземпляр VacancyManager с мок-объектом db_manager
        vacancy_manager = VacancyManager(mock_db_manager)

        companies = [{"id": "1"}, {"id": "2"}]  # Список компаний
        vacancy_manager.fetch_and_store_vacancies(companies)

        # Проверяем, что метод save_vacancy не был вызван
        mock_db_manager.save_vacancy.assert_not_called()

        # Проверяем, что метод save_to_file был вызван один раз с пустым списком
        mock_save_to_file.assert_called_once_with([], "data/vacancies.json")


if __name__ == "__main__":
    unittest.main()
