import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
from scipy.interpolate import barycentric_interpolate
import numpy as np
import io
import base64

app = Flask(__name__)

data_points = []  # Store the data points

@app.route('/')
def index():
    # get the points to interpolate
    # not sure what this is even for lol


    return render_template('index.html',)

@app.route('/add_point', methods=['POST'])
def add_point():

    # Receive the clicked coordinates from JavaScript
    data = request.get_json()
    x = data['x']
    y = data['y']

    # Add the data point to the list
    data_points.append((x, y))

    return 'OK'


@app.route('/get_data')
def get_data():
    print('data_points:', data_points)
    # get the points to interpolate
    xi = np.array([d[0] for d in data_points])
    yi = np.array([d[1] for d in data_points])
    j = np.arange(101)
    xch = np.cos(j*np.pi/100) * 200 + 200
    ych = barycentric_interpolate(xi, yi, xch)

    return jsonify({'x_data': xch.tolist(), 'y_data': ych.tolist()})



if __name__ == '__main__':
    app.debug = True

    app.run()
