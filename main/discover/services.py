# main/discover/services.py ___________________________________________________
# Author: Mathias Sackey, Sun Lee


import random

from main.home.services import get_random_tracks


def get_quiz(n=4):
    quiz = {
        'Which of the following best describes your current mood?'  : ['Happy', 'Sad', 'Angry', 'Anxious'],
        'How often do you listen to music?'                         : ['Less than an hour daily', 'At least an hour daily', '1-3 hours daily', 'More than 3 hours daily'],
        'Do you like musicals?'                                     : ['Do I breathe?', "I'd rather watch paint dry", "I'd go if I got paid 20 bucks", 'I go for the story'],
        'Do you like discovering new music?'                        : ['Sometimes', "I'd rather stick to what I know", "It's hard to find something new I like", 'Always!'],
        'How do you consume most of your music?'                    : ['Radio', 'Streaming App', 'Tiktok', "I don't"],
        'Do you enjoy live music?'                                  : ['Hell Yea!', 'No thanks', 'Why go out when you can stay in', 'Depends on the artist'],
        'What makes you like a song?'                               : ['The melody', 'The lyrics', 'The voice', 'The instrumentals'],
        'Do you enjoy dancing?'                                     : ['I Boogie all night long', "Can't move to rhythm", 'Slow dancing is the way to go', 'I only jump and wave my hands']
    }

    while len(quiz) > n:
        randq = random.choice(list(quiz.keys()))
        if randq != 'Which of the following best describes your current mood?':
            quiz.pop(randq)

    quiz = list(quiz.items())
    random.shuffle(quiz)

    return dict(quiz)


def get_mood(q):
    if 'Happy' in q:
        return 'Happy'
    if 'Sad' in q:
        return 'Sad'
    if 'Angry' in q:
        return 'Angry'
    if 'Anxious' in q:
        return 'Anxious'


def get_mooded_description(mood):
    moods = {
        'Happy'     : "It appears you're feeling very bubbly today!\
                    Our algorithm recommends you listen to this track to help to continue having an awesome day!",
        'Sad'       : "Sorry to hear you're feeling down today.\
                    This track will help you pick yourself back up!",
        'Angry'     : "Sorry to hear you're frustrated with your day today.\
                    This track will help lighten the mood and help you bounce back up.",
        'Anxious'   : "Sorry you're feeling stressed at the moment.\
                    This track certainly makes for a great pick to help you validat your feelings and improve your mood."
    }
    
    return moods[mood]


# TODO implement
def get_mooded_track(mood):
    return get_random_tracks(1)[0]