# config.py __________________________________________________________________


"""Flask configuration variables."""

from os import environ
from dotenv import load_dotenv


load_dotenv()


class Config:
    """Set Flask configuration from .env file."""

    FLASK_APP =     environ.get('FLASK_APP')
    SECRET_KEY =    environ.get('SECRET_KEY')

    REPOSITORY =    environ.get('REPOSITORY')