#!/usr/bin/env python
import pika
import uuid
import json
import signal


class Event():
    """Represents an event with an ID, name, and data payload."""
    id = None
    name = None
    data = dict()


class Lettuce():
    """
    Lettuce is an event-driven abstraction layer that simulates a signal-based system,
    similar to Blinker but using RabbitMQ as the message broker.

    - It allows dispatching and listening to events asynchronously.
    - Works similarly to Blinker’s signals but enables cross-service communication.
    - Useful for mocking webhooks or integrating event-driven workflows.
    """

    def __init__(self, worker_name=None):
        self.connection = None
        self.channel = None
        self.queue_name = worker_name
        self.exchange_name = 'events'  # Defines the exchange for event routing
        self.event_topic = 'event.'  # Event topic prefix

        self.init_connection()
        self.declare_exchange()

    # Initializes connection with RabbitMQ
    def init_connection(self, broker='amqp://guest:guest@localhost:5672/lettuce'):
        parameters = pika.URLParameters(broker)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    # Closes connection with RabbitMQ
    def close_connection(self):
        self.connection.close()

    # Declares the exchange used for event routing
    def declare_exchange(self):
        self.channel.exchange_declare(
            exchange=self.exchange_name, exchange_type='topic')

    # Declares the queue (used for listening to events)
    def declare_queue(self):
        self.channel.queue_declare(self.queue_name, durable=True)

    # Binds the queue to a specific event routing key
    def bind_queue(self, binding_key):
        self.channel.queue_bind(exchange=self.exchange_name,
                                queue=self.queue_name,
                                routing_key=binding_key)

    # Dispatches an event to RabbitMQ
    def dispatch(self, name, data):
        """
        Publishes an event with a unique ID and payload to the message queue.

        Args:
        - name (str): Event name (used as the routing key).
        - data (dict): Payload containing event details.

        Returns:
        - dict: The dispatched event's data.
        """
        event = Event()
        event.name = name
        event.data = data
        event.id = str(uuid.uuid1())

        self.channel.basic_publish(exchange=self.exchange_name,
                                   routing_key=name,
                                   body=json.dumps(event.__dict__))

        print(f" [x] Event '{name}' dispatched with data: {data}")

        return event.__dict__

    # Adds an event listener for a specific event type
    def add_listener(self, name, handler):
        """
        Registers a function to handle incoming events matching the given name.

        Similar to Blinker’s signal handling but using RabbitMQ for event distribution.

        Args:
        - name (str): The event name (routing key).
        - handler (function): The function that will process the event.

        This method:
        - Declares a queue (if not already declared).
        - Binds the queue to listen for the specified event.
        - Defines a callback function to handle incoming messages.
        """
        self.declare_queue()
        self.bind_queue(name)
        self.handler = handler

        def callback(ch, method, properties, body):
            print(f" [x] Event received '{method.routing_key}': {body}")
            event = Event()
            event.__dict__ = json.loads(body)
            self.handler(event)  # Passes the event to the registered handler
            ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledges receipt

        self.channel.basic_consume(queue=self.queue_name,
                                   on_message_callback=callback)

    # Adds a listener and immediately starts consuming messages
    def listen(self, name, handler):
        self.add_listener(name, handler)
        self.consume()

    # Starts consuming messages from RabbitMQ
    def consume(self):
        """
        Starts listening for events and handling them via the registered callback.
        """
        self.handle_ctrl_c()
        print(' [*] Waiting for events. To exit press CTRL+C')
        self.channel.start_consuming()

    # Handles graceful shutdown on CTRL+C
    def handle_ctrl_c(self):
        def handler(signum, frame):
            self.channel.stop_consuming()
            self.close_connection()
            print('Closing connection')

        signal.signal(signal.SIGINT, handler)