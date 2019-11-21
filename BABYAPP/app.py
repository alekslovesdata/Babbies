from decouple import config
from flask import Flask, render_template, request
from .models import Name, DB


def create_app():
    app = Flask (__name__)

    #config to database
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baby_names_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

    #have the database know about the app:
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html', title = 'Home')

    #make reset route at end of lecture
    @app.route('/reset')
    def reset():
        return render_template('base.html', title = 'Reset')
        #DB.drop_all()
        #DB.create_all()
        #return render_template('base.html', title = 'Reset', users = [])

    @app.route('/generator',methods=['POST'])
    #@app.route('/user/',methods=['GET'])
    def generator(value1 = None, value2 = None, value3 = None, value4 = None,
    value5 = None, value6 = None):
        value1 = value1 or request.values['form1']
        value2 = request.values['form2']
        value3 = request.values['form3']
        value4 = request.values['form4']
        value5 = request.values['form5']
        value6 = request.values['form6']
        try:
            pass
        except Exception as e:
            message = "Error page: {}".format(e)
        return render_template('user2.html', title="NAMES", value1=value1,
        value2=value2,value3=value3,value4=value4, value5=value5, value6=value6)

    return app
