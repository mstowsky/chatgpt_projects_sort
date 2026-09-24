from browser import Browser
from pages.chatgpt_page import ChatGPTPage
from page_actions import PageActions
from tests import ChatGPTTests


# ============================================================
# ОСНОВНАЯ ПРОГРАММА
# ============================================================

def main():

    browser = Browser()

    try:

        # 1. Запускаем / подключаем Chrome
        page = browser.start()

        # 2. Создаём слой действий
        actions = PageActions(page)

        # 3. Создаём Page Object ChatGPT
        chatgpt = ChatGPTPage(
            page,
            actions
        )

        # 4. Открываем ChatGPT
        chatgpt.open()

        # 5. Запускаем временный тест
        tests = ChatGPTTests(chatgpt)
        tests.test_chatgpt_input_field()

        # 6. Информация
        print()
        print("=" * 50)
        print("Готово.")
        print("=" * 50)
        print(f"URL:       {page.url}")
        print(f"Заголовок: {page.title()}")
        print("=" * 50)
        print()
        print("Работай в Chrome.")
        print(
            "Для завершения программы "
            "просто закрой окно Chrome."
        )
        print()

        # 7. Ждём закрытия Chrome
        browser.wait_for_close()

    finally:

        browser.close()


# ============================================================
# ТОЧКА ВХОДА
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()
        print(
            "Программа остановлена пользователем."
        )

    except Exception as e:

        print()
        print("Произошла ошибка:")
        print(e)