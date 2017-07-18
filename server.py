import socket
import time

UDP_IP = "" 
UDP_PORT = 44663
CONNECTED_PLAYERS = {}
PLAYER_SCORE = {}
AVAILABLE_PLAYER_IDS = ["1","2"]
coinPoints = 5
counterMessagesRecv = 0
counterMessagesSent = 0
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
start = time.time()

def broadcast(data,addr):
      global counterMessagesSent
      for k, v in CONNECTED_PLAYERS.iteritems():
            if k != str(addr):
                sock.sendto(data,v)
                counterMessagesSent +=1
                print "Broadcasted  position/score to network"+str(v)

def reply(data,addr):
      global counterMessagesSent
      sock.sendto(data,addr)
      counterMessagesSent +=1
      print "Replied score to player"

while True:
    buf = bytearray(1024)
    nbytes, addr = sock.recvfrom_into(buf)
    try:
      data = buf.decode("utf-8")
      print "data rec",data
      command = data.split(",")
      counterMessagesRecv +=1
      if command[0] == 'request' :
          if len(AVAILABLE_PLAYER_IDS) > 0:
                temp = AVAILABLE_PLAYER_IDS.pop(0)
                temp = "1"
                sock.sendto("createplayer,"+temp,addr)
                CONNECTED_PLAYERS[str(addr)] = addr
                PLAYER_SCORE[str(addr)] = 0
                print len(CONNECTED_PLAYERS)
                if len(CONNECTED_PLAYERS) > 1:
                      sock.sendto(data,addr)
                      print "sent back--------------"
                print "Sent Create player to client"
                broadcast(data,addr)
      if command[0] == 'register' :
          print "Player registration request received from Address:",addr
          print "Player ",addr," registered with the Game Server"
          print "Player position : <",command[1],",",command[2],",",command[3],">"
          sock.sendto("Registered with server",addr)
          CONNECTED_PLAYERS[str(addr)] = addr
          print "Sent confirmation to client"
          broadcast(data,addr)
      if command[0] == 'position' :
          print "Player position : <",command[1],",",command[2],",",command[3],">"
          broadcast(data,addr)
      if command[0] == 'disconnectone':
          print "Player ",addr," disconnected"
          AVAILABLE_PLAYER_IDS.append("1")
          del CONNECTED_PLAYERS[str(addr)]
          del PLAYER_SCORE[str(addr)]
      if command[0] == 'disconnecttwo':
          print "Player ",addr," disconnected"
          AVAILABLE_PLAYER_IDS.append("2")
          del CONNECTED_PLAYERS[str(addr)]
          del PLAYER_SCORE[str(addr)]
      if command[0] == 'ScoreObject':
          print "Player request received"
          score = PLAYER_SCORE[str(addr)]
          PLAYER_SCORE[str(addr)] = score+coinPoints
          scorestr = "score,"+str(PLAYER_SCORE[str(addr)])
          reply(scorestr,addr)
      if command[0] == 'ReduceScore':
          print "Reduce Score request received"
          redscore = "reducescore,"+str(addr)
          broadcast(redscore,addr)
      print "Connected players list", CONNECTED_PLAYERS
      print "Connected players score", PLAYER_SCORE
      print "Available player", AVAILABLE_PLAYER_IDS
      print "Number of Messages Received by Server: ", counterMessagesRecv
      print "Number of Messages Sent by Server: ", counterMessagesSent
      print "Time taken: ", time.time() - start
    except Exception as e:
      print "",e

