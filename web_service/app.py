from flask import Flask, render_template, request, redirect
import requests
import pickle
import numpy as np
import os


app = Flask(__name__)
model_path = os.path.join('model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)


DB_SERVICE_URL = "http://dbapp_container:5001/record"

iris_classes = {
    0: 'Setosa',
    1: 'Versicolor',
    2: 'Virginica'
}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':

        sepal_length = float(request.form['sepal_length'])
        sepal_width = float(request.form['sepal_width'])
        petal_length = float(request.form['petal_length'])
        petal_width = float(request.form['petal_width'])
        features = [sepal_length, sepal_width, petal_length, petal_width]
        print(features)
        features = np.array(features)
        features = features.reshape(1, -1)
        pred = model.predict(features)
        ans = pred[0]

        flower_name = iris_classes[ans]

        res = requests.post(DB_SERVICE_URL,
                            {"sepal_length": sepal_length, "sepal_width": sepal_width, "petal_length": petal_length, "petal_width": petal_width, "predicted_class": flower_name})

        print("Response from db", res)

        return render_template('index.html', prediction=flower_name)
    else:
        return redirect(location='/')


@app.route('/show-result')
def show_result():
    # comme
    records = requests.get(DB_SERVICE_URL)
    print("records", records.json())
    return render_template('show-result.html', records=records.json())


if __name__ == '__main__':
    print("testing commit build")
    app.run(host="0.0.0.0", port=5000, debug=True)
