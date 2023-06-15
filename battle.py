import websocket
import sys
import json
import requests
import re
import webbrowser
import time

def on_open(ws):
	print("Searching free battles...")
	message = '40/case-battle,{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJsYW5nIjoiUEwiLCJjb3VudHJ5IjoiRU4iLCJzdWIiOiI2MjM2MjAxIiwiZXhwIjoxNjgzNjQ0MjM0fQ.hwJjpRrXQHFL8OzrcYfq_bS4Rg2xcuYHhg52Qe8uPBrs5GuOgTFOQGB0oYbJc7mTIj9fhfQBj6sOrg1yz-DTOodlcd5MtM6N5azz7RUm3CzA2r5SjwiUTc9jrjAFHDgEayAMPsaFAENe_KikoUXkXAf_YsVlAk5UyX1MWJ6jnJS8AIrHok7IfqtcXSDo-J8bafpe5rX1I7j6qvhCDM_tRn39cedDwWI9rhCkUahWwciSm4rtDUodqc-DVYES5NaUXJMcZ2NrF53-M80oQgLrXa5y9ivz-YdLEUi9rH8bT_YWDWX9E_EEalFK-AbyLt_XHT3KovkXwsQZP9MDy1Z8ww"}'
	ws.send(message)

def battle_status(id):
	response = requests.get(f'https://kdrp2.com/CaseBattle/gameFullData/{id}')
	return response.json()['data']

def join_battle(id, slot):
	url = f'https://kdrp2.com/CaseBattle/joinCaseBattle/{id}/{slot}'
	headers = { 'authorization': f'Bearer {token}' }
	response = requests.post(url, headers=headers)
	data = response.json()
	if data['success']:
		print(f'https://key-drop.com/pl/case-battle/{id}')
	else:
		print(data['message'])
		sys.exit()

def on_message(ws, message):
	regex_free_battle = r'("BC_CREATE_V3"|\'BC_CREATE_V3\').*?("public",\s*true|\[true,\s*"public"\])'
	if not re.search(regex_free_battle, message): return
	battle_id = re.search(r'",\[(.*?),.,"', message).group(1)
	battle_data = battle_status(battle_id)
	if battle_data['status'] == 'ended': return
	slots = [0, 1, 2, 3]
	occupied_slots = [user['slot'] for user in battle_data['users']]
	free_slots = [slot for slot in slots if slot not in occupied_slots]
	join_battle(battle_id, free_slots[0])

def on_close(ws):
	print("Battle search error")

if __name__ == "__main__":
	webbrowser.open("https://key-drop.com/pl/token?t=1686828540445")
	time.sleep(1)
	question = "Paste the token: "
	token = input(question)
	ws = websocket.WebSocketApp("wss://kdrp3.com/socket.io/?connection=battle&EIO=4&transport=websocket",
								on_open=on_open,
								on_message=on_message,
								on_close=on_close)
	ws.run_forever()