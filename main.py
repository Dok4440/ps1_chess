import chess
import urllib.parse

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
    encoded_fen = urllib.parse.quote(fen, safe='')
    base_url = "https://lichess.org/editor/"
    url = base_url + encoded_fen

    return url


while not board.is_game_over():
    player_move = input("move: ")
    image_url = play_move(player_move)
    print(image_url)

print("Game over.")