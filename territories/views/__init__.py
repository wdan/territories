from flask import render_template
from territories import territories

@territories.route('/')
def index():
    return render_template('index.html')
