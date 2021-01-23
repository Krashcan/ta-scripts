import csv
import sys
import urllib.request


class CandleStick:
    name = ""
    open_p = close = high = low = 0
    turnover = 0

    MAROBOZU_CANDLESTICK_LENGTH_THRESHOLD = 98

    def __init__(self, name, open_p, close, high, low, turnover):
        self.name = name
        self.open_p = float(open_p)
        self.close = float(close)
        self.high = float(high)
        self.low = float(low)
        self.turnover = float(turnover)

    def body_length(self):
        body_size = abs(self.close - self.open_p)
        total_size = self.high-self.low
        return (body_size/total_size) * 100

    def stick_length(self):
        return ((self.high - self.low) / self.low) * 100

    def is_tradable_stick(self):
        return 1 <= self.stick_length() <= 10

    def is_bullish_marobozu(self):
        return self.open_p < self.close and self.body_length() > self.MAROBOZU_CANDLESTICK_LENGTH_THRESHOLD

    def is_bearish_marobozu(self):
        return self.close > self.open_p and self.body_length() > self.MAROBOZU_CANDLESTICK_LENGTH_THRESHOLD


def bse_csv_reader(filename):
    candlesticks = []
    with open(filename) as csv_file:
        line_count = 0
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
            else:
                candlesticks.append(CandleStick(row[1], row[4], row[7], row[5], row[6], row[12]))
            line_count += 1
    return candlesticks


# def get_bse_url(date):
#     base_url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ{}_CSV.ZIP'
#     return base_url.format(date)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        candlesticks = bse_csv_reader(sys.argv[1])
        bullish = []
        bearish = []
        for candlestick in candlesticks:
            if candlestick.is_bullish_marobozu():
                bullish.append(candlestick)
            if candlestick.is_bearish_marobozu():
                bearish.append(candlestick)
        bullish.sort(key=lambda x: x.turnover, reverse=True)
        with open('bullish_marobozu.csv', 'w', newline='') as file:
            fieldnames = ['name', 'body_length', 'stick_length', 'is_tradable', 'stoploss', 'turnover']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            print('BULLISH MAROBOZU sticks:')
            for cs in bullish:
                print(cs.name, cs.body_length(), cs.is_tradable_stick(), "stoploss=", cs.low, 'turnover=', cs.turnover)
                writer.writerow({'name': cs.name, 'body_length': cs.body_length(), 'stick_length': cs.stick_length(),
                                 'is_tradable': cs.is_tradable_stick(), 'stoploss': cs.low, 'turnover': cs.turnover})





