import chess
import chess.svg
import urllib.parse


from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1100, 1100)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 1080, 1080)

        self.chessboard = chess.Board()

        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

    def paintEvent(self, event):
        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

if __name__ == "__main__":
    app = QApplication([])
    board = MainWindow()
    board.show()
    app.exec()

#board = chess.Board()

def play_move(player_move):
    try:
        move = board.chessboard.parse_uci(player_move)
    except ValueError:
        print("Invalid move format, try again.")
        return

    if move not in board.chessboard.legal_moves:
        print("Illegal move, try again.")
        return

    board.chessboard.push(move)
    MainWindow.paintEvent(board, move)
    board.show()
    app.exec()
    return get_board_image_url()


def get_board_image_url():
    fen = board.chessboard.fen()
    encoded_fen = urllib.parse.quote(fen, safe='')
    base_url = "https://lichess.org/editor/"
    url = base_url + encoded_fen

    return url


while not board.chessboard.is_game_over():
    player_move = input("move: ")
    image_url = play_move(player_move)
    print(image_url)

print("Game over.")