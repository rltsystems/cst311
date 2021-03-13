#Client
import time
from socket import *

serverName = 'mininet-vm'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1.0)

#message = input('Input lowercase sentense: ')
baseMessage = "Ping"
packetsLost = 0.0
maxRTT = 0
minRTT = 100

addition = 0.0 # used to be sum
avgRTT = 0.0
estRTT = 0.0
devRTT = 0.0
tOut = 0.0
estRTT_prev = 0.0
devRTT_prev = 0.0

first = True # used to be First
print()

for i in range(1,11):
    message = baseMessage + str(i)
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    print("Mesg sent:" + message)
    start = time.time()
    try:
        rsentence = clientSocket.recv(1024)
        end = time.time()
        print("Mesg rcvd: " + rsentence.decode())
        elapsed = round((end - start)*1000, 11)
        print("PONG " + str(i) + " RTT: " + str(elapsed) + "ms\n")
        if (i != 1):
            estRTT = (0.875 * estRTT_prev) + (0.125 * elapsed)
            devRTT = (0.75 * devRTT_prev) + (0.25 * abs(elapsed - estRTT))
            estRTT_prev = estRTT
            devRTT_prev = devRTT
        if (elapsed > maxRTT):
            maxRTT = elapsed
        if (elapsed < minRTT):
            minRTT = elapsed
        addition += elapsed

    except timeout:
        print("No Mesg rcvd ")
        print("PONG " + str(i) + " Request Timed out\n")
        packetsLost += 1.0
