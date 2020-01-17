from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route('/<zip>')
def getResults(zip):
    print(zip)
    return render_template('results.html')