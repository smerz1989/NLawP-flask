from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
import os
from config import Config
from models import OutcomeForm
import requests
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import (ColumnDataSource, HoverTool, 
			PrintfTickFormatter, GeoJSONDataSource, CustomJS)
from bokeh.tile_providers import CARTODBPOSITRON, get_provider, STAMEN_TERRAIN
import json
import plotting

app = Flask(__name__)
app.config.from_object(Config)

Bootstrap(app)

@app.route('/',methods=['GET'])
def index():
    form = OutcomeForm() 
    script,div = plotting.create_geoplot('./static/javascript/USDistrict.geojson')
    return render_template('index.html',form=form,script=script,div=div)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=33507)
