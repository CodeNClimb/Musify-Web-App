# main/services.py  __________________________________________________________
# Author: Sun Lee


# Validators _________________________________________________________________

def validate_integer(integer):
    try:
        if int(integer) < 0:
            raise ValueError
        return int(integer)
    except:
        raise ValueError(f'Invalid int: {integer}')

def validate_string(string):
    try:
        if string.strip() == '':
            raise ValueError
        return string.strip()
    except:
        return None
