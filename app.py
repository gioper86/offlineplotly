from flask import Flask, render_template, Response, request
import flask
import json

import plotly
import plotly.graph_objs as go
from plotly.graph_objs import Figure
from plotly.graph_objs import Layout

import pandas as pd
from json import encoder
import quandl

app = Flask(__name__)
app.debug = True


def prepare_graph():
	mydata = quandl.get("NETH/HPI")
	df_cities = mydata.iloc[:,-4:]
	trace1 = go.Scatter (
	    x = df_cities["Amsterdam"].index,
	    y = df_cities["Amsterdam"],
	    mode = 'lines',
	    name = "Amsterdam"
	)

	trace2 = go.Scatter (
	    x = df_cities["Rotterdam"].index,
	    y = df_cities["Rotterdam"],
	    mode = 'lines+markers',
	    name = "Rotterdam"
	)
	
	layout = dict(title = 'Netherlands house prices')
	return Figure(data=[trace1, trace2], layout=layout)


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