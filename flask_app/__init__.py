from flask import Flask, render_template, redirect, request, session
from flask_bcrypt import Bcrypt
import re

app: 'Flask' = Flask(__name__)
app.secret_key = 'a40f0fc4-64ef-4a22-9509-5bfb7db7cc51'

bcrypt = Bcrypt(app)

DATABASE = 'recipe_network_db'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATE_REGEX = re.compile('^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$')