import json

import pytest

from ..todo_crm import get_app


@pytest.fixture
def client(loop, test_client):
    return loop.run_until_complete(test_client(get_app))


@pytest.fixture
def user(client):
    data = {
        'firstname': 'test_first',
        'lastname': 'test_last'
    }

    return client.post('/', data=json.dumps(data))


async def test_empty_initial_list_of_users(client):
    resp = await client.get('/')
    assert resp.status == 200

    assert {} == await resp.json()


async def test_create_user(client):
    data = {
        'firstname': 'test_name',
        'lastname': 'test_lastname'
    }

    resp = await client.post('/', data=json.dumps(data))
    res = await resp.json()

    assert resp.status == 201
    assert res['lastname'] == data['lastname']
    assert res['firstname'] == data['firstname']
    assert res['todos'] == []

    
async def test_dont_create_invalid_user(client):
    data = {
        'firstname': 'test_name',
    }

    resp = await client.post('/', data=json.dumps(data))
    res = await resp.json()

    assert resp.status == 400
    assert 'no required field' in res


async def test_get_users(client, user):
    resp = await client.get('/')
    res = await resp.json()
    
    assert resp.status == 200
    assert len(res) == 1

