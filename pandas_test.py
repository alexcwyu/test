import pandas as pd
from rx.concurrency import GEventScheduler
from rx.observable import Observable, Observer
from rx.subjects import Subject
import rx
from odo import odo
import blaze
import abc


class Provider:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def start(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def stop(self):
        raise NotImplementedError()


class Event:
    pass

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "%s(%s)" % (self.__class__.__name__, ', '.join(items))


class Bar(Event):
    def __init__(self, date, row):
        self.timestamp = date
        self.symbol = row['Symbol']
        self.open = row['Open']
        self.high = row['High']
        self.low = row['Low']
        self.close = row['Close']
        self.vol = row['Volume']
        self.adj_close = row['Adj Close']


class CSVDataFeed(Provider):
    pass


dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')

class PandasCSVDataFeed(CSVDataFeed):
    def __init__(self, subject, names):
        self.subject = subject
        self.dfs = []
        for name in names:
            df = pd.read_csv('data/%s.csv' % name, index_col='Date', parse_dates=['Date'], date_parser=dateparse)
            df['Symbol'] = name
            df['Frequency'] = 24 * 60 * 60
            self.dfs.append(df)

        self.df = pd.concat(self.dfs).sort_index(0, ascending=True)

    def start(self):
        for index, row in self.df.iterrows():
            self.subject.on_next(Bar(index, row))

    def stop(self):
        pass


# class BlazeCSVDataFeed(CSVDataFeed):
#     def __init__(self, subject, names):
#         self.subject = subject
#         self.dfs = []
#         for name in names:
#             d = blaze.Data('data/%s.csv' % name)
#             df['Symbol'] = name
#             df['Frequency'] = 24 * 60 * 60
#             self.dfs.append(df)
#
#         self.df = pd.concat(self.dfs).sort_index(0, ascending=True)
#
#     def start(self):
#         for index, row in self.df.iterrows():
#             self.subject.on_next(Bar(index, row))
#
#     def stop(self):
#         pass



class Strategy(Observer):
    def on_next(self, x):
        print x

    def on_error(self, e):
        print("STG Error: %s" % e)

    def on_completed(self):
        print("STG Completed")


class OrderManager(Observer):
    def on_next(self, x):
        print x

    def on_error(self, e):
        print("OM Error: %s" % e)

    def on_completed(self):
        print("OM Completed")


data_subject = Subject()
order_subject = Subject()
execution_report_subject = Subject()

strategy = Strategy()
orderManager = OrderManager()
data_subject.subscribe(strategy.on_next)
data_subject.subscribe(orderManager.on_next)

feed = PandasCSVDataFeed(names=['goog', 'msft'], subject=data_subject)
feed.start()

