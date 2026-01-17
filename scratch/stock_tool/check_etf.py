import pandas as pd

url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
print(f"Reading {url}...")
try:
    df = pd.read_excel(url)
    # Search for "ChinaAMC" or "SSE50" in name
    # Column for name is usually '銘柄名'
    mask = df['銘柄名'].astype(str).str.contains('ChinaAMC|SSE50', case=False, na=False)
    matches = df[mask]
    
    if not matches.empty:
        print("Found Matches:")
        for _, row in matches.iterrows():
            print(f"Code: {row['コード']}, Name: {row['銘柄名']}, Market: {row['市場・商品区分']}")
    else:
        print("No matches found for ChinaAMC/SSE50.")
        
    # Also check unique markets again to be sure
    print("\nUnique Markets:")
    print(df['市場・商品区分'].astype(str).unique())

except Exception as e:
    print(e)
