import requests


class HeadHunterAPI:
    """Класс для взаимодействия с API hh.ru."""

    BASE_URL = "https://api.hh.ru"

    @staticmethod
    def get_companies(companies_ids: list) -> list:
        """Получает данные о компаниях по их ID."""
        companies = []
        for company_id in companies_ids:
            response = requests.get(f"{HeadHunterAPI.BASE_URL}/employers/{company_id}")
            if response.status_code == 200:
                companies.append(response.json())
        return companies

    @staticmethod
    def get_vacancies(company_id: str) -> list:
        """Получает вакансии для заданной компании."""
        response = requests.get(f"{HeadHunterAPI.BASE_URL}/vacancies?employer_id={company_id}")
        if response.status_code == 200:
            return response.json().get("items", [])
        return []
