from collections import deque
from typing import Callable

# module interal variables
__CURRENCY_PAIR_KEY__ = "currencyPair"
__RATE_KEY__ = "rate"
__TIMESTAMP_KEY__ = "timestamp"
__LEAKY_QUEUE_LEN__ = 5 * 60 + 1


class Observable:
    """
    A class that can subclassed to get a callback subscription.

    ...

    Methods
    -------
    attach(observer)
        Adds an observer callback to an internal list of observers
    notify()
        Runs the callbacks stored in an internal list of observers
    """

    def __init__(self) -> None:
        self._observers = []

    def attach(self, observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer(self)


class ExchangeRatesData:
    """
    A class used to store currency pairs and their rates.

    ...

    Attributes
    ----------
    currency_pairs : dict
        a dictionary mapping currency pairs to their readings stored in 
        CurrencyPairData object
    callbacks : list
        a list of callbacks that are intended to observe the CurrencyPairData 
        objects in currency_pairs parameter

    Methods
    -------
    update(reading)
        Adds a reading to corresponding value in currency_pairs dict
    """

    def __init__(self, callbacks: list = []) -> None:
        self.currency_pairs = dict()
        self.callbacks = callbacks

    def update(self, reading: dict) -> None:
        if not self._isvalid_reading(reading):
            raise ValueError(
                "The reading(s) do(es) not contain all the expected keys.")
        currency_pair = reading[__CURRENCY_PAIR_KEY__]
        if currency_pair not in self.currency_pairs:
            self.currency_pairs[currency_pair] = CurrencyPairData(
                reading, self.callbacks
            )
        else:
            self.currency_pairs[currency_pair].append(reading)

    def _isvalid_reading(self, reading: dict) -> bool:
        expected_keys = set(
            [__CURRENCY_PAIR_KEY__, __RATE_KEY__, __TIMESTAMP_KEY__])
        if expected_keys.issubset(set(reading.keys())):
            return True
        else:
            return False


class CurrencyPairData(Observable):
    """
    A class used to keep track of the readings of a single currency pair

    ...

    Attributes
    ----------
    average : float
        keeps track of the average of the rate
    rates_leaky_queue : deque
        a sliding window that keeps track of the most recent exchange rate
    ts_leaky_queue : deque
        a sliding window that keeps track of the timestamps
        (we only need the most recent timestamp but, this can be used to 
        implement a more accurate average when we have jitter in the 
        readings arrival - NOT IMPLEMENTED YET)
    currency_pair : str
        the currency pair string

    Methods
    -------
    append(reading)
        Adds a reading to the sliding windows
    """

    def __init__(self, reading: dict, callbacks: list = []) -> None:
        super().__init__()
        self.average = 0.0
        # sliding window for exchange rates
        self.rates_leaky_queue = deque(
            [0.0] * __LEAKY_QUEUE_LEN__, maxlen=__LEAKY_QUEUE_LEN__)
        # sliding window for timestamps
        self.ts_leaky_queue = deque(
            [0.0] * __LEAKY_QUEUE_LEN__, maxlen=__LEAKY_QUEUE_LEN__)
        # a counter for more accurate average
        self._inserted_counter = 0
        # maintain the rates sum to avoid O(n) average calculation
        self._rates_sum = 0.0
        self.currency_pair = reading[__CURRENCY_PAIR_KEY__]
        self.append(reading)
        for callback in callbacks:
            self.attach(callback)

    def _update_average(self) -> None:
        self._rates_sum = self._rates_sum + \
            self.rates_leaky_queue[-1] - self.rates_leaky_queue[0]
        self.average = self._rates_sum / self._inserted_counter

    def append(self, reading: dict) -> None:
        self.rates_leaky_queue.append(reading[__RATE_KEY__])
        self.ts_leaky_queue.append(reading[__TIMESTAMP_KEY__])
        # for accurate average estimation for the early measurements, less than 5 min.
        if self._inserted_counter < __LEAKY_QUEUE_LEN__:
            self._inserted_counter = self._inserted_counter + 1
        # notify observers
        self.notify()
        # update the average
        self._update_average()


def alert_generator(subject: CurrencyPairData) -> None:
    """Prints an alert message if the spot rate for a currency pair changes 
    by more than 10% from the 5 minute average

    Arguments
    ----------
    subject : CurrencyPairData
        the currency pair rates of the last 5 minutes
    """

    latest_rate = subject.rates_leaky_queue[-1]
    # check for 10% change
    if abs(latest_rate - subject.average) > 0.1 * subject.average:
        alert_msg = {
            "timestamp": subject.ts_leaky_queue[-1],
            "currencyPair": subject.currency_pair,
            "alert": "spotChange",
        }
        print(alert_msg)
