#!/usr/bin/python3

import socket
import time

import scrollphat


def show_text(text: str, speed: float = 20):
    scrollphat.write_string(text, 11)
    for _ in range(scrollphat.buffer_len()):
        scrollphat.scroll()
        time.sleep(1 / speed)
    scrollphat.clear()


def listen(port: int = 8888):
    buf = b""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", port))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                buf += data

    show_text(buf.decode())


def main():
    # show_text("Hello, this is a message that's fairly long")
    while True:
        listen()


if __name__ == "__main__":
    main()
