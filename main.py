import chess
import requests

board = chess.Board()

def play_move(player_move):
    try:
        move = board.parse_uci(player_move)
    except ValueError:
        print("Invalid move format, try again.")
        return

    if move not in board.legal_moves:
        print("Illegal move, try again.")
        return

    board.push(move)
    return get_board_image_url()


def get_board_image_url():
    fen = board.fen()
    url = f"https://www.chess.com/dynboard?fen={fen}&size=3"

    response = requests.get(url)
    if response.status_code == 200:
        return response.url
    else:
        print(f"Error getting board image URL: {response.status_code}")
        return None


while not board.is_game_over():
    player_move = input("move: ")
    image_url = play_move(player_move)
    if image_url:
        print(image_url)

print("Game over.")