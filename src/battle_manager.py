import sys
import requests


class BattleManager:
    BASE_URL = "https://kdrp2.com/CaseBattle"

    def __init__(self, token, cookie):
        self.token = token
        self.cookie = cookie

    def battle_status(self, id):
        response = requests.get(f"{self.BASE_URL}/gameFullData/{id}")
        return response.json()["data"]

    def join_battle(self, id, slot):
        url = f"{self.BASE_URL}/joinCaseBattle/{id}/{slot}"
        headers = {"authorization": f"Bearer {self.token}"}
        response = requests.post(url, headers=headers).json()
        if response["success"]:
            print(f"https://key-drop.com/case-battle/{id}")
        if response["errorCode"] == "userHasToWaitBeforeJoiningFreeBattle":
            print(response["message"])
            if not self.cookie:
                input("Press Enter to continue...")
            sys.exit()