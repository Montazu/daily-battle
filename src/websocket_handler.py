class BattleSearchWebSocket:
    def __init__(self, token, battle_manager):
        self.token = token
        self.battle_manager = battle_manager

    def on_open(self, ws):
        print("Searching free battles...")
        ws.send("40/case-battle")

    def on_message(self, ws, message):
        if "],1" in message:
            battle_id = (message.split(",")[2]).replace("[", "")
            battle_data = self.battle_manager.battle_status(battle_id)
            if battle_data["status"] != "ended":
                slots = [0, 1, 2, 3]
                occupied_slots = [user["slot"] for user in battle_data["users"]]
                free_slots = [slot for slot in slots if slot not in occupied_slots]
                self.battle_manager.join_battle(battle_id, free_slots[0])

    def on_close(self, ws):
        print("Battle search error")