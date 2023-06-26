import websocket
import sys
import json
import requests
import re
import webbrowser
import time

def on_open(ws):
	print('Searching free battles...')
	ws.send('40/case-battle')

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
	if data['errorCode'] == 'userHasToWaitBeforeJoiningFreeBattle':
		print(data['message'])
		input('Press Enter to continue...')
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
	print('Battle search error')

if __name__ == '__main__':
	webbrowser.open('https://key-drop.com/pl/token?t=1686828540445')
	time.sleep(1)
	question = 'Paste the token: '
	token = input(question)
	ws = websocket.WebSocketApp('wss://kdrp3.com/socket.io/?connection=battle&EIO=4&transport=websocket',
		on_open=on_open,
		on_message=on_message,
		on_close=on_close)
	ws.run_forever()
