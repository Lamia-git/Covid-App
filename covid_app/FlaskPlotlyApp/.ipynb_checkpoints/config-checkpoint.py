"""Flask configuration variables."""
import os
from os import environ, path
from dotenv import load_dotenv
import sys

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

FlaskPlotly = os.path.dirname(basedir)
initializer = os.path.join(FlaskPlotly, "initializer")
sys.path.append(initializer)


class Config:
    """Set Flask configuration from .env file."""

    # General Config

    TESTING = True
    DEBUG = True
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    FLASK_APP = 'wsgi.py'
    SECRET_KEY = 'GDtfDCFYjD'

    # Database
    psw = environ.get('pg_psw')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{psw}@localhost:5433/covid'
