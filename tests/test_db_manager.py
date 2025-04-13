import unittest
from unittest.mock import MagicMock, patch
from src.db_manager import DBManager


class TestDBManager(unittest.TestCase):

    @patch("psycopg2.connect")
    def setUp(self, mock_connect):
        """Настройка мока для подключения к базе данных."""
        self.db_manager = DBManager()
        self.db_manager.cursor = MagicMock()
        self.db_manager.connection.commit = MagicMock()

    def test_create_tables(self):
        """Тестирование создания таблиц."""
        self.db_manager.create_tables()

        # Проверяем, что команды на удаление и создание таблиц были выполнены
        self.db_manager.cursor.execute.assert_any_call("DROP TABLE IF EXISTS companies;")
        self.db_manager.cursor.execute.assert_any_call("DROP TABLE IF EXISTS vacancies;")
        self.db_manager.cursor.execute.assert_any_call(
            """
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                hh_id INT UNIQUE NOT NULL
            );
        """
        )
        self.db_manager.cursor.execute.assert_any_call(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                salary INT,
                url VARCHAR(255) NOT NULL,
                company_id INT REFERENCES companies(id)
            );
        """
        )

    def test_save_company(self):
        """Тестирование сохранения компании."""
        company = {"name": "Test Company", "id": 1}

        self.db_manager.save_company(company)

        # Проверяем, что команда на вставку компании была выполнена
        self.db_manager.cursor.execute.assert_called_once_with(
            "INSERT INTO companies (name, id) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;",
            (company["name"], company["id"]),
        )

    def test_get_companies_and_vacancies_count(self):
        """Тестирование получения количества вакансий у компаний."""
        expected_result = [("Company A", 2), ("Company B", 3)]

        self.db_manager.cursor.fetchall.return_value = expected_result

        result = self.db_manager.get_companies_and_vacancies_count()

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, expected_result)

    def test_get_all_vacancies(self):
        """Тестирование получения всех вакансий."""
        expected_result = [("Vacancy A", 1000, "Company A", "http://example.com/vacancy_a")]

        self.db_manager.cursor.fetchall.return_value = expected_result

        result = self.db_manager.get_all_vacancies()

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, expected_result)

    def tearDown(self):
        """Закрытие соединения после тестов."""
        self.db_manager.close()


if __name__ == "__main__":
    unittest.main()
