import os
import json
import pytest
from flask import current_app
from src.app import create_app

@pytest.fixture(scope="module")
def client():
    app = create_app()
    with app.test_client() as test_client:
        yield test_client

@pytest.fixture(scope="module")
def auth_token(client):
    params = {
        'username': os.getenv('APP_USERNAME'),
        'password': os.getenv('APP_PASSWORD')
    }
    response = client.post('/authorize', headers={'Content-Type': "application/json"}, data=json.dumps(params))
    data = response.json
    current_app.logger.info(data)
    assert data.get('auth_token')
    return data.get('auth_token')

def test_authorize(client):
    params = {
        'username': os.getenv('APP_USERNAME'),
        'password': os.getenv('APP_PASSWORD')
    }
    response = client.post('/authorize', headers={'Content-Type': "application/json"}, data=json.dumps(params))
    current_app.logger.info(params)
    data = response.json
    current_app.logger.info(data)
    assert data.get('auth_token')

def test_accounts_country(client, auth_token):
    params = {
        'country': "CA"
    }
    headers = {
        'Authorization': f"Bearer {auth_token}"
    }
    response = client.get('/accounts', query_string=params, headers=headers)
    data = response.json
    current_app.logger.debug(data)
    valid_results = True
    for account in data.get('results', []):
        if account.get('country') != params.get('country'):
            valid_results = False
            break
    assert valid_results and data.get('total_results')

def test_accounts_mfa(client, auth_token):
    params = {
        'mfa': "TOTP"
    }
    headers = {
        'Authorization': f"Bearer {auth_token}"
    }
    response = client.get('/accounts', query_string=params, headers=headers)
    data = response.json
    current_app.logger.debug(data)
    valid_results = True
    for account in data.get('results', []):
        if account.get('mfa') != params.get('mfa'):
            valid_results = False
            break
    assert valid_results and data.get('total_results')

def test_accounts_pagination(client, auth_token):
    params = {
        'mfa': "TOTP",
        'limit': 3,
        'sort': "amt",
        'sort_dir': -3
    }
    headers = {
        'Authorization': f"Bearer {auth_token}"
    }
    response = client.get('/accounts', query_string=params, headers=headers)
    data = response.json
    current_app.logger.debug(data)
    
    if not data.get('results'):
        raise AssertionError("request failed")

    prev_last_account = data.get('results', []).pop()

    params['next_cursor'] = data.get('next_cursor')
    response = client.get('/accounts', query_string=params, headers=headers)
    data = response.json
    current_app.logger.info(data)

    first_account = data.get('results', [])[0]

    assert data.get('total_results') and prev_last_account.get('_id') != first_account.get('_id') 
