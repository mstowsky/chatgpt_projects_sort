import os
import subprocess
import time
import urllib.request

from playwright.sync_api import sync_playwright


# ============================================================
# НАСТРОЙКИ
# ============================================================

CHROME_PATH = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
)

USER_DATA_DIR = os.path.expandvars(
    r"%LOCALAPPDATA%\Google\Chrome\ChromeDebug"
)

CDP_HOST = "127.0.0.1"
CDP_PORT = 9222

CDP_URL = (
    f"http://{CDP_HOST}:{CDP_PORT}"
)


# ============================================================
# BROWSER
# ============================================================

class Browser:

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

        self.chrome_started_by_script = False

    # ========================================================
    # ПРОВЕРКА CDP
    # ========================================================

    def is_cdp_available(self) -> bool:
        """
        Проверяет, доступен ли Chrome DevTools Protocol
        на порту 9222.
        """

        try:

            with urllib.request.urlopen(
                f"{CDP_URL}/json/version",
                timeout=1
            ) as response:

                return response.status == 200

        except Exception:

            return False

    # ========================================================
    # ЗАПУСК CHROME
    # ========================================================

    def start_chrome(self):
        """
        Запускает отдельный Google Chrome
        с отдельным профилем и Remote Debugging.
        """

        print("Запускаю ChromeDebug...")

        # Создаём папку профиля,
        # если её ещё нет.

        os.makedirs(
            USER_DATA_DIR,
            exist_ok=True
        )

        command = [
            CHROME_PATH,
            f"--remote-debugging-port={CDP_PORT}",
            f"--user-data-dir={USER_DATA_DIR}",
        ]

        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=(
                subprocess.CREATE_NEW_PROCESS_GROUP
            ),
        )

        print("ChromeDebug запущен.")

        self.chrome_started_by_script = True

    # ========================================================
    # ОЖИДАНИЕ CDP
    # ========================================================

    def wait_for_cdp(self, timeout: int = 15):
        """
        Ждёт, пока Chrome откроет CDP-порт.
        """

        print(
            f"Жду подключения Chrome к "
            f"{CDP_HOST}:{CDP_PORT}..."
        )

        start_time = time.time()

        while time.time() - start_time < timeout:

            if self.is_cdp_available():

                print("CDP доступен.")

                return

            time.sleep(0.25)

        raise RuntimeError(
            f"Chrome запустился, но CDP-порт "
            f"{CDP_PORT} не стал доступен "
            f"за {timeout} секунд."
        )

    # ========================================================
    # ПОДКЛЮЧЕНИЕ PLAYWRIGHT
    # ========================================================

    def connect(self):
        """
        Подключает Playwright к уже запущенному Chrome.
        """

        print(
            "Подключаю Playwright к Chrome "
            "через CDP..."
        )

        self.playwright = sync_playwright().start()

        self.browser = (
            self.playwright.chromium.connect_over_cdp(
                CDP_URL
            )
        )

        print("Playwright подключён.")

        # Получаем существующий browser context.

        if not self.browser.contexts:

            raise RuntimeError(
                "У Chrome не найден browser context."
            )

        self.context = self.browser.contexts[0]

        # Получаем существующую вкладку.

        if self.context.pages:

            self.page = self.context.pages[0]

            print(
                "Использую существующую вкладку."
            )

        else:

            self.page = self.context.new_page()

            print(
                "Создана новая вкладка."
            )

        return self.page

    # ========================================================
    # ОТКРЫТИЕ САЙТА
    # ========================================================

    def open(self, url):
        """
        Открывает указанный URL.
        """

        print(f"Открываю: {url}")

        self.page.goto(
            url,
            wait_until="domcontentloaded"
        )

    # ========================================================
    # ЗАПУСК
    # ========================================================

    def start(self):
        """
        Полностью подготавливает Chrome и Playwright.
        """

        # ----------------------------------------------------
        # Проверяем, запущен ли уже ChromeDebug
        # ----------------------------------------------------

        if self.is_cdp_available():

            print(
                "ChromeDebug уже запущен."
            )

            self.chrome_started_by_script = False

        else:

            self.start_chrome()

            self.wait_for_cdp()

        # ----------------------------------------------------
        # Подключаем Playwright
        # ----------------------------------------------------

        return self.connect()

    # ========================================================
    # ОЖИДАНИЕ ЗАКРЫТИЯ CHROME
    # ========================================================

    def wait_for_close(self):
        """
        Если Chrome был запущен этим Python-скриптом,
        ждёт его закрытия.
        """

        if not self.chrome_started_by_script:

            print(
                "Chrome был запущен до запуска Python."
            )

            print(
                "Python-программа завершает работу."
            )

            return

        print(
            "Ожидаю закрытия Chrome..."
        )

        while self.is_cdp_available():

            time.sleep(1)

        print()
        print("Chrome закрыт.")
        print("Завершаю Python-программу.")

    # ========================================================
    # ЗАКРЫТИЕ PLAYWRIGHT
    # ========================================================

    def close(self):
        """
        Закрывает соединение Playwright.
        """

        if self.playwright is not None:

            self.playwright.stop()

            self.playwright = None