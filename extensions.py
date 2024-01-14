from config import apikey, keys
import requests
import json

class APIException(Exception):
    pass
class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException('невозможно конвертировать одинаковые валюты')
        try:
            quote_ticker, base_ticker = keys[quote], keys[base]
        except KeyError:
            raise APIException('Не удалось определить название валюты')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')
        url = f'https://v6.exchangerate-api.com/v6/{apikey}/pair/{quote_ticker}/{base_ticker}/{amount}'
        r = requests.get(url)
        result = json.loads(r.content)['conversion_result']
        return result