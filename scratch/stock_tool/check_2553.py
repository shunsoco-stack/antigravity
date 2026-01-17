import pandas as pd

url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
try:
    df = pd.read_excel(url)
    # Check code 2553
    # JPX codes in excel might be int or string.
    df['CodeStr'] = df['コード'].astype(str).str.strip()
    target = df[df['CodeStr'] == '2553']
    
    if not target.empty:
        print("Found 2553:")
        print(target[['コード', '銘柄名', '市場・商品区分']].to_string())
    else:
        print("2553 not found.")
        
except Exception as e:
    print(e)
