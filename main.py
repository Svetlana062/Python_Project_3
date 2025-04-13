from src.user_interaction import UserInteraction


def main():
    """Основная функция программы."""
    try:
        # Инициализируем интерфейс пользователя
        user_interface = UserInteraction()  # Создаем экземпляр UserInteraction

        # Запускаем главное меню
        user_interface.run()  # Вызываем метод run()

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
