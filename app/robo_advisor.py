#Followed Walkthrough for all core code
#https://pypi.org/project/python-dotenv/
#I had a lot of trouble getting dotenv to load, this was code from stack overflow and it seems to work
from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
import json
import csv
import os
import requests

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")


#heip's code was inspiration for the failing gracefully condition


while True:
	symbol=input("Please type a valid stock symbol: ")
	if not symbol.isalpha():
		print("Please try again, entering a valid stock ticker of 3-4 letters")
	else:
		data=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+str(symbol)+'&apikey='+str(api_key))

		if 'Error' in data.text:
			print("There has been an error. Please type a different stock symbol: ")
		else:
			break




request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

response = requests.get(request_url)
parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys())
latest_day = dates[0]
latest_close = tsd[latest_day]["4. close"]

high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)
# print(type(response))
# print(response.status_code)
# print(response.text)

#from groceries exercise
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)


#
# INFO OUTPUTS
#

# TODO: write response data to a CSV file

#from stream

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file: 
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() 
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })

# TODO: further revise the example outputs below to reflect real information
print("-----------------")
# print(f"STOCK SYMBOL: {symbol}")
print("RUN AT: 11:52pm on June 5th, 2018")
print("-----------------")
print(f"LATEST DAY OF AVAILABLE DATA: {last_refreshed}")
print(f"LATEST DAILY CLOSING PRICE: {to_usd(float(latest_close))} ")
print(f"RECENT AVERAGE HIGH CLOSING PRICE: {to_usd(float(recent_high))}")
print(f"RECENT AVERAGE LOW CLOSING PRICE: {to_usd(float(recent_low))}")

print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}")
print("-------------------------")

#Completed with help from Ashish Patel
print("-----------------")
threshold = 1.3*float(recent_low)
if float(latest_close) < threshold:
    print("RECOMMENDATION: BUY!")
    print("RECOMMENDATION REASON: The latest closing price is not larger than 30 percent of the recent low, indicating potential growth")
else:
    print("RECOMMENDATION: DONT BUY!")
    print("RECOMMENDATION REASON: The latest closing price is larger than 30 percent of the recent low, indicating potential decline")
print("----------------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-----------------")

