from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__, template_folder='templates')
CORS(app, resources={r"/api/*": {"origins": "*"}})

data = pd.read_csv('water_potability.csv')

acceptable_ranges = {
    'ph': (data['ph'].quantile(0.25), data['ph'].quantile(0.75)),
    'Hardness': (data['Hardness'].quantile(0.25), data['Hardness'].quantile(0.75)),
    'Solids': (data['Solids'].quantile(0.25), data['Solids'].quantile(0.75)),
    'Chloramines': (data['Chloramines'].quantile(0.25), data['Chloramines'].quantile(0.75)),
    'Sulfate': (data['Sulfate'].quantile(0.25), data['Sulfate'].quantile(0.75)),
    'Conductivity': (data['Conductivity'].quantile(0.25), data['Conductivity'].quantile(0.75)),
    'Organic_carbon': (data['Organic_carbon'].quantile(0.25), data['Organic_carbon'].quantile(0.75)),
    'Trihalomethanes': (data['Trihalomethanes'].quantile(0.25), data['Trihalomethanes'].quantile(0.75)),
    'Turbidity': (data['Turbidity'].quantile(0.25), data['Turbidity'].quantile(0.75))
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.json
        values = {key: float(data[key]) for key in acceptable_ranges.keys()}
        potable = all(acceptable_ranges[key][0] <= values[key] <= acceptable_ranges[key][1] for key in values)
        return jsonify({'potable': potable, 'values': values})
    else:
        return render_template("main.html")
    