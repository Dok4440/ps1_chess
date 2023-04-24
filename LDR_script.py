import time
import wiringpi
import sys
# import spidev

# functions

# ADC function
# def readadc(adcnum):
#     if ((adcnum > 7) or (adcnum < 0)):
#         return -1
#     revlen, recvData = wiringpi.wiringPiSPIDataRW(1, bytes([1,(8+adcnum)<<4,0]))
#     time.sleep(0.000005)
#     adcout = ((recvData[1]&3) << 8) + recvData[2]
#     return adcout

# defines the LDR's
wiringpi.wiringPiSetup()
LDR_E2 = wiringpi.pinMode(1,0)
LDR_E4 = wiringpi.pinMode(3,0)
LDR_G8 = wiringpi.pinMode(4,0)
LDR_F6 = wiringpi.pinMode(6,0)

# Loop that checks for input/light
try:
    while True:
        # Move of pawn
        if LDR_E2 == 1:
            print("pawn selected")
            time.sleep(1)

            if LDR_E4 == 1:
               print("moving pawn to E4")

            # aborts if nothing in selected in time
            else:
                print("no move selected in time, try again")
            
        # Move of knight
        elif LDR_G8 == 1:
            print("knight selected")
            time.sleep(1)

            if LDR_F6 == 1:
               print("moving knight to F6")

            # aborts if nothing in selected in time
            else:
                print("no move selected in time, try again")

        # No move
        else:
            print("no piece selected")
            time.sleep(1)

        time.sleep(1) 

except KeyboardInterrupt:
    print("Exit")
    sys.exit(0)

# als 1 en 0 niet werken --> ADC, waardes tussen 0 en 1023