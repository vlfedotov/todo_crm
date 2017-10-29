import asyncio
import logging

from aiohttp import web

from .views import *


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_app(loop):
    app = web.Application(loop=loop)
    app.router.add_route('*', '/', UserListCreateView.dispatch)
    app.router.add_route('*', '/{id}', UserRetrieveView.dispatch)
    app.router.add_route('*', '/{id}/todos', TodoListCreateView.dispatch)
    return app


async def init(loop, port):
    app = get_app(loop)
    server = await loop.create_server(app.make_handler(), '127.0.0.1', port)
    logger.info('Server started on 127.0.0.1:{}'.format(port))
    return server
