import websocket
import sys
import requests
import webbrowser
import time


def on_open(ws):
    print("Searching free battles...")
    ws.send("40/case-battle")


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
        input("Press Enter to continue...")
        sys.exit()


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
    webbrowser.open("https://key-drop.com/token")
    time.sleep(1)
    token = input("Paste the token: ")
    ws = websocket.WebSocketApp(
        "wss://kdrp3.com/socket.io/?EIO=4&transport=websocket",
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,
    )
    ws.run_forever()
