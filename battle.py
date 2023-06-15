import websocket
import sys
import json
import requests
import re

def on_open(ws):
    print("Szukanie darmowych bitw")
    ws.send('40/case-battle,{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJsYW5nIjoiUEwiLCJjb3VudHJ5IjoiRU4iLCJzdWIiOiI2MjM2MjAxIiwiZXhwIjoxNjgzNjQ0MjM0fQ.hwJjpRrXQHFL8OzrcYfq_bS4Rg2xcuYHhg52Qe8uPBrs5GuOgTFOQGB0oYbJc7mTIj9fhfQBj6sOrg1yz-DTOodlcd5MtM6N5azz7RUm3CzA2r5SjwiUTc9jrjAFHDgEayAMPsaFAENe_KikoUXkXAf_YsVlAk5UyX1MWJ6jnJS8AIrHok7IfqtcXSDo-J8bafpe5rX1I7j6qvhCDM_tRn39cedDwWI9rhCkUahWwciSm4rtDUodqc-DVYES5NaUXJMcZ2NrF53-M80oQgLrXa5y9ivz-YdLEUi9rH8bT_YWDWX9E_EEalFK-AbyLt_XHT3KovkXwsQZP9MDy1Z8ww"}')

def battle_status(id):
    response = requests.get(f'https://kdrp2.com/CaseBattle/gameFullData/{id}')
    data = response.json()
    return data['data']

def join_battle(id, slot):
    url = f'https://kdrp2.com/CaseBattle/joinCaseBattle/{id}/{slot}'
    headers = {
        'accept': '*/*',
        'accept-language': 'pl-PL,pl;q=0.8',
        'authorization': f'Bearer {token}',
        'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'x-currency': 'usd'
    }
    response = requests.post(url, headers=headers)
    data = response.json() 
    if data['success']:
        print(f'https://key-drop.com/pl/case-battle/{id}')
    else:
        print(data['message'])
        sys.exit()

def on_message(ws, message):
    if not re.search(r'("BC_CREATE_V3"|\'BC_CREATE_V3\').*?("public",\s*true|\[true,\s*"public"\])', message):
        return
    battle = re.search(r'",\[(.*?),.,"', message).group(1)
    battle_data = battle_status(battle)
    if battle_data['status'] == 'ended':
        return
    slots = [0, 1, 2, 3]
    occupied_slots = [user['slot'] for user in battle_data['users']]
    free_slots = [slot for slot in slots if slot not in occupied_slots]
    join_battle(battle, free_slots[0])

def on_close(ws):
    print("Rozłączono z serwerem WebSocket")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1]
        ws = websocket.WebSocketApp("wss://kdrp3.com/socket.io/?connection=battle&EIO=4&transport=websocket",
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_close=on_close)
        ws.run_forever()
    else:
        print("Podaj token jako argument.")

