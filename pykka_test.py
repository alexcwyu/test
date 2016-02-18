import pykka
import pykka.gevent


class Greeter(pykka.gevent.GeventActor):
    def __init__(self, greeting='Hi there!'):
        super(Greeter, self).__init__()
        self.greeting = greeting

    def on_receive(self, message):
        print self.greeting, message

actor_ref = Greeter.start(greeting='Hi you!')
actor_ref.tell({'no': 'Norway', 'se': 'Sweden'})
actor_ref.tell({'a': 3, 'b': 4, 'c': 5})
actor_ref.stop()