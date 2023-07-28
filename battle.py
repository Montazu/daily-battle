import argparse
import requests
import sys
import time
import webbrowser
import websocket
import re
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
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        driver.get(url)
        driver.add_cookie(
            {
                "name": "session_id",
                "value": cookie,
            }
        )
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


def battle_status(id):
    url = f"https://kdrp2.com/CaseBattle/gameFullData/{id}"
    response = requests.get(url)
    return response.json()["data"]


def join_battle(id, slot):
    url = f"https://kdrp2.com/CaseBattle/joinCaseBattle/{id}/{slot}"
    headers = {"authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers).json()
    if response["success"]:
        print(f"https://key-drop.com/case-battle/{id}")
    if response["errorCode"] == "userHasToWaitBeforeJoiningFreeBattle":
        print(response["message"])
        if not args.cookie:
            input("Press Enter to continue...")
        sys.exit()


def on_open(ws):
    print("Searching free battles...")
    ws.send("40/case-battle")


def on_message(ws, message):
    if "],1" in message:
        battle_id = (message.split(",")[2]).replace("[", "")
        battle_data = battle_status(battle_id)
        if battle_data["status"] != "ended":
            slots = [0, 1, 2, 3]
            occupied_slots = [user["slot"] for user in battle_data["users"]]
            free_slots = [slot for slot in slots if slot not in occupied_slots]
            join_battle(battle_id, free_slots[0])


def on_close(ws):
    print("Battle search error")


if __name__ == "__main__":
    description = "It automates the process of participating in daily battles."
    parser = argparse.ArgumentParser(description)
    parser.add_argument("-c", "--cookie", help="Generates a token")
    args = parser.parse_args()
    token = get_token(args.cookie)
    ws = websocket.WebSocketApp(
        "wss://kdrp3.com/socket.io/?EIO=4&transport=websocket",
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,
    )
    ws.run_forever()
