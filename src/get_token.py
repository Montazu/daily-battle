import re
import time
import webbrowser
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_token(cookie=None):
    url = "https://key-drop.com/pl/token"

    if cookie:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        stealth(
            driver,
            languages = ["en-US", "en"],
            vendor = "Google Inc.",
            platform = "Win32",
            webgl_vendor = "Intel Inc.",
            renderer = "Intel Iris OpenGL Engine",
            fix_hairline = True,
        )
        driver.get(url)
        driver.add_cookie({"name": "session_id", "value": cookie})
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.text_to_be_present_in_element(
                (By.XPATH, "//*"), "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9."
            )
        )
        page_content = driver.page_source
        driver.quit()
        body_pattern = r"<body>(.*?)<\/body>"
        match = re.search(body_pattern, page_content, re.DOTALL)
        return match.group(1)
    else:
        webbrowser.open(url)
        time.sleep(1)
        return input("Paste the token: ")