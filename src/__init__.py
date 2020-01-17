from flask import Flask, render_template
import os
from .priceFinder import getCostcoLocations

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route('/<zip>')
def getResults(zip):
    locations = getCostcoLocations(zip)
    return render_template('results.html', locations=locations)