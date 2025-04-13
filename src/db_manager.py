import psycopg2
from config import config


class DBManager:
    def __init__(self):
        """Инициализация класса DBManager и подключение к базе данных."""
        self.connection = None
        self.cursor = None
        self.connect()
        self.connection = psycopg2.connect(...)
        self.cursor = self.connection.cursor()

    def connect(self):
        """Подключение к серверу базы данных PostgreSQL."""
        try:
            params = config()
            self.connection = psycopg2.connect(**params)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def create_tables(self):
        """Создает необходимые таблицы в базе данных."""
        self.cursor.execute("DROP TABLE IF EXISTS companies;")
        self.cursor.execute("DROP TABLE IF EXISTS vacancies;")
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                hh_id INT UNIQUE NOT NULL
            );
        """
        )
        self.cursor.execute(
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
        self.connection.commit()

    def save_company(self, company):
        """Сохранение компании в базе данных."""
        try:
            insert_company = "INSERT INTO companies (name, id) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;"
            self.cursor.execute(insert_company, (company["name"], company["id"]))
            self.connection.commit()  # Не забудьте зафиксировать изменения
        except Exception as e:
            print(f"Ошибка при сохранении компании {company['name']}: {e}")

    def save_vacancy(self, vacancy):
        """Сохранение вакансии в базе данных."""

        insert_vacancy = "INSERT INTO vacancies (title, salary, url, company_id) VALUES (%s, %s, %s, %s);"
        self.cursor.execute(
            insert_vacancy, (vacancy["title"], vacancy.get("salary"), vacancy["url"], vacancy["company_id"])
        )

    def get_companies_and_vacancies_count(self):
        """Получение списка всех компаний и количества вакансий у каждой компании."""
        query = """
        SELECT c.name, COUNT(v.id) AS vacancies_count 
        FROM companies c 
        LEFT JOIN vacancies v ON c.id = v.company_id 
        GROUP BY c.name;
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        """Получение списка всех вакансий с указанием названия компании и зарплаты."""
        query = """
        SELECT v.title, v.salary, c.name AS company_name, v.url 
        FROM vacancies v 
        JOIN companies c ON v.company_id = c.id;
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """Получение средней зарплаты по всем вакансиям."""
        query = "SELECT AVG(salary) FROM vacancies;"

        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Получение списка всех вакансий с зарплатой выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        query = "SELECT * FROM vacancies WHERE salary > %s;"

        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получение списка всех вакансий, в названии которых содержатся переданные слова."""
        query = "SELECT * FROM vacancies WHERE title ILIKE %s;"

        self.cursor.execute(query, ("%" + keyword + "%",))
        return self.cursor.fetchall()

    def close(self):
        """Закрытие соединения с базой данных."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except Exception as e:
            print(f"Ошибка при закрытии соединения: {e}")
