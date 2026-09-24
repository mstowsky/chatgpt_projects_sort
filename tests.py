import inspect


class ChatGPTTests:
    def __init__(self, chatgpt_page):
        self.chatgpt = chatgpt_page

    # =================================
    # Тест поля ввода ChatGPT
    # =================================

    def test_chatgpt_input_field(self):
        current_test_name = inspect.currentframe().f_code.co_name

        print()
        print(f"ChatGPTTests: начинаю тест {current_test_name}")
        print("-" * 50)
        print("URL:", self.chatgpt.page.url)
        print("Title:", self.chatgpt.page.title())

        # Находим поле ввода
        textbox = self.chatgpt.textbox

        count = textbox.count()

        print("Найдено полей ввода:", count)

        if count == 0:

            raise RuntimeError(
                "Поле ввода ChatGPT не найдено."
            )

        # Берём первое найденное поле
        textbox = textbox.first

        # Получаем placeholder
        placeholder = self.chatgpt.actions.get_attribute(
            textbox,
            "placeholder"
        )

        print("Placeholder:", placeholder)

        # Устанавливаем фокус
        self.chatgpt.actions.focus(textbox)

        print("Фокус установлен на поле ввода.")

        # Вводим символ "1"
        self.chatgpt.actions.fill(
            textbox,
            "1"
        )

        print('В поле ввода введён символ "1".')
        print("-" * 50)
        print(f"ChatGPTTests: тест {current_test_name} завершён")
        print()

    # ============================================================
    # ИССЛЕДОВАНИЕ СТРУКТУРЫ ЧАТА:
    # ============================================================

    def test_chat_structure(self):
        current_test_name = inspect.currentframe().f_code.co_name

        print()
        print(f"ChatGPTTests: начинаю тест {current_test_name}")
        print("-" * 50)

        page = self.chatgpt.page

        print("URL:", page.url)
        print("Title:", page.title())
        print()
        print("Элементы <main>:", page.locator("main").count())
        print("Элементы <article>:", page.locator("article").count())
        print()
        print("Элементы с data-message-author-role:")

        messages = page.locator("[data-message-author-role]")
        message_count = messages.count()

        print("Количество:", message_count)

        print()
        print("Сообщения:")
        print("-" * 50)

        for i in range(message_count):

            message = messages.nth(i)

            role = message.get_attribute(
                "data-message-author-role"
            )

            text = message.inner_text()

            print()
            print(f"Сообщение #{i + 1}")
            print("Role:", role)
            print("Text:", text[:500])

        print()
        print("-" * 50)
        print(f"ChatGPTTests: тест {current_test_name} завершён")
        print()