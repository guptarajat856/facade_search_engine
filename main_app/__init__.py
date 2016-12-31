import os
from flask import Flask


app = Flask(__name__)

__import__('main_app.route')