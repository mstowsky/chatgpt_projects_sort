from locators import CHATGPT_TEXTBOX


class ChatGPTPage:

    URL = "https://chatgpt.com/"

    def __init__(self, page, actions):

        self.page = page
        self.actions = actions

    # ========================================================
    # ОТКРЫТИЕ СТРАНИЦЫ
    # ========================================================

    def open(self):
        """
        Открывает ChatGPT и ждёт загрузки страницы.
        """

        self.page.goto(
            self.URL,
            wait_until="domcontentloaded"
        )

        print("ChatGPT открыт.")

    # ========================================================
    # ЭЛЕМЕНТЫ СТРАНИЦЫ
    # ========================================================

    @property
    def textbox(self):
        """
        Возвращает поле ввода ChatGPT.
        """

        return self.actions.find_by_role(
            role=CHATGPT_TEXTBOX["role"]
        )