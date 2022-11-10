from backend import app

from flask import render_template, redirect, session

@app.route('/')
def index():
    return render_template('loading.html')
