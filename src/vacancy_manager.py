from src.hhru_api import HeadHunterAPI
from src.file_manager import FileManager


class VacancyManager:
    def __init__(self, db_manager):
        """Инициализация класса VacancyManager."""
        self.db_manager = db_manager
        self.api = HeadHunterAPI()  # Предполагается наличие экземпляра API

    def fetch_and_store_companies(self, companies):
        """Получение и сохранение компаний в базе данных."""
        for company in companies:
            # Сохраняем компанию в БД
            try:
                self.db_manager.save_company(company)
            except Exception as e:
                print(f"Ошибка при сохранении компании: {e}")

    def fetch_and_store_vacancies(self, companies):
        """Получение и сохранение вакансий для заданных компаний."""

        all_vacancies = []  # Список для хранения всех вакансий
        for company in companies:
            try:
                vacancies = self.api.get_vacancies(company["id"])  # Получаем вакансии для компании
                all_vacancies.extend(vacancies)  # Добавляем их в общий список

                # Сохраняем каждую вакансию в БД
                for vacancy in vacancies:
                    vacancy["company_id"] = company["id"]  # Добавляем ID компании к вакансии
                    try:
                        self.db_manager.save_vacancy(vacancy)
                    except Exception as e:
                        print(f"Ошибка при сохранении вакансии {vacancy['title']}: {e}")
            except Exception as e:
                print(f"Ошибка при получении вакансий для компании {company['id']}: {e}")

        # Сохраняем все собранные вакансии в файл один раз
        FileManager.save_to_file(all_vacancies, "data/vacancies.json")
