# Implementation Plan - UI Streamlining (Screener Mode)

The user wants to remove the manual stock code input and keep filters always visible.
This effectively changes the tool from a "Checker" to a "Screener" that always runs against the full JPX list.

## Proposed Changes

### UI
#### [MODIFY] [app.py](file:///c:/Users/shunk/.gemini/antigravity/scratch/stock_tool/app.py)
- **Input Removal**:
    - Remove `input_tickers` `st.text_area`.
    - Update logic to *always* fetch the JPX stock list when the search button is clicked.
- **Filter Visibility**:
    - Remove `with st.expander(...)` block.
    - Place the filter columns directly in the layout.
- **Button**:
    - Rename button to "スクリーニング実行" (Run Screening) or similar for clarity.
    - Keep the warning that it fetches all stocks.

## Verification Plan

### Manual Verification
1.  **UI Check**:
    - Verify no text area exists.
    - Verify filters are visible immediately without clicking an expander.
2.  **Functionality**:
    - Click the button.
    - Verify it auto-downloads the JPX list and starts the fetch/filter loop.
