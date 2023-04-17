# Author: Mathias Sackey, Sun Lee

import pytest
from flask import session

import main.auth.services as auth_services
from main.adapters.abstract_repository import *
from main.models.else_models import *
from main.models.msac_models import *
from main.models.model import *


def test_sign_up(client):
    # Check that we retrieve the register page.
    response_code = client.get('/sign-up').status_code
    assert response_code == 200

    # Check that we can register a user successfully,
    # supplying a valid user name and password.
    response = client.post(
        '/sign-up',
        data = {'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.status_code == 200

def test_sign_can_add_user(in_repo):
    username = 'jz'
    password = 'abc123A1'
    auth_services.repo = in_repo
    auth_services.add_user(username, password)
    user = in_repo.get_user(username)
    assert username == user.username

def test_cannot_add_user_with_existing_name(in_repo):
    user_name = 'mathias'
    password = 'abcd1A23'
    auth_services.repo = in_repo

    with pytest.raises(auth_services.ValidUsernameError):
        auth_services.add_user(user_name, password)

def test_can_authenticate_valid_user(in_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'
    auth_services.repo = in_repo

    try:
        auth_services.authenticate(new_user_name, new_password)
    except auth_services.ValidUsernameError:
        assert False

def test_authentication_with_invalid_credentials(in_repo):
    auth_services.repo = in_repo
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    with pytest.raises(auth_services.ValidPasswordError):
        auth_services.authenticate(new_user_name, '0987654321')
