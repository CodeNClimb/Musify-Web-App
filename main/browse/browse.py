# main/browse/browse.py _______________________________________________________
# Author: Sun Lee, Mathias Sackey


from better_profanity import profanity
from datetime import datetime
from flask import Blueprint, render_template, session
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, TextAreaField 
from wtforms.validators import DataRequired, Length, ValidationError

from main.browse.services import *


# Browse ______________________________________________________________________

bp_browse = Blueprint('bp_browse', __name__ )

@bp_browse.route('/<tag>/<i>', methods=['GET'])
def browse(tag, i):
    return render_template('browse/browse.html',
                            an=get_alphanumeric(tag,i), # alphanumeric navigation
                            tag=get_tag(tag,i),         # name
                            tagged=get_tagged(tag,i))   # albums/artists/genres/tracks


# Track _______________________________________________________________________

bp_track = Blueprint('bp_track', __name__)

@bp_track.route('/track/<i>', methods=['GET', 'POST'])
def track(i):
    i = int(i)
    form = ReviewForm()

    if form.validate_on_submit():
        
        # success
        try:
            add_review(i, session['username'], datetime.now(), form.rating.data, form.review.data)
        
        # fail
        # TODO redirect to SIGN IN?
        except KeyError:
            form.submit.errors.append('SIGN UP or SIGN IN to review this track.')
    
    return render_template('browse/track.html',
                            track=get_track(i),
                            form=form)


# Profanity Free Validator ____________________________________________________

class ProfanityFree():
    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError('Field must not contain profanity')


# Review Form _________________________________________________________________

class ReviewForm(FlaskForm):
    rating = RadioField('Rating', choices=['☆☆☆☆☆','★☆☆☆☆','★★☆☆☆','★★★☆☆','★★★★☆','★★★★★'], validators=[DataRequired()])
    review = TextAreaField('Review', validators=[ProfanityFree()])
    submit = SubmitField('Submit')