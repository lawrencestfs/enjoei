import unittest
from datetime import datetime

from stock_prices import get_data


class SearchTestCase(unittest.TestCase):
    ticker = 'ENJU3'
    url = 'https://br.advfn.com/bolsa-de-valores/bovespa/enjoei-com-br-atividades-on-ENJU3/cotacao'

    @staticmethod
    def get_result(self):
        result = get_data(
            ticker=self.ticker,
            url=self.url
        )
        return result

    def test_ticker(self):
        result = self.get_result(self)
        self.assertEqual(result.get('ticker'), 'ENJU3')

    def test_open_price(self):
        result = self.get_result(self)
        self.assertEqual(result.get('open'), 10.86)

    def test_high_price(self):
        result = self.get_result(self)
        self.assertEqual(result.get('high'), 11.01)

    def test_low_price(self):
        result = self.get_result(self)
        self.assertEqual(result.get('low'), 10.67)

    def test_close_price(self):
        result = self.get_result(self)
        self.assertEqual(result.get('close'), 10.70)

    def test_date(self):
        result = self.get_result(self)
        self.assertEqual(result.get('date'), datetime.today().replace(microsecond=0))


if __name__ == '__main__':
    unittest.main()
