from src.main.ratetracker import ExchangeRatesData, CurrencyPairData
from collections import deque
import pytest


def test_ratetracker():
    pass


def test_conformant_exchange_rates_reading():
    exchange_rates = ExchangeRatesData([])
    reading = {"timestamp": 1554933794.023,
               "currencyPair": "CNYAUD", "rate": 0.59281}
    exchange_rates.update(reading)
    assert list(exchange_rates.currency_pairs.keys()) == ["CNYAUD"]
    reading = {"timestamp": 1554933794.023,
               "currencyPair": "USDAUD", "rate": 0.59281}
    exchange_rates.update(reading)
    assert set(exchange_rates.currency_pairs.keys()) == {"CNYAUD", "USDAUD"}


def test_nonconformant_exchange_rates_reading():
    exchange_rates = ExchangeRatesData([])
    reading = {"timestamp": 1554933794.023,
               "currencypair": "CNYAUD", "rate": 0.59281}
    with pytest.raises(Exception) as exp:
        exchange_rates.update(reading)
    assert str(
        exp.value) == "The reading(s) do(es) not contain all the expected keys."


def test_rate_sliding_window():
    reading = {"timestamp": 1554933794.023,
               "currencyPair": "CNYAUD", "rate": 0}
    currency_pair_data = CurrencyPairData(reading)
    for rate_value in range(5*60):
        reading['rate'] = rate_value + 1
        currency_pair_data.append(reading)
    assert currency_pair_data.rates_leaky_queue[-1] == 5*60
    assert currency_pair_data.rates_leaky_queue[0] == 0
    assert currency_pair_data.rates_leaky_queue[1] == 1
    currency_pair_data.append(reading)
    assert currency_pair_data.rates_leaky_queue[-1] == 5*60
    assert currency_pair_data.rates_leaky_queue[0] == 1
    currency_pair_data.append(reading)
    assert currency_pair_data.rates_leaky_queue[-1] == 5*60
    assert currency_pair_data.rates_leaky_queue[0] == 2


def test_average_calculation():
    reading = {"timestamp": 1554933794.023,
               "currencyPair": "CNYAUD", "rate": 0}
    currency_pair_data = CurrencyPairData(reading)
    assert currency_pair_data.average == 0.0
    max_len = 5 * 60 + 1
    val_queue = deque(
        [0.0] * max_len, maxlen=max_len)
    for val in range(1000):
        reading['rate'] = val + 1
        val_queue.append(reading['rate'])
        currency_pair_data.append(reading)
    assert abs(currency_pair_data.average -
               ((sum(val_queue) - val_queue[0]) / max_len)) < 0.001
