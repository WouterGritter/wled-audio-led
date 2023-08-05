import socket

from wled.wled import WLED


class UDPWLED(WLED):
    def __init__(self, address, port=21324, timeout_delay=2):
        super().__init__()

        self.address = address
        self.port = port
        self.timeout_delay = timeout_delay

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def update(self, data: list[tuple[float, float, float]]) -> None:
        arr = [2, self.timeout_delay]
        for color in data:
            arr.append(int(color[0] * 255))
            arr.append(int(color[1] * 255))
            arr.append(int(color[2] * 255))

        self.socket.sendto(bytearray(arr), (self.address, self.port))
