import yfinance as yf
import pandas as pd
import argparse
import sys

def get_all_jpx_tickers():
    """
    東証の全銘柄データをJPXのサイトから取得してリストで返す
    Returns:
        list: 銘柄コードのリスト（例: ['1301.T', '1305.T', ...]）
    """
    print("Fetching JPX data...")
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    try:
        # pandasでExcelを直接読み込む
        df = pd.read_excel(url)
        
        # 市場区分で絞り込み（プライム、スタンダード、グロースのみ）
        # カラム名は '市場・商品区分' であることを確認済み
        if '市場・商品区分' in df.columns:
            # 該当する区分を含む行のみ抽出
            target_markets = ['プライム', 'スタンダード', 'グロース']
            # df['市場・商品区分'] の中に target_markets のいずれかが含まれているか
            # 正規表現で 'プライム|スタンダード|グロース' を探す
            pattern = '|'.join(target_markets)
            df = df[df['市場・商品区分'].astype(str).str.contains(pattern, na=False)]
        else:
            print("Warning: '市場・商品区分' column not found, using all data.")

        # 'コード'カラムを取得 (データによってカラム名が変わる可能性に注意だが、通常は'コード')
        # 銘柄コードは数字4桁とは限らない（ETFなど）が、ここでは単純に抽出
        codes = df['コード'].astype(str)
        
        # 銘柄名も取得したい場合は辞書にするなど拡張可能だが、まずはコードのみでリスト化
        # 日本株なので .T をつける
        # 4桁以下の数字、または末尾に何か付いている場合などのケア
        
        tickers = []
        for code in codes:
            # コードが数字のみ、あるいは数字+文字だが、yfinance形式(.T)にする
            # JPXのデータは "1301" のようになっている
            # 念のためストリップ
            code = code.strip()
            # 4桁でなくても.Tをつけるのがyfinanceの流儀（名証などは.N等だが基本は.Tでトライ）
            tickers.append(f"{code}.T")
            
        print(f"Found {len(tickers)} tickers.")
        return tickers
    except Exception as e:
        print(f"Error fetching JPX data: {e}")
        return []

def get_stock_info(ticker_symbol):
    """
    指定された銘柄コードの情報を取得する
    日本株の場合は '.T' を付与して検索する
    """
    # 日本株対応: 数字のみ4桁の場合は .T を付与
    if ticker_symbol.isdigit() and len(ticker_symbol) == 4:
        ticker_symbol = f"{ticker_symbol}.T"
        
    print(f"Fetching data for: {ticker_symbol}...")
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # 取得できたか簡易チェック (regularMarketPriceなどが取れない場合がある)
        if not info or 'regularMarketPrice' not in info:
             # yfinanceはエラーを吐かずに空に近い辞書を返すことがあるため
             # 必須そうなキーでチェックするが、バージョンによってキーが異なることもある
             # ここでは簡易的に名前が取れるかで判断
             pass

        q_type = info.get('quoteType')
        name = info.get('longName') or info.get('shortName') or ''
        
        # quoteTypeがETFでなくても、名前にETFが含まれる場合はETFとみなす
        # 1309.Tなどが漏れる場合への対策
        name_upper = name.upper()
        if q_type == 'ETF':
            stock_type = 'ETF'
        elif 'ETF' in name_upper or 'EXCHANGE TRADED FUND' in name_upper:
            stock_type = 'ETF'
        else:
            stock_type = q_type

        data = {
            'Symbol': ticker_symbol,
            'Name': name,
            'Current Price': info.get('currentPrice') or info.get('regularMarketPrice') or info.get('ask'),
            'Previous Close': info.get('previousClose'),
            'Market Cap': info.get('marketCap'),
            'PER (Trailing)': info.get('trailingPE'),
            'PBR': info.get('priceToBook'),
            'Dividend Yield': info.get('dividendYield'),
            'Currency': info.get('currency'),
            'Type': stock_type
        }
        
        return data

    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Get Japanese stock information.')
    parser.add_argument('tickers', metavar='T', type=str, nargs='*',
                        help='Stock ticker symbols (e.g., 7203 for Toyota)')
    parser.add_argument('--csv', metavar='FILE', type=str, help='Output to CSV file')
    parser.add_argument('--web', action='store_true', help='Launch web interface')
    
    args = parser.parse_args()

    if args.web:
        import subprocess
        import os
        
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        app_path = os.path.join(script_dir, 'app.py')
        
        print(f"Launching web interface from {app_path}...")
        try:
            # Use sys.executable to ensure we use the same python environment
            # and run streamlit as a module to avoid PATH issues
            subprocess.run([sys.executable, "-m", "streamlit", "run", app_path], check=True)
        except KeyboardInterrupt:
            print("\nWeb interface stopped.")
        except Exception as e:
            print(f"Error launching web interface: {e}")
        return
    
    screening_mode = False
    if not args.tickers:
        print("No stock tickers specified.")
        confirm = input("Do you want to fetch ALL JPX stocks? This may take a long time. (y/n): ")
        if confirm.lower() == 'y':
            screening_mode = True
            args.tickers = get_all_jpx_tickers()
            if not args.tickers:
                print("Failed to fetch ticker list.")
                sys.exit(1)
        else:
            parser.print_help()
            sys.exit(1)
    else:
        # User specified tickers manually
        screening_mode = False

    results = []
    
    for symbol in args.tickers:
        data = get_stock_info(symbol)
        if data:
            # If in screening mode (fetching all stocks), exclude ETFs
            if screening_mode and data.get('Type') == 'ETF':
                continue
            results.append(data)
            
    if not results:
        print("No data found.")
        return

    df = pd.DataFrame(results)
    
    # 見やすく表示するために列を並び替えたりフォーマット調整
    # 金額表示などを調整してもよいが、まずはそのまま表示
    print("\n--- Results ---")
    print(df.to_string(index=False))
    
    if args.csv:
        df.to_csv(args.csv, index=False, encoding='utf-8-sig')
        print(f"\nSaved to {args.csv}")

if __name__ == '__main__':
    main()
