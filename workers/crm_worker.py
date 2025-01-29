from lettuce import Lettuce
from pprint import pprint


def registration_handler(event):
    """Handles incoming 'registration_created' events."""
    print("Event received")
    pprint(event.__dict__)


# Initialize Lettuce with the worker name 'crm_worker'
lettuce = Lettuce(worker_name="crm_worker")

# Start listening for 'registration_created' events
lettuce.listen(name="registration_created", handler=registration_handler)