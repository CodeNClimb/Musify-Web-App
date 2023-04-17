# main/home/services.py _______________________________________________________
# Author: Sun Lee


import random

from main.adapters.abstract_repository import repo as repo


def get_random_tracks(n=5):
    return random.sample(repo.get_tracks(), n)