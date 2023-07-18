from flask import Flask, render_template, request, jsonify
from scipy.interpolate import barycentric_interpolate
import numpy as np

app = Flask(__name__)

data_points = []  # Store the data points
x_points = set() # Store x-coord of clicked points to avoid zero-divide
cheby = True

@app.route('/')
def index():
    data_points.clear()  # empty list when page is loaded/refreshed
    x_points.clear()

    return render_template('index.html',)

@app.route('/add_point', methods=['POST'])
def add_point():

    # Receive the clicked coordinates from JavaScript
    data = request.get_json()
    x = data['x']
    y = data['y']

    # Add the data point to the list, if the x hasn't already been clicked
    if x not in x_points: # makes sure no divide by zero errors occur.
        data_points.append((x, y))
        x_points.add(x)
    else:
        pass

    return 'OK'


@app.route('/get_data')
def get_data():
    print('data_points:', data_points)
    # get the points to interpolate
    xi = np.array([d[0] for d in data_points])
    yi = np.array([d[1] for d in data_points])
    j = np.arange(101)
    if cheby:
        xch = np.cos(j*np.pi/100) * 200 + 200
    else:
        xch = np.linspace(0,400,101)
    ych = barycentric_interpolate(xi, yi, xch)

    return jsonify({'x_data': xch.tolist(), 'y_data': ych.tolist()})


@app.route('/modify_zeros', methods=['POST'])
def modify_zeros():
    cheby = bool(int(request.form['zeros']))
    index()

    return 'OK'

if __name__ == '__main__':
    app.debug = True

    app.run()
