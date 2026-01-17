import stock_tool
import concurrent.futures
import time

def check_stock(ticker):
    try:
        data = stock_tool.get_stock_info(ticker)
        if not data:
            return None
            
        # Filter ETF (using robust check from previous step)
        if data.get('Type') == 'ETF':
            return None
        name = data.get('Name', '').upper()
        if 'ETF' in name or 'EXCHANGE TRADED FUND' in name:
            return None
            
        # Filter Dividend Yield >= 4%
        div = data.get('Dividend Yield')
        if div is None:
            return None
            
        if div >= 0.04:
            return data
            
    except Exception:
        return None
    return None

def main():
    print("Fetching ticker list...")
    tickers = stock_tool.get_all_jpx_tickers()
    print(f"Total tickers: {len(tickers)}")
    
    # Limit for testing if needed, or run all if capable
    # tickers = tickers[:100] 
    
    high_div_stocks = []
    
    print("Starting screening (this make take a few minutes)...")
    start_time = time.time()
    
    # Use ThreadPoolExecutor for IO bound tasks
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_ticker = {executor.submit(check_stock, t): t for t in tickers}
        
        completed = 0
        for future in concurrent.futures.as_completed(future_to_ticker):
            completed += 1
            if completed % 100 == 0:
                print(f"Processed {completed}/{len(tickers)}...")
                
            result = future.result()
            if result:
                high_div_stocks.append(result)

    elapsed = time.time() - start_time
    print(f"\nScreening complete in {elapsed:.1f} seconds.")
    print(f"Found {len(high_div_stocks)} stocks with Dividend Yield >= 4%.")
    
    # Sort by Dividend Yield descending
    high_div_stocks.sort(key=lambda x: x['Dividend Yield'], reverse=True)
    
    print("\nTop 20 High Dividend Stocks:")
    print(f"{'Ticker':<8} {'Yield':<8} {'Name'}")
    print("-" * 40)
    for stock in high_div_stocks[:20]:
        print(f"{stock['Symbol']:<8} {stock['Dividend Yield']*100:.2f}%   {stock['Name']}")

if __name__ == "__main__":
    # Suppress print from stock_tool.get_stock_info to avoid spam
    import sys
    import os
    
    # Simple suppression might be hard since it's in the function
    # But for this purpose, we can just let it flow or ignore
    main()
