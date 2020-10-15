from flask import render_template, request, redirect

from app import app

from app.models import Application, Route, Car


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/create_order', methods=['POST', 'GET'])
def create_order():
    return render_template("create_order.html")
