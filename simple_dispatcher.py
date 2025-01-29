from lettuce import Lettuce

lettuce = Lettuce(broker='amqp://guest:guest@localhost:5672/lettuce')
lettuce.dispatch(name="pagou", data={'name':'davi', 'age': 30})
