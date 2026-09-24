import os
import subprocess
import time
import urllib.request

from playwright.sync_api import sync_playwright


# ============================================================
# НАСТРОЙКИ
# ============================================================

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

USER_DATA_DIR = os.path.expandvars(
    r"%LOCALAPPDATA%\Google\Chrome\ChromeDebug"
)

CDP_HOST = "127.0.0.1"
CDP_PORT = 9222
CDP_URL = f"http://{CDP_HOST}:{CDP_PORT}"

# Сайт, который нужно открыть
CHATGPT_URL = "https://chatgpt.com/"


# ============================================================
# ПРОВЕРКА CDP
# ============================================================

def is_chrome_debug_running() -> bool:
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


# ============================================================
# ЗАПУСК CHROME
# ============================================================

def start_chrome_debug():
    """
    Запускает отдельный Google Chrome с отдельным профилем
    и Remote Debugging.
    """

    print("Запускаю ChromeDebug...")

    # Создаём папку профиля, если её ещё нет
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    command = [
        CHROME_PATH,
        f"--remote-debugging-port={CDP_PORT}",
        f"--user-data-dir={USER_DATA_DIR}",
    ]

    subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )

    print("ChromeDebug запущен.")


# ============================================================
# ОЖИДАНИЕ CDP
# ============================================================

def wait_for_cdp(timeout: int = 15):
    """
    Ждёт, пока Chrome откроет CDP-порт.
    """

    print(
        f"Жду подключения Chrome к "
        f"{CDP_HOST}:{CDP_PORT}..."
    )

    start_time = time.time()

    while time.time() - start_time < timeout:

        if is_chrome_debug_running():
            print("CDP доступен.")
            return

        time.sleep(0.25)

    raise RuntimeError(
        f"Chrome запустился, но CDP-порт "
        f"{CDP_PORT} не стал доступен за {timeout} секунд."
    )


# ============================================================
# ОСНОВНАЯ ПРОГРАММА
# ============================================================

def main():

    # --------------------------------------------------------
    # 1. Проверяем, запущен ли уже ChromeDebug
    # --------------------------------------------------------

    if is_chrome_debug_running():

        print("ChromeDebug уже запущен.")

        # В этом сценарии Python не владеет Chrome.
        # Поэтому не будем ждать его закрытия.
        chrome_started_by_script = False

    else:

        start_chrome_debug()

        chrome_started_by_script = True

        wait_for_cdp()


    # --------------------------------------------------------
    # 2. Подключаем Playwright к Chrome
    # --------------------------------------------------------

    print("Подключаю Playwright к Chrome через CDP...")

    with sync_playwright() as p:

        browser = p.chromium.connect_over_cdp(CDP_URL)

        print("Playwright подключён.")


        # ----------------------------------------------------
        # 3. Получаем существующий browser context
        # ----------------------------------------------------

        context = browser.contexts[0]


        # ----------------------------------------------------
        # 4. Используем первую существующую вкладку
        # ----------------------------------------------------

        if context.pages:

            page = context.pages[0]

            print("Использую существующую вкладку.")

        else:

            page = context.new_page()

            print("Создана новая вкладка.")


        # ----------------------------------------------------
        # 5. Открываем нужный сайт
        # ----------------------------------------------------

        print(f"Открываю: {CHATGPT_URL}")

        page.goto(
            CHATGPT_URL,
            wait_until="domcontentloaded"
        )


        # ----------------------------------------------------
        # 6. Информация
        # ----------------------------------------------------

        print()
        print("=" * 50)
        print("Готово.")
        print("=" * 50)
        print(f"URL:       {page.url}")
        print(f"Заголовок: {page.title()}")
        print("=" * 50)
        print()
        print("Работай в Chrome.")
        print("Для завершения программы просто закрой окно Chrome.")
        print()


        # ----------------------------------------------------
        # 7. Если Chrome запустил этот Python-скрипт —
        #    ждём закрытия Chrome
        # ----------------------------------------------------

        if chrome_started_by_script:

            print("Ожидаю закрытия Chrome...")

            while is_chrome_debug_running():

                time.sleep(1)

            print()
            print("Chrome закрыт.")
            print("Завершаю Python-программу.")

        else:

            print(
                "Chrome был запущен до запуска Python."
            )

            print(
                "Python-программа завершает работу."
            )


# ============================================================
# ТОЧКА ВХОДА
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()
        print("Программа остановлена пользователем.")

    except Exception as e:

        print()
        print("Произошла ошибка:")
        print(e)