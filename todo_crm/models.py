import json
import logging

import requests

from .settings import TODO_HOST


logger = logging.getLogger(__name__)


class User(object):
    required_fields = ('firstname', 'lastname')
    users = {}
    user_id_inc = 0

    @staticmethod
    def validate_content(required_fields, content):
        errors = []
        for f in required_fields:
            if f not in content:
                errors.append(f)
        return errors
    
    @classmethod
    def create_user(cls, content):
        validation_errors = cls.validate_content(cls.required_fields, content)
        if validation_errors:
            raise ValueError('no required fields: {}'.format(validation_errors))
            
        cls.user_id_inc += 1
        content.update({'todos': []})
        cls.users.update({cls.user_id_inc: content})
        return content

    @classmethod
    def get_user(cls, user_id):
        try:
            user = cls.users[int(user_id)]
        except KeyError:
            raise ValueError('no user with id: {}'.format(user_id))
        return user
    
    @classmethod
    def create_todo(cls, user_id, content):
        required_todo_fields = ('todo', )
        user_id = int(user_id)
        if user_id not in cls.users:
            raise ValueError('no user with id: {}'.format(user_id))

        validation_errors = cls.validate_content(required_todo_fields, content)
        if validation_errors:
            raise ValueError('no required fields: {}'.format(validation_errors))

        content.update({'user': user_id})
        todo = requests.post(TODO_HOST, json.dumps(content)).json()
        cls.users[user_id]['todos'].append(todo)
        user = cls.get_user(user_id)
        return user
        
    @classmethod
    def all_users(cls):
        return cls.users
