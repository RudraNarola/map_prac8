import pytest
import json
from app import app, db, Prediction


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


def test_record_get_returns_saved_records(client):
    form_data = {
        'sepal_length': '6.3',
        'sepal_width': '3.3',
        'petal_length': '6.0',
        'petal_width': '2.5',
        'predicted_class': 'Virginica'
    }

    client.post('/record', data=form_data)
    response = client.get('/record')

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data) == 1
    assert response_data[0]['sepal_length'] == 6.3
    assert response_data[0]['sepal_width'] == 3.3
    assert response_data[0]['petal_length'] == 6.0
    assert response_data[0]['petal_width'] == 2.5
    assert response_data[0]['predicted_class'] == 'Virginica'


if __name__ == "__main__":
    # testing
    pytest.main([__file__, "-v"])
