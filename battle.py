import argparse
import requests
import sys
import time
import webbrowser
import websocket


def get_token(cookie=None):
    url = "https://key-drop.com/pl/token"
    if cookie:
        headers = {
            "cookie": f"session_id={cookie}; __vioShield=49f7a4dd63e6f34db13d25b9be83c7e5",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        }
        return requests.get(url, headers=headers).text
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
