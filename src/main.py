import argparse
import websocket
from battle_manager import BattleManager
from get_token import get_token
from websocket_handler import BattleSearchWebSocket


def main():
    description = "It automates the process of participating in daily battles."
    parser = argparse.ArgumentParser(description)
    parser.add_argument("-c", "--cookie", help="Generates a token")
    args = parser.parse_args()

    token = get_token(args.cookie)
    battle_manager = BattleManager(token, args.cookie)
    websocket_handler = BattleSearchWebSocket(token, battle_manager)

    ws = websocket.WebSocketApp(
        "wss://kdrp3.com/socket.io/?EIO=4&transport=websocket",
        on_open=websocket_handler.on_open,
        on_message=websocket_handler.on_message,
        on_close=websocket_handler.on_close,
    )
    ws.run_forever()


if __name__ == "__main__":
    main()