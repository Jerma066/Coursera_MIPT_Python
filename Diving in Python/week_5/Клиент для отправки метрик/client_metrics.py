import socket
import time


class ClientError(Exception):
    """Общий класс исключений клиента"""
    pass


class Client:
    def __init__(self, host, port, timeout = None):
        self.host = host
        self.port = port
        self.timeout = timeout

        try:
            sock = socket.socket()
            self.connection = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientError("connection error", err)

    @staticmethod
    def obtain_data(server_answer):
        data = {}
        if server_answer == "":
            return data

        for row in server_answer.split("\n"):
            key, value, timestamp = row.split()
            if key not in data:
                data[key] = []
            data[key].append((int(timestamp), float(value)))

        return data

    def _read(self):
        data = b""
        while not data.endswith(b"\n\n"):
            try:
                data += self.connection.recv(1024)
            except socket.error as err:
                raise ClientError("receiving error", err)

        decoded_data = data.decode()
        # Прекратить разбиение, как только встретим "\n" первый раз
        _, payload = decoded_data.split("\n", 1)
        server_answer = payload.strip()

        return server_answer

    def put(self, key, value, timestamp=None):
        ts = timestamp or int(time.time())

        try:
            self.connection.sendall(f"put {key} {value} {ts}\n".encode())
        except socket.error as err:
            raise ClientError("error sending data", err)

        self._read()

    def get(self, key):
        try:
            self.connection.sendall(f"get {key}\n".encode())
        except socket.error as err:
            raise ClientError("error sending data", err)

        server_answer = self._read()
        data = self.obtain_data(server_answer)
        return data

    def close(self):
        try:
            self.connection.close()
        except socket.error as err:
            raise ClientError("error socket closing error", err)
