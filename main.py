from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'

# 連接postgresql db
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://<USER>:<PASSWORD>@<DBIP>:<DBPORT>/<DBNAME>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


