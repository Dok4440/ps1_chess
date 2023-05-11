import chess
import requests
import time
import wiringpi
import sys

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

wiringpi.wiringPiSetup()
pin_CS_adc = 16 #We will use w16 as CE, not the default pin w15!
wiringpi.pinMode(pin_CS_adc, 1) # Set ce to mode 1 ( OUTPUT )
wiringpi.wiringPiSPISetupMode(1, 0, 500000, 0) #(channel, port, speed, mode)

while not board.is_game_over():

    ActivateADC()
    LDR_E2 = readadc(0)  # read from channel 0
    DeactivateADC()
    print(LDR_E2)

    if LDR_E2 < 70:
        player_first_move = "e2"
        print("pawn selected")
        time.sleep(5)

        ActivateADC()
        LDR_E4 = readadc(1)  # read from channel 1
        DeactivateADC()
        print(LDR_E4)

        if LDR_E4 < 70:
            player_second_move = "e4"
            print("moving pawn to", player_second_move)

        # aborts if nothing in selected in time
        else:
            print("no move selected in time, try again")

    player_move = player_first_move +  player_second_move
    image_url = play_move(player_move)
    if image_url:
        print(image_url)


print("Game over.")