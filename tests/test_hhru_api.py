import unittest
from unittest.mock import Mock, patch

from src.hhru_api import HeadHunterAPI  # Убедитесь, что путь к вашему классу правильный


class TestHeadHunterAPI(unittest.TestCase):
    """Тесты для класса HeadHunterAPI."""

    @patch("requests.get")
    def test_get_companies_success(self, mock_get):
        """Тест успешного получения компаний по их ID."""
        # Настраиваем мок-объект для успешного ответа
        mock_response_1 = Mock()
        mock_response_1.status_code = 200
        mock_response_1.json.return_value = {"id": "1", "name": "Test Company 1"}

        mock_response_2 = Mock()
        mock_response_2.status_code = 200
        mock_response_2.json.return_value = {"id": "2", "name": "Test Company 2"}

        # Настраиваем возврат для двух разных вызовов
        mock_get.side_effect = [mock_response_1, mock_response_2]

        companies_ids = ["1", "2"]
        companies = HeadHunterAPI.get_companies(companies_ids)

        self.assertEqual(len(companies), 2)  # Ожидаем две компании
        self.assertEqual(companies[0]["id"], "1")  # Проверяем ID первой компании
        self.assertEqual(companies[0]["name"], "Test Company 1")  # Проверяем имя первой компании
        self.assertEqual(companies[1]["id"], "2")  # Проверяем ID второй компании
        self.assertEqual(companies[1]["name"], "Test Company 2")  # Проверяем имя второй компании

    @patch("requests.get")
    def test_get_companies_failure(self, mock_get):
        """Тест неуспешного получения компаний по их ID (404 ошибка)."""
        # Настраиваем мок-объект для неуспешного ответа
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        companies_ids = ["1", "2"]
        companies = HeadHunterAPI.get_companies(companies_ids)

        self.assertEqual(len(companies), 0)  # Ожидаем, что не будет компаний

    @patch("requests.get")
    def test_get_vacancies_success(self, mock_get):
        """Тест успешного получения вакансий по ID компании."""
        # Настраиваем мок-объект для успешного ответа
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"id": "1", "name": "Vacancy 1"}, {"id": "2", "name": "Vacancy 2"}]
        }

        mock_get.return_value = mock_response

        company_id = "1"
        vacancies = HeadHunterAPI.get_vacancies(company_id)

        self.assertEqual(len(vacancies), 2)  # Ожидаем две вакансии
        self.assertEqual(vacancies[0]["id"], "1")  # Проверяем ID первой вакансии
        self.assertEqual(vacancies[1]["name"], "Vacancy 2")  # Проверяем имя второй вакансии

    @patch("requests.get")
    def test_get_vacancies_failure(self, mock_get):
        """Тест неуспешного получения вакансий по ID компании (404 ошибка)."""
        # Настраиваем мок-объект для неуспешного ответа
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        company_id = "1"
        vacancies = HeadHunterAPI.get_vacancies(company_id)

        self.assertEqual(len(vacancies), 0)  # Ожидаем, что не будет вакансий


if __name__ == "__main__":
    unittest.main()
