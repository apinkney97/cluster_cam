#!/usr/bin/python3

import asyncio
from typing import Optional

try:
    import scrollphat

    HAS_SCROLLPHAT = True
except (ImportError, OSError):
    HAS_SCROLLPHAT = False

try:
    from RPi import GPIO

    HAS_GPIO = True
except (ImportError, OSError):
    HAS_GPIO = False

from aiohttp import web


SPEED: float = 20
QUEUE: Optional[asyncio.Queue] = None

routes = web.RouteTableDef()


async def poll_queue() -> None:
    if not HAS_SCROLLPHAT:
        return

    while True:
        text = await QUEUE.get()
        scrollphat.clear()
        scrollphat.write_string(text, 11)
        for _ in range(scrollphat.buffer_len()):
            scrollphat.scroll()
            await asyncio.sleep(1 / SPEED)


@routes.post("/message")
async def handle(request: web.Request) -> web.Response:
    if not HAS_SCROLLPHAT:
        raise web.HTTPNotImplemented(text="No scrollphat :(")

    data = await request.text()
    await QUEUE.put(data)
    return web.Response(text="OK")


@routes.post("/brightness")
async def handle(request: web.Request) -> web.Response:
    if not HAS_SCROLLPHAT:
        raise web.HTTPNotImplemented(text="No scrollphat :(")

    brightness = await request.json()
    scrollphat.set_brightness(brightness)

    return web.Response(text="OK")


@routes.post("/lights")
async def handle(request: web.Request) -> web.Response:
    if not HAS_GPIO:
        raise web.HTTPNotImplemented(text="No gpio :(")

    lights_on = await request.json()
    GPIO.output(17, bool(lights_on))

    return web.Response(text="OK")


@routes.get("/health")
async def handle(request: web.Request) -> web.Response:
    return web.Response(text="OK")


async def main() -> None:
    global QUEUE
    QUEUE = asyncio.Queue()

    if HAS_GPIO:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, 0)

    app = web.Application()
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner)
    await site.start()

    await asyncio.gather(asyncio.Event().wait(), poll_queue())


if __name__ == "__main__":
    asyncio.run(main())
