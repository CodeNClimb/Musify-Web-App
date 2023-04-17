# main/auth/services.py _______________________________________________________
# Author: Mathias Sackey, Sun Lee


from flask import redirect, session, url_for
from functools import wraps

from main.adapters.abstract_repository import repo as repo
from main.adapters.services import write_users
from main.models.msac_models import User


# ?
def authorise(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('bp_auth.sign_in'))
        
        return view(**kwargs)
    
    return wrapped_view


def authenticate(username, password):
    user = repo.get_user(username)
    if not user:
        raise ValidUsernameError
    if user.password != password:
        raise ValidPasswordError


def add_user(username, password):
    user = repo.get_user(username)
    if user:
        raise ValidUsernameError
    user = User(username, password)
    repo.add_user(user)
    write_users(repo)


# Valid Username Error ________________________________________________________

class ValidUsernameError(Exception):
    pass


# Valid Password Error ________________________________________________________

class ValidPasswordError(Exception):
    pass