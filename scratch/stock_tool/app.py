import streamlit as st
import yfinance as yf
import pandas as pd
import stock_tool  # 追加
import importlib
importlib.reload(stock_tool)

# ページ設定
st.set_page_config(
    page_title="日本株情報取得ツール",
    page_icon="📈",
    layout="wide"
)



def main():
    st.title("📈 日本株情報取得ツール")
    st.markdown("銘柄コードを入力して、日本株（および米国株など）の情報を取得します。")
    st.markdown("※入力がない状態で「情報取得」を押すと、**全上場銘柄**を取得します（時間がかかります）。")

    st.markdown("条件を設定して「スクリーニング実行」を押すと、全上場銘柄から条件に合う銘柄を抽出します（時間がかかります）。")

    st.header("スクリーニング条件")
    st.caption("0を指定した場合は制限なしとなります（下限の0は含みます）")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # PER
        st.markdown("##### PER (株価収益率)")
        per_help = "Price Earnings Ratio。株価が1株当たり純利益の何倍まで買われているかを示します。一般的に15倍以下が割安と言われます。"
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            min_per = st.number_input("下限 (倍)", min_value=0.0, value=0.0, step=0.1, key="min_per", help=per_help)
        with sub_col2:
            max_per = st.number_input("上限 (倍)", min_value=0.0, value=0.0, step=0.1, key="max_per", help=per_help)

        # PBR
        st.markdown("##### PBR (株価純資産倍率)")
        pbr_help = "Price Book-value Ratio。株価が1株当たり純資産の何倍まで買われているかを示します。1倍以下は解散価値より割安と言われます。"
        sub_col3, sub_col4 = st.columns(2)
        with sub_col3:
            min_pbr = st.number_input("下限 (倍)", min_value=0.0, value=0.0, step=0.1, key="min_pbr", help=pbr_help)
        with sub_col4:
            max_pbr = st.number_input("上限 (倍)", min_value=0.0, value=0.0, step=0.1, key="max_pbr", help=pbr_help)

    with col2:
        # 配当利回り
        st.markdown("##### 配当利回り (%)")
        div_help = "投資額に対する年間配当金の割合です。3%以上が高配当の目安とされます。"
        sub_col5, sub_col6 = st.columns(2)
        with sub_col5:
            min_div = st.number_input("下限 (%)", min_value=0.0, value=0.0, step=0.1, key="min_div", help=div_help)
        with sub_col6:
            max_div = st.number_input("上限 (%)", min_value=0.0, value=0.0, step=0.1, key="max_div", help=div_help)

    search_button = st.button("スクリーニング実行", type="primary")

    if search_button:
        st.warning("全銘柄リストを取得・検索します。この処理には非常に時間がかかります。")
        with st.spinner("JPXから銘柄リストを取得中..."):
            tickers = stock_tool.get_all_jpx_tickers()
            if not tickers:
                st.error("銘柄リストの取得に失敗しました。")
                return
        st.info(f"全取扱銘柄 {len(tickers)} 件を読み込みました。スクリーニングを開始します...")
        
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 結果表示用のプレースホルダーを作成
        st.subheader("取得結果（リアルタイム更新）")
        result_table = st.empty()
        
        # カラム設定（共通化）
        column_config = {
            "Current Price": st.column_config.NumberColumn(format="%.2f"),
            "Previous Close": st.column_config.NumberColumn(format="%.2f"),
            "Market Cap": st.column_config.NumberColumn(format="%.0f"),
            "Dividend Yield": st.column_config.NumberColumn(format="%.4f"),
        }

        for i, ticker in enumerate(tickers):
            status_text.text(f"Scanning: {ticker} ... Found: {len(results)} matches so far")
            data = stock_tool.get_stock_info(ticker)
            if data:
                # フィルタリング処理
                # ETF除外
                # 1. Typeフィールドによるチェック
                if data.get('Type') == 'ETF':
                    continue
                
                # 2. 名前によるチェック (フェイルセーフ: stock_toolの更新が反映されない場合など)
                name = data.get('Name', '').upper()
                if 'ETF' in name or 'EXCHANGE TRADED FUND' in name:
                    continue

                match = True
                
                # PER
                val_per = data.get('PER (Trailing)')
                has_per_limit = (min_per > 0 or max_per > 0)
                if val_per is not None:
                    if min_per > 0 and val_per < min_per: match = False
                    if max_per > 0 and val_per > max_per: match = False
                elif has_per_limit:
                     match = False

                # PBR
                val_pbr = data.get('PBR')
                has_pbr_limit = (min_pbr > 0 or max_pbr > 0)
                if val_pbr is not None:
                    if min_pbr > 0 and val_pbr < min_pbr: match = False
                    if max_pbr > 0 and val_pbr > max_pbr: match = False
                elif has_pbr_limit:
                    match = False
                    
                # 配当利回り (dataは0.03など。入力は3%)
                val_div = data.get('Dividend Yield')
                has_div_limit = (min_div > 0 or max_div > 0)
                if val_div is not None:
                    val_div_percent = val_div * 100
                    if min_div > 0 and val_div_percent < min_div: match = False
                    if max_div > 0 and val_div_percent > max_div: match = False
                elif has_div_limit:
                    match = False
                
                if match:
                    results.append(data)
                    # リアルタイムでテーブルを更新
                    df_current = pd.DataFrame(results)
                    result_table.dataframe(
                        df_current,
                        use_container_width=True,
                        column_config=column_config
                    )
                    
            progress_bar.progress((i + 1) / len(tickers))
        
        status_text.text(f"Done! Checked {len(tickers)} stocks. Found {len(results)} matches.")
        progress_bar.empty()

        if results:
            df = pd.DataFrame(results)
            # 最終的なテーブル表示（すでに表示されているが、CSVボタン等のためにdfを確定）
            # result_tableはそのまま残るが、念のため上書き更新しておく
            result_table.dataframe(
                df,
                use_container_width=True,
                column_config=column_config
            )
            
            # CSVダウンロードボタン
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="CSVをダウンロード",
                data=csv,
                file_name="stock_info.csv",
                mime="text/csv",
            )
        else:
            st.info("データが見つかりませんでした。")

if __name__ == '__main__':
    main()
