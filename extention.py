import requests
import json
from config import keys


class APIException(Exception):
    pass


class MoneyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Введено некорректное количество валюты к переводу')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={quote_ticker}&symbols={base_ticker}')
        total_base = amount * json.loads(r.content)['rates'][keys[base]]

        return total_base

    @staticmethod
    def get_date(quote: str, base: str):
        quote_ticker = keys[quote]
        base_ticker = keys[base]
        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={quote_ticker}&symbols={base_ticker}')
        money_date = json.loads(r.content)['date']

        return money_date
