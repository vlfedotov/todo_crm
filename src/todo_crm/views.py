import logging

from aiohttp import web
from aiohttp.web_exceptions import HTTPMethodNotAllowed

from .settings import TODO_HOST

from .models import User

logger = logging.getLogger(__name__)


class View(object):
    def __init__(self, request):
        self.request = request

    @classmethod
    async def dispatch(cls, request):
        view = cls(request)
        method = getattr(view, request.method.lower())
        if not method:
            return HTTPMethodNotAllowed()

        return await method()


class UserListCreateView(View):
    async def get(self):
        users = User.all_users()
        return web.json_response(users)

    async def post(self):
        content = await self.request.json()
        try:
            user = User.create_user(content)
        except ValueError as e:
            return web.json_response(str(e), status=400)
        return web.json_response(user, status=201)

    
class UserRetrieveView(View):
    def __init__(self, request):
        super().__init__(request)
        self.id = request.match_info.get('id')
    
    async def get(self):
        try:
            user = User.get_user(self.id)
        except ValueError as e:
            return web.json_response(str(e), status=400)
        return web.json_response(user)


class TodoListCreateView(UserRetrieveView):
    async def get(self):
        user = User.get_user(self.id)
        todos = user['todos']
        return web.json_response(todos)

    async def post(self):
        content = await self.request.json()
        try:
            todo = User.create_todo(self.id, content)
        except ValueError as e:
            return web.json_response(str(e), status=400)
        
        return web.json_response(todo)
