#!/usr/bin/python3

import asyncio

import scrollphat


class MessageListener:
    def __init__(self, port: int, speed: float = 20) -> None:

        self.period = 1 / speed
        self.port = port

        self.queue = asyncio.Queue()

    async def poll_queue(self) -> None:
        while True:
            text = await self.queue.get()
            scrollphat.clear()
            scrollphat.write_string(text, 11)
            for _ in range(scrollphat.buffer_len()):
                scrollphat.scroll()
                await asyncio.sleep(self.period)

    async def handle_message(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        message = (await reader.readline()).decode()
        await self.queue.put(message)
        writer.write(b"OK\n")
        await writer.drain()
        writer.close()

    async def run(self) -> None:

        server = await asyncio.start_server(self.handle_message, "", self.port)
        async with server:
            await asyncio.gather(server.serve_forever(), self.poll_queue())


async def main():
    listener = MessageListener(port=8888)
    await listener.run()


if __name__ == "__main__":
    asyncio.run(main())
