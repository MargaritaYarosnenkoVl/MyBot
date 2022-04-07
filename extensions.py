import requests
import json

from config import keys


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(quote, base, amount):
        try:
            quote_key = keys[quote]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        try:
            base_key = keys[base]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        if quote_key == base_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {quote}!')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key=451d8378fb590de30fdd1b3c7ab064ac&base={quote_key}&symbols={base_key}')
        resp = json.loads(r.content)
        new_price = resp['rates'][base_key] * float(amount)

        return round(new_price, 3)
