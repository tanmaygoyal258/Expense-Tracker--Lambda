from flask import render_template, redirect
from app import app

@app.route('/')
@app.route('/home')
def home():
    return render_template(home.html)