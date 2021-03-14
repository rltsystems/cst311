#Client
import time
from socket import *

serverName = 'mininet-vm'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1.0)

baseMessage = "Ping"
alpha = 0.125
beta = 0.25 # this value is typically 0.25
packetsLost = 0.0
maxRTT = 0
minRTT = 1000

totalTimeElapsed = 0.0
avgRTT = 0.0
estRTT = 0.0
devRTT = 0.0
estRTT_prev = 0.0
devRTT_prev = 0.0

firstSucMess = True
print()

# send message 10 times
for i in range(1,11):
    message = baseMessage + str(i)
    # send message
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    start = time.time() # time message was sent
    print("Mesg sent: " + message)
    
    try:
        rsentence = clientSocket.recv(1024) # receive message
        end = time.time() # time at which message arrived
        print("Mesg rcvd: " + rsentence.decode())
        elapsed = (end - start) * 1000
        print("PONG " + str(i) + " RTT: " + str(elapsed) + "ms\n")

        if (i == 1): # was if(firstSucMess):
            # uppon first successful rtt measured set the values max, min, est, dev
            maxRTT = elapsed
            minRTT = elapsed
            estRTT = elapsed
            devRTT = elapsed/2
            firstSucMess = False
        else:
            # calculate estimated RTT and deviation RTT
            estRTT = ((1-alpha) * estRTT_prev) + (alpha * elapsed)
            devRTT = ((1-beta) * devRTT_prev) + (beta * abs(elapsed - estRTT))
        # save values as previous for the next iteration
        estRTT_prev = estRTT
        devRTT_prev = devRTT

        if (elapsed > maxRTT):
            maxRTT = elapsed
        if (elapsed < minRTT):
            minRTT = elapsed
        totalTimeElapsed += elapsed

    except timeout:
        print("No Mesg rcvd ")
        print("PONG " + str(i) + " Request Timed out\n")
        packetsLost += 1
        estRTT = estRTT_prev
        devRTT = devRTT_prev

avgRTT = totalTimeElapsed / (10-packetsLost)
packetsLostPcent = (packetsLost/10) * 100
timeoutInter = estRTT + (4 * devRTT)

print("Min RTT:\t  " + str(minRTT) + " ms")
print("Max RTT:\t  " + str(maxRTT) + " ms")
print("Avg RTT:\t  " + str(avgRTT) + " ms")
print("Packet Loss:\t  " + str(packetsLostPcent)) #printed as percentage
print("Estimated RTT:\t  " + str(estRTT) + " ms")
print("Dev RTT:\t  " + str(devRTT) + " ms")
print("Timeout Intervals:" + str(timeoutInter) + " ms")
