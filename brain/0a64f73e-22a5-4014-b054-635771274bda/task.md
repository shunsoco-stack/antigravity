# Task List

- [x] Analyze efficient ways to fetch "all" stocks (Total TSE list vs Index).
- [x] Create implementation plan. <!-- id: 0 -->
- [x] Add `openpyxl` and `xlrd` to `requirements.txt` for reading JPX Excel list. <!-- id: 1 -->
- [x] Implement function to download/parse TSE stock list. <!-- id: 2 -->
- [x] Modify `app.py` to handle empty input by triggering "Fetch All". <!-- id: 3 -->
- [x] Optimize "Fetch All" to use bulk download if possible, or warn user. (Implemented warning) <!-- id: 4 -->
- [x] Verify the changes. <!-- id: 5 -->

## Search Filters (PER, PBR, Dividend Yield)
- [x] Create implementation plan for filters. <!-- id: 6 -->
- [x] Add sidebar inputs for Min/Max PER, PBR, Dividend Yield in `app.py`. <!-- id: 7 -->
- [x] Implement filtering logic inside the fetch loop in `app.py`. <!-- id: 8 -->
- [x] Verify filtering works with example stocks. <!-- id: 9 -->

## UI Refinements
- [x] Move search inputs from Sidebar to Main Area (Top). <!-- id: 10 -->
- [x] Add explanatory tooltips for PER and PBR. <!-- id: 11 -->
- [x] Verify the layout changes. <!-- id: 12 -->

## UI Streamlining (Screener Mode)
- [x] Remove stock code input field (Default to "All"). <!-- id: 13 -->
- [x] Make filters always visible (Remove Expander). <!-- id: 14 -->
- [x] Verify the screener workflow. <!-- id: 15 -->

## UI Tweaks & Fixes
- [x] Align Min/Max inputs horizontally and adjust width. <!-- id: 16 -->
- [x] Fix filter logic to exclude `None` data when limit is active. <!-- id: 17 -->
- [x] Improve UI feedback: Show "Scanning X/Total" and "Hits: Y" separately. <!-- id: 18 -->
- [x] Implement real-time result table updates. <!-- id: 19 -->

## Market Section Filtering
- [x] Inspect JPX Excel column names. <!-- id: 18 -->
- [x] Modify `get_all_jpx_tickers` in `stock_tool.py` to filter by market section. <!-- id: 19 -->
- [x] Verify the filtering correctly reduces the number of tickers. <!-- id: 20 -->
