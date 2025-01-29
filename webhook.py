from flask import Flask, request
from lettuce import Lettuce

# Initialize Flask app
app = Flask(__name__)

# Initialize Lettuce, which acts as an abstraction layer for event-driven behavior
lettuce = Lettuce()

@app.route('/')
def index():
    """Health check endpoint."""
    return 'Ok'


@app.route('/registrations', methods=['POST'])
def create_registration():
    """
    Mock endpoint simulating a user registration webhook.
    Dispatches an event via Lettuce, which abstracts event-driven behavior using RabbitMQ.
    """
    payload = request.get_json()
    return lettuce.dispatch(name="registration_created", data=payload)


@app.route('/purchases', methods=['POST'])
def create_purchase():
    """
    Mock endpoint simulating a purchase event webhook.
    Dispatches an event via Lettuce.
    """
    payload = request.get_json()
    return lettuce.dispatch(name="purchase_created", data=payload)


@app.route('/payments', methods=['POST'])
def create_payment():
    """
    Mock endpoint simulating a payment event webhook.
    Dispatches an event via Lettuce.
    """
    payload = request.get_json()
    return lettuce.dispatch(name="payment_created", data=payload)


if __name__ == "__main__":
    """
    Runs the Flask API server on port 8012 with single-threaded execution.
    """
    app.run(host='0.0.0.0', port=8012, debug=False, threaded=False)