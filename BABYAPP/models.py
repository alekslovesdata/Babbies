from flask_sqlalchemy import SQLAlchemy

#import database
DB = SQLAlchemy()

#define class for name 
class Name(DB.Model):
    __tablename__ = 'name'
    IDName = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
    Year = DB.Column(DB.Integer)
    Name = DB.Column(DB.String(30))
    Sex = DB.Column(DB.String(30))
    Percent = DB.Column(DB.Integer)
