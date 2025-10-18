import socket
import struct
import time


ARTNET_PORT = 6454


class ArtNetDiscovery:
    def __init__(
        self,
        bind_ip: str = None,
        broadcast: str = None,
    ):
        self.bind_ip = bind_ip or "0.0.0.0"
        self.broadcast = broadcast or "<broadcast>"
        self.socket = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        try:
            self.socket.bind((self.bind_ip, ARTNET_PORT))
        except Exception as e:
            print(e)

    def stop(self):
        if self.socket:
            self.socket.close()

    def discover_devices(self, timeout: float = 1.5):
        artpoll = self._create_artpoll_packet()

        self.socket.sendto(artpoll, ("<broadcast>", ARTNET_PORT))

        devices = {}
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                self.socket.settimeout(0.1)
                data, addr = self.socket.recvfrom(1024)

                if self._is_artpoll_reply(data):
                    device = self._parse_artpoll_reply(data, addr)
                    if device:
                        if device["reported_ip"] not in devices:
                            devices[device["reported_ip"]] = device

            except socket.timeout:
                continue
            except Exception as e:
                print(e)

        device_list = list(devices.values())
        return device_list

    def _create_artpoll_packet(self):
        packet = b"Art-Net\x00"  # ID
        packet += struct.pack("<H", 0x2000)  # OpCode (ArtPoll)
        packet += struct.pack("<H", 0x0000)  # Protocol version
        packet += b"\x00"  # TalkToMe
        packet += b"\x00"  # Priority
        return packet

    def _is_artpoll_reply(self, data: bytes):
        return (
            len(data) >= 10
            and data.startswith(b"Art-Net\x00")
            and struct.unpack("<H", data[8:10])[0] == 0x2100
        )

    def _parse_artpoll_reply(self, data: bytes, addr: tuple):
        """Parse ArtPollReply packet."""
        try:
            ip_bytes = data[10:14]
            reported_ip = f"{ip_bytes[0]}.{ip_bytes[1]}.{ip_bytes[2]}.{ip_bytes[3]}"
            short_name = data[26:43].decode("ascii", errors="ignore").strip("\x00")
            long_name = data[44:171].decode("ascii", errors="ignore").strip("\x00")

            return {
                "reported_ip": reported_ip,
                "source_ip": addr[0],
                "short_name": short_name,
                "long_name": long_name,
            }
        except Exception as e:
            print(f"Error parsing ArtPollReply: {e}")
            return None


def main():
    configurator = ArtNetDiscovery()
    configurator.start()
    devices = configurator.discover_devices(2)


if __name__ == "__main__":
    main()
