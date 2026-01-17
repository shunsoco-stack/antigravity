import stock_tool
import yfinance as yf

etfs = ['1309.T', '1306.T', '1321.T', '1570.T', '1357.T']
stocks = ['7203.T', '9984.T']

with open('verify_result.txt', 'w', encoding='utf-8') as f:
    f.write("--- Checking ETFs ---\n")
    for ticker in etfs:
        data = stock_tool.get_stock_info(ticker)
        f.write(f"{ticker}: Type={data.get('Type')}, Name={data.get('Name')}\n")
        if data.get('Type') != 'ETF':
            f.write(f"!!! WARNING: {ticker} is NOT labeled as ETF via stock_tool !!!\n")
            # Direct check
            info = yf.Ticker(ticker).info
            f.write(f"Direct yfinance check: {info.get('quoteType')}\n")

    f.write("\n--- Checking Stocks ---\n")
    for ticker in stocks:
        data = stock_tool.get_stock_info(ticker)
        f.write(f"{ticker}: Type={data.get('Type')}, Name={data.get('Name')}\n")
