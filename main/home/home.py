# main/home/home.py ___________________________________________________________
# Author: Sun Lee


from flask import Blueprint, render_template

from main.home.services import get_random_tracks


bp_home = Blueprint('bp_home', __name__)

@bp_home.route('/', methods=['GET'])
def home():
    return render_template('home.html',
                            tagged=get_random_tracks())