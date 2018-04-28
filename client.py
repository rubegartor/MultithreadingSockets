import socket
import threading

class ThreadedClient(object):
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.buffer = 1024
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def connect(self):
    self.sock.connect((self.host, self.port))
    threading.Thread(target = self.readSocket).start()
    threading.Thread(target = self.send).start()

  def readSocket(self):
    while True:
      data = self.sock.recv(self.buffer).decode('utf-8')
      if data:
        print('[SERVER] {}'.format(data))

  def send(self):
    while True:
      msg = input()
      if msg != '':
        self.sock.send(msg.encode('utf-8'))

if __name__ == '__main__':
  ThreadedClient('127.0.0.1', 9999).connect()
