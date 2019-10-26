import asyncio

class Storage:
    """Класс для хранения метрик в памяти процесса"""

    def __init__(self):
        self._data = {}

    def put(self, key, value, timestamp):
        if key not in self._data:
            self._data[key] = {}

        self._data[key][timestamp] = value

    def get(self, key):
        data = self._data

        if key != "*":
            data = {
                key: data.get(key, {})
            }

        result = {}
        for key, timestamp_data in data.items():
            result[key] = sorted(timestamp_data.items())

        return result


class ParseError(ValueError):
    pass


class Parser:
    """Класс для реализации протокола"""

    def encode(self, responses):
        """Преобразование ответа сервера в строку для передачи в сокет"""
        rows = []
        for response in responses:
            if not response:
                continue
            for key, values in response.items():
                for timestamp, value in values:
                    rows.append('{} {} {}'.format(key, value, timestamp))

        result = "ok\n"

        if rows:
            result += "\n".join(rows) + "\n"

        return result + "\n"

    def decode(self, data):
        """Разбор команды для дальнейшего выполнения. Возвращает список команд для выполнения"""
        parts = data.split("\n")
        commands = []
        for part in parts:
            if not part:
                continue

            try:
                method, params = part.strip().split(" ", 1)
                if method == "put":
                    key, value, timestamp = params.split()
                    commands.append(
                        (method, key, float(value), int(timestamp))
                    )
                elif method == "get":
                    key = params
                    commands.append(
                        (method, key)
                    )
                else:
                    raise ValueError("unknown method")
            except ValueError:
                raise ParseError("wrong command")

        return commands


class ExecutorError(Exception):
    pass


class Executor:
    """Класс Executor реализует метод run, который знает как выполнять команды сервера"""

    def __init__(self, storage):
        self.storage = storage

    def run(self, method, *params):
        if method == "put":
            return self.storage.put(*params)
        elif method == "get":
            return self.storage.get(*params)
        else:
            raise ExecutorError("Unsupported method")


class EchoServerClientProtocol(asyncio.Protocol):
    """Класс для реализции сервера при помощи asyncio"""

    storage = Storage()

    def __init__(self):
        super().__init__()

        self.parser = Parser()
        self.executor = Executor(self.storage)
        self._buffer = b''

    def process_data(self, data):
        """Обработка входной команды сервера"""

        # разбираем сообщения при помощи self.parser
        commands = self.parser.decode(data)

        # выполняем команды и запоминаем результаты выполнения
        responses = []
        for command in commands:
            resp = self.executor.run(*command)
            responses.append(resp)

        # преобразовываем команды в строку
        return self.parser.encode(responses)

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        """Метод data_received вызывается при получении данных в сокете"""
        self._buffer += data
        try:
            decoded_data = self._buffer.decode()
        except UnicodeDecodeError:
            return

        # ждем данных, если команда не завершена символом \n
        if not decoded_data.endswith('\n'):
            return

        self._buffer = b''

        try:
            # обрабатываем поступивший запрос
            resp = self.process_data(decoded_data)
        except (ParseError, ExecutorError) as err:
            # формируем ошибку, в случае ожидаемых исключений
            self.transport.write("error\n{}\n\n".format(err).encode())
            return

        # формируем успешный ответ
        self.transport.write(resp.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        EchoServerClientProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    # запуск сервера для тестирования
    pass