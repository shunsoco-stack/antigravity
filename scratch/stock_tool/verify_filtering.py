import stock_tool
import sys

def verify():
    # Test case 1: ETF
    etf = stock_tool.get_stock_info('1321.T')
    if etf['Type'] != 'ETF':
        print(f"FAIL: 1321.T should be ETF, got {etf.get('Type')}")
        return False
    else:
        print("PASS: 1321.T identified as ETF")

    # Test case 2: Stock
    stock = stock_tool.get_stock_info('7203.T')
    if stock['Type'] == 'ETF':
        print(f"FAIL: 7203.T should NOT be ETF, got {stock.get('Type')}")
        return False
    else:
        print(f"PASS: 7203.T identified as {stock.get('Type')}")

    # Test case 3: REIT
    reit = stock_tool.get_stock_info('8951.T')
    if reit['Type'] == 'ETF':
        print(f"FAIL: 8951.T should NOT be ETF, got {reit.get('Type')}")
        return False
    else:
        print(f"PASS: 8951.T identified as {reit.get('Type')}")

    return True

if __name__ == '__main__':
    if verify():
        print("All tests passed.")
        sys.exit(0)
    else:
        print("Some tests failed.")
        sys.exit(1)
