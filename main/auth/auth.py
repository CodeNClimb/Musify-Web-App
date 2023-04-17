# main/auth/auth.py ___________________________________________________________
# Author: Mathias Sackey, Sun Lee


from flask import Blueprint, redirect, render_template, session, url_for
from flask_wtf import FlaskForm
from password_validator import PasswordValidator
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from main.auth.services import *


# Authentication ______________________________________________________________

bp_auth = Blueprint('bp_auth', __name__)


# Authentication: Sign Up _____________________________________________________

@bp_auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    form = SignUpForm()

    if form.validate_on_submit():

        # success
        try:
            add_user(form.username.data, form.password.data)
            return redirect(url_for('bp_auth.sign_in'))
        
        # fail
        except ValidUsernameError:
            form.username.errors.append('Username is taken.')
    
    return render_template('auth/auth.html',
                            form = form,
                            handler_url = url_for('bp_auth.sign_up'))


# Authentication: Sign In _____________________________________________________

@bp_auth.route('/sign-in', methods=['GET','POST'])
def sign_in():
    form = SignInForm()

    if form.validate_on_submit():

        # success
        try:
            authenticate(form.username.data, form.password.data)
            session.clear()
            session['username'] = form.username.data
            return redirect(url_for('bp_home.home'))
        
        # fail
        except ValidUsernameError:
            form.username.errors.append('Invalid username.')
        
        # fail
        except ValidPasswordError:
            form.password.errors.append('Invalid password.')

    return render_template('auth/auth.html',
                            form = form,
                            handler_url = url_for('bp_auth.sign_in'))


# Authentication: Sign Out ____________________________________________________

@bp_auth.route('/sign-out')
def sign_out():
    session.clear()
    return redirect(url_for('bp_home.home'))


# Validate Password ___________________________________________________________

class ValidatePassword:
    def __call__(self, form, field):
        schema = PasswordValidator()
        schema.has().uppercase()\
              .has().lowercase()\
              .has().digits()
        if not schema.validate(field.data):
            raise ValidationError('Password requires an uppercase, \
                                                     a lowercase, and \
                                                     a digit.')


# Sign Up Form ________________________________________________________________

class SignUpForm(FlaskForm):
    username    = StringField('Username', [Length(min=3)])
    password    = PasswordField('Password', [Length(min=8), ValidatePassword()])
    submit      = SubmitField('Sign Up')


# Sign In Form ________________________________________________________________

class SignInForm(FlaskForm):
    username    = StringField('Username', [DataRequired()])
    password    = PasswordField('Password', [DataRequired()])
    submit      = SubmitField('Sign In')
