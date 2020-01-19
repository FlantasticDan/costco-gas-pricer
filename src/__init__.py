from flask import Flask, render_template, request
import flask_cors
import os
from .priceFinder import getCostcoAJAXurl, interpretCostcoAJAX

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route('/<zip>')
@flask_cors.cross_origin()
def generateURL(zip):
    url = getCostcoAJAXurl(zip)
    print(url)
    return render_template('scrape.html', ajax=url)

@app.route('/render/', methods=['POST'])
def renderResults():
    locations = interpretCostcoAJAX(request)
    return render_template('results.html', locations=locations)
