from lettuce import Lettuce
from pprint import pprint


def payment_handler(event):
    """Handles incoming 'payment_created' events."""
    print("Event received")
    pprint(event.__dict__)


# Initialize Lettuce with the worker name 'logs_payment_worker'
lettuce = Lettuce(worker_name="logs_payment_worker")

# Start listening for 'payment_created' events
lettuce.listen(name="payment_created", handler=payment_handler)