from flask import Flask, render_template, Response, request
import flask
import json

import plotly
import plotly.graph_objs as go
from plotly.graph_objs import Figure
from plotly.graph_objs import Layout

import pandas as pd
from json import encoder

app = Flask(__name__)
app.debug = True


def prepare_graph():
	df = pd.read_csv('static/san_francisco.csv')
	df = df[['TMAX','TMIN','DATE']]
	df['DATE'] = pd.to_datetime(df['DATE'], format="%Y%m%d")
	df = df.set_index('DATE')
	df = df.sort_index()
	df = df['20140101':'20161231']
	
	data = [go.Scatter(
		x = df.index,
		y = df[col],
		name = col,
		mode = 'lines',
	) for col in df.columns]
	
	layout = dict(title = 'San Francisco temperature')
	return Figure(data=data, layout=layout)


@app.route("/data")
def data():
	figure = prepare_graph()
	figureJSON = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)
	return Response(response=figureJSON, mimetype="application/json")

@app.route('/')
def index():
    return render_template('layouts/index.html')    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)