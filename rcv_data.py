#!/usr/bin/env python
# encoding: utf-8

import os

import asyncio
# ATTENTION: must use asyncio supported lib
from aioredis import create_connection, Channel
import websockets

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_URL = 'redis://{}:{}/{}'.format(REDIS_HOST, REDIS_PORT, REDIS_DB)
PUB_CHANNEL_NAME = 'data_pipeline_demo'
WS_HOST = '0.0.0.0'
WS_PORT = 8686

async def subscribe_to_redis(redis_url, channel_name):
    """async redis channel subscribe
    """
    r = await create_connection(redis_url)
    channel = Channel(channel_name, is_pattern=False)
    await r.execute_pubsub('subscribe', channel)
    return channel, r

async def ws_handler(websocket, path):
    channel, conn = await subscribe_to_redis(REDIS_URL, PUB_CHANNEL_NAME)

    try:
        while 1:
            # async receive massage from redis channel
            msg = await channel.get()
            print('data received from redis channel {}: {}'.format(PUB_CHANNEL_NAME, msg))
            # publish data in websocket
            await websocket.send(msg.decode('utf-8'))
    except websockets.exceptions.ConnectionClosed:
        # Free up channel if websocket goes down
        await conn.execute_pubsub('unsubscribe', channel)
        conn.close()


if __name__ == '__main__':
    # asyncio loop for concurrency
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    ws_server = websockets.serve(ws_handler, WS_HOST, WS_PORT)
    loop.run_until_complete(ws_server)
    print('websocket server running on {}:{}'.format(WS_HOST, WS_PORT))
    loop.run_forever()
