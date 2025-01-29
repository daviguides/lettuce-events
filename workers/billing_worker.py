from lettuce import Lettuce
from pprint import pprint


def purchase_handler(event):
    """Handles incoming 'purchase_created' events."""
    print("Event received")
    pprint(event.__dict__)


# Initialize Lettuce with the worker name 'billing_worker'
lettuce = Lettuce(worker_name="billing_worker")

# Start listening for 'purchase_created' events
lettuce.listen(name="purchase_created", handler=purchase_handler)