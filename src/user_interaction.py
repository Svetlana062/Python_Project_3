import json

from src.vacancy_manager import VacancyManager
from src.db_manager import DBManager


class UserInteraction:
    def __init__(self):
        """Инициализация класса UserInteraction."""
        self.db_manager = DBManager()  # Создаем экземпляр DBManager
        self.vacancy_manager = VacancyManager(self.db_manager)  # Создаем экземпляр VacancyManager

    @staticmethod
    def load_companies(file_path):
        try:
            with open(file_path) as f:
                return json.load(f)
        except FileNotFoundError:
            print("Файл не найден.")
            return []
        except json.JSONDecodeError:
            print("Ошибка при чтении JSON файла.")
            return []
        except Exception as e:
            print(f"Ошибка: {e}")
            return []

    def run(self):
        """Основной метод для запуска взаимодействия с пользователем."""
        while True:
            print("1. Загрузить компании из файла")
            print("2. Получить и сохранить вакансии")
            print("3. Выход")

            choice = input("Выберите действие: ")

            if choice == "1":
                file_path = input("Введите путь к файлу с компаниями: ")
                companies = self.load_companies(file_path)
                if companies:
                    self.vacancy_manager.fetch_and_store_companies(companies)
                    print("Компании успешно загружены и сохранены в базе данных.")

            elif choice == "2":
                company_ids = input("Введите ID компаний через запятую: ")
                try:
                    company_ids = [int(company_id.strip()) for company_id in company_ids.split(",")]
                    companies = [{"id": company_id} for company_id in company_ids]
                    self.vacancy_manager.fetch_and_store_vacancies(companies)
                    print("Вакансии успешно загружены и сохранены.")
                except ValueError:
                    print("Ошибка: убедитесь, что вы вводите только числовые значения.")

            elif choice == "3":
                print("Выход из программы.")
                break

            else:
                print("Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    user_interaction = UserInteraction()
    user_interaction.run()
