import socket
import threading

CLIENTS = []

class ThreadedServer(object):
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.buffer = 1024
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind((self.host, self.port))

  def listen(self):
    self.sock.listen(5)
    while True:
      client, address = self.sock.accept()
      client.settimeout(60)
      CLIENTS.append(client)
      threading.Thread(target = self.receiveData, args = (client,address)).start()

  def receiveData(self, client, address):
    while True:
      try:
        data = client.recv(self.buffer)
        if data:
          data = data.decode('utf-8')
          print('[{}] {}'.format(address, data))
          self.sendToAll(data)
        else:
          raise error('Client disconnected')
      except:
        client.close()

  def sendToAll(self, data):
    for clt in CLIENTS:
      try:
        clt.send(data.encode('utf-8'))
      except IOError as e:
        continue

if __name__ == "__main__":
  ThreadedServer('127.0.0.1', 9999).listen()
