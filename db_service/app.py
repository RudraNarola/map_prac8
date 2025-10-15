from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prediction.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sepal_length = db.Column(db.Float, nullable=False)
    sepal_width = db.Column(db.Float, nullable=False)
    petal_length = db.Column(db.Float, nullable=False)
    petal_width = db.Column(db.Float, nullable=False)
    predicted_class = db.Column(db.String(50), nullable=False)


@app.route('/record', methods=["GET", "POST"])
def record_service():
    if request.method == "GET":
        records = Prediction.query.all()
        records = [{"sepal_length": rec.sepal_length, "sepal_width": rec.sepal_width, "petal_length": rec.petal_length,
                    "petal_width": rec.petal_width, "predicted_class": rec.predicted_class} for rec in records]
        return jsonify(records)
    else:
        sepal_length = float(request.form['sepal_length'])
        sepal_width = float(request.form['sepal_width'])
        petal_length = float(request.form['petal_length'])
        petal_width = float(request.form['petal_width'])
        predicted_class = request.form["predicted_class"]

        pred = Prediction(sepal_length=sepal_length, sepal_width=sepal_width,  # type: ignore
                          petal_length=petal_length, petal_width=petal_width,  predicted_class=predicted_class)  # type: ignore

        db.session.add(pred)
        db.session.commit()

        return jsonify({"message": "Successfully Saved Record"})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5001, debug=True)
