import os
from twilio.rest import Client
import requests
import json
import schedule
import time
import sys


def PriceCheck(coin):
     response = requests.get(f'https://api.coinbase.com/v2/prices/{coin}-USD/spot')
     data = response.json()
     cryptoInfo = data['data']
     coin = cryptoInfo["base"]
     currency = cryptoInfo["currency"]
     val = cryptoInfo["amount"]
     return f'{coin} is currently at {val} {currency}'


def SendText(coinsToCheck):
     m=""
     for coin in coinsToCheck:
          m+=PriceCheck(coin)+"\n"
     account_sid = os.environ['TWILIO_ACCOUNT_SID']
     auth_token = os.environ['TWILIO_AUTH_TOKEN']
     client = Client(account_sid, auth_token)

     message = client.messages \
                     .create(
                          body=m,
                          from_=os.environ['TPN'],
                          to=os.environ['PN']
                 )


def job():
     global eligibleCrpytos
     SendText(eligibleCrpytos)


if __name__ == "__main__":
     coinBaseCryptos = ['ZRX', '1INCH', 'AAVE', 'ALGO', 'AMP', 'FORTH', 'ANKR', 'BAL', 'Token BNT', 'BAND', 'BOND', 'Token BAT', 'BTC', 'Cash BCH', 'ADA', 'CTSI', 'CGLD', 'CHZ', 'COMP', 'ATOM', 'Token CRV', 'DAI', 'COMP', 'DASH', 'COMP', 'DOGE', 'Coin ENJ', 'MLN', 'EOS', 'ETH', 'ETC', 'FIL', 'GTC', 'RLC', 'ICP', 'KEEP', 'KNC', 'LTC', 'LRC', 'MIR', 'NKN', 'NU', 'NMR', 'OMG', 'OXT', 'OGN', 'DOT', 'MATIC', 'REN', 'SKL', 'SOL', 'XLM', 'STORJ', 'SUSHI', 'SNX', 'TRB', 'USDT', 'XTZ', 'GRT', 'UMA', 'UNI', 'USDC', 'WTBC', 'YFI', 'ZEC']
     eligibleCrpytos = [x for x in sys.argv if x.upper() in coinBaseCryptos]
     if len(eligibleCrpytos)==0: eligibleCrpytos = ['ETH', 'BTC']

schedule.every().day.at("12:00").do(job)

while True:
     schedule.run_pending()
     time.sleep(1)
