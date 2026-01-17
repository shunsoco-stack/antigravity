import yfinance as yf
info = yf.Ticker('1309.T').info
print(f"Type: {info.get('quoteType')}")
print(f"Name: {info.get('longName')}")
print(f"ShortName: {info.get('shortName')}")
