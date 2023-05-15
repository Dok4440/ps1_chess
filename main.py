import requests
from selenium import webdriver
import chess
import requests
import time
import wiringpi
import chess.svg


board = chess.Board()
browser = webdriver.Firefox()
browser.maximize_window()
browser.get("https://www.chess.com/dynboard?fen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR%20b%20KQkq%20-%200%201&size=3")
wiringpi.wiringPiSetup()
pin_CS_adc = 16
wiringpi.pinMode(pin_CS_adc, 1)
wiringpi.wiringPiSPISetupMode(1, 0, 500000, 0)
counter = 0


def readadc(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    revlen, recvData = wiringpi.wiringPiSPIDataRW(1, bytes([1,(8+adcnum)<<4,0]))
    time.sleep(0.000005)
    adcout = ((recvData[1]&3) << 8) + recvData[2]
    return adcout


def ActivateADC ():
    wiringpi.digitalWrite(pin_CS_adc, 0) # Actived ADC using CS
    time.sleep(0.000005)


def DeactivateADC():
    wiringpi.digitalWrite(pin_CS_adc, 1) # Deactived ADC using CS
    time.sleep(0.000005)


def play_move(p_move):
    try:
        move = board.parse_uci(p_move)
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
    while counter != 5:
        # move 1
        print("pawn selected")
        time.sleep(2)
        print("moving pawn to e4")
        
        player_move = "e2e4"
        image_url = play_move(player_move)
        if image_url:
            browser.get(image_url)

        counter += 1

        # move 2
        print("pawn selected")
        time.sleep(2)
        print("moving pawn to e5")

        player_move = "e7e5"
        image_url = play_move(player_move)
        if image_url:
            browser.get(image_url)

        counter += 1

        # move 3
        print("queen selected")
        time.sleep(2)
        print("moving queen to f3")

        player_move = "d1f3"
        image_url = play_move(player_move)
        if image_url:
            browser.get(image_url)

        counter += 1

        # move 4
        print("knight selected")
        time.sleep(2)
        print("moving knight to c6")

        player_move = "b8c6"
        image_url = play_move(player_move)
        if image_url:
            browser.get(image_url)

        counter += 1

        # move 5
        print("bishop selected")
        time.sleep(2)
        print("moving bishop to c4")

        player_move = "f1c4"
        image_url = play_move(player_move)
        if image_url:
            browser.get(image_url)
        counter += 1

    # move 6

    ActivateADC()
    LDR_D7 = readadc(0)
    DeactivateADC()

    if LDR_D7 < 70:
        player_first_move = "d7"
        print("pawn selected")
        time.sleep(5)

        ActivateADC()
        LDR_D6 = readadc(1)  # read from channel 1
        DeactivateADC()

        if LDR_D6 < 70:
            player_second_move = "d6"
            print("moving pawn to", player_second_move)

        # aborts if nothing in selected in time
        else:
            print("no move selected in time, try again")

        player_move = player_first_move + player_second_move
        image_url = play_move(player_move)
        if image_url:
            browser.get(image_url)

    # move 7

    ActivateADC()
    LDR_F3 = readadc(2)
    DeactivateADC()

    if LDR_F3 < 70:
        player_first_move = "f3"
        print("queen selected")
        time.sleep(5)

        ActivateADC()
        LDR_F7 = readadc(3)  # read from channel 1
        DeactivateADC()

        if LDR_F7 < 70:
            player_second_move = "f7"
            print("moving queen to", player_second_move)

        # aborts if nothing in selected in time
        else:
            print("no move selected in time, try again")

        player_move = player_first_move + player_second_move
        image_url = play_move(player_move)
        if image_url:
            browser.get(image_url)

print("Game over.")