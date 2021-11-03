from flask import Flask, Blueprint, session , redirect, jsonify
from api import app, db
from user.models import User
from functools import wraps

uroute = Blueprint('uroute', __name__)

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return "add frontend step to redirect"
  return wrap

@uroute.route('/user/signup', methods=['POST'])
def signup():
  return User().signup()

@uroute.route('/user/signout')
def signout():
  return User().signout()

@uroute.route('/user/login', methods=['POST'])
def login():
  return User().login()

@uroute.route('/loginstatus')
def loginstatus():
    status = 1 if 'logged_in' in session else 0
    return jsonify({'logged_in': status})
