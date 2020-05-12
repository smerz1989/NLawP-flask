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

def create_geoplot(geojsonfile):
    geojson = json.load(open(geojsonfile,'r'))
    geo_source = GeoJSONDataSource(geojson=json.dumps(geojson))

    tile_provider = get_provider(CARTODBPOSITRON)
    tooltips = [("District","@DISTRICT"),("District Number","@District_N"),("Win Chance","@Win_Chance")]
    p = figure(x_range=(-1.4e7,-7e6),y_range=(2.6e6,6.4e6),plot_height = 600 , plot_width = 950,
                       x_axis_type="mercator", y_axis_type="mercator",tooltips=tooltips)
    p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
    p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks

    p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
    p.yaxis.minor_tick_line_color = None 
    p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
    p.yaxis.major_label_text_font_size = '0pt'
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.add_tile(tile_provider)
    p.patches('xs','ys',source=geo_source,fill_alpha=0.7,line_color="white",line_width=0.5)
    script, div = components(p)
    return script,div

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
