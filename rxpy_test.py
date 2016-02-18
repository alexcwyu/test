from rx.concurrency import GEventScheduler
from rx.observable import Observable, Observer
from rx.subjects import Subject
import rx
import gevent


scheduler = GEventScheduler()

class MyObserver(Observer):
    def on_next(self, x):
        print("Got: %s" % x)

    def on_error(self, e):
        print("Got error: %s" % e)

    def on_completed(self):
        print("Sequence completed")
#
# res = Observable.from_iterable(range(10))
# d = res.subscribe(MyObserver())

pauser = Subject()
source = rx.Observable.interval(1000, scheduler = scheduler).pausable(pauser)
source.subscribe(MyObserver())

pauser.on_next("test")