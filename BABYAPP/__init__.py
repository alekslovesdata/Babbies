"""Entry point for baby name app"""

from .app import create_app

APP = create_app()

#run this in terminal with FLASK_APP=BABYAPP:APP flask run
