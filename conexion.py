import socket
class Conexion:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def conectar(self):
        self.socket.connect((self.host, self.port))

    def recibir_datos(self):
        data = self.socket.recv(1024)
        return data