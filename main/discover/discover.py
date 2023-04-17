# main/discover/discover.py ___________________________________________________
# Author: Mathias Sackey, Sun Lee


from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

from main.auth.services import authorise
from main.browse.services import *
from main.discover.services import *


# Discover ____________________________________________________________________

bp_discover = Blueprint('bp_discover', __name__, url_prefix='/discover')


# Discover: Home ______________________________________________________________

@bp_discover.route('/', methods=['GET'])
def discover():
    return render_template('discover/home.html')


# Discover: Question __________________________________________________________

# TODO polish
@authorise
@bp_discover.route('/question', methods=['GET'])
def question():
    form        = QuestionForm()
    quiz        = get_quiz()

    questions   = list(quiz.keys())
    answers     = list(quiz.values())

    form.q1.label   = questions[0]
    form.q1.choices = answers[0]

    form.q2.label   = questions[1]
    form.q2.choices = answers[1]

    form.q3.label   = questions[2]
    form.q3.choices = answers[2]

    form.q4.label   = questions[3]
    form.q4.choices = answers[3]

    return render_template('discover/question.html',
                            form=form)


# Discover: Answer ____________________________________________________________

@authorise
@bp_discover.route('/answer', methods=['GET', 'POST'])
def answer():
    if request.method == 'POST':
        form = request.form
        mood = get_mood(form['q1'] + form['q2'] + form['q3'] + form['q4'])
    
    return render_template('discover/answer.html',
                            description=get_mooded_description(mood),
                            track=get_mooded_track(mood))


# Question Form _______________________________________________________________

class QuestionForm(FlaskForm):
    q1      = RadioField(validators=[DataRequired()])
    q2      = RadioField(validators=[DataRequired()])
    q3      = RadioField(validators=[DataRequired()])
    q4      = RadioField(validators=[DataRequired()])
    submit  = SubmitField('Match!')