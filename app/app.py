from flask import Flask, render_template, request, session
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
     UserMixin, RoleMixin

import gnews_translate as gt

# Create app
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_CONFIRMABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True

app.config.from_object('config.private')

# Setup mail extension
mail = Mail(app)

# Create database connection object
db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True)
  password = db.Column(db.String(255))
  active = db.Column(db.Boolean())
  confirmed_at = db.Column(db.DateTime())
  roles = db.relationship('Role', secondary=roles_users,
                          backref=db.backref('users', lazy='dynamic'))

  def __str__(self):
    return '<User id=%s email=%s>' % (self.id, self.email)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

db.create_all()

# Views
@app.route('/')
def home():
  my_lang = "en_us"

  result = dict()
  for r in gt.regions:
    result[r] = gt.get_news(r, my_lang)

  return render_template('index.html', news=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
