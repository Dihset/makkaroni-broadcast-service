import asyncio
import os
import logging
import aiohttp.web


async def message_getter(request):
    data = await request.data()
    await request.app['queue'].put(data)
    return aiohttp.web.Response(text='Test handle')


async def websocket_handler(request):
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    while True:
        data = await request.app['queue'].get()
        logging.info(data)
        await ws.send_str(data)
    return ws


async def init_app():
    logging.basicConfig()
    app = aiohttp.web.Application()
    app['queue'] = asyncio.Queue()
    app.router.add_route('POST', '/api/messages', message_getter)
    app.router.add_route('GET', '/api/messages/broadcast/ws', websocket_handler)
    return app
