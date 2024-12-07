import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import (
    ChromeDriverManager,
)
from typing import List
import os
import time

WINDOW_CHROME_SUBPROCESS_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"'
SUBPROCESS_PORT = 9222


class ChatGPTScraper:
    def __init__(self, subprocess_path: str, subprocess_port: int):
        self.url = "https://chat.openai.com/"
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option(
            "debuggerAddress", f"127.0.0.1:{subprocess_port}"
        )
        self.driver = self._initialize_driver(subprocess_path)
        self.driver.get("https://www.chatgpt.com")

    def _initialize_driver(self, subprocess_path):
        self.open_subprocess(subprocess_path)
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=self.options
        )

    def open_subprocess(self, subprocess_path: str):
        subprocess.Popen(subprocess_path)

    def search_chatgpt(self, query: str) -> List[str]:
        results = []
        try:

            search_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "p.placeholder"))
            )

            search_box.click()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)

            time.sleep(10)  # TODO: Replace with WebDriverWait

            responses = self.driver.find_elements(
                By.CSS_SELECTOR,
                "div > div > div > div > article > div > div",
            )
            last_response = responses[-1]
            results.append(last_response.text)

        except Exception as e:
            print(f"Error during ChatGPT search: {e}")
        # finally:  # TODO: 프로그램 종료 시 브라우저 종료
        #     self.driver.quit()
        #     subprocess.Popen("taskkill /f /im chrome.exe")  # TODO: control exceptions

        return results[0]


if __name__ == "__main__":
    # Example usage
    CHROME_SUBPROCESS_PATH = os.getenv(
        "CHROME_SUBPROCESS_PATH", WINDOW_CHROME_SUBPROCESS_PATH
    )
    subprocess_port = os.getenv("SUBPROCESS_PORT", SUBPROCESS_PORT)
    scraper = ChatGPTScraper(
        subprocess_path=CHROME_SUBPROCESS_PATH, subprocess_port=SUBPROCESS_PORT
    )
    scraper.search_chatgpt("What is the capital of France?")