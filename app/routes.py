from flask import render_template

from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/create_order', methods=['POST', 'GET'])
def create_order():
    return render_template("create_order.html")
