# Web Browser Visualization Implementation Plan

The goal is to allow the user to view stock data in a web browser instead of just CSV/Console output.
We will achieve this by integrating the existing `app.py` (Streamlit app) with the main `stock_tool.py` entry point.

## User Review Required
> [!NOTE]
> I will add a `--web` argument to `stock_tool.py`. Running `python stock_tool.py --web` will launch the web interface.

## Proposed Changes

### [stock_tool]

#### [MODIFY] [stock_tool.py](file:///c:/Users/shunk/.gemini/antigravity/scratch/stock_tool/stock_tool.py)
- Import `subprocess` and `os`.
- Add `--web` argument to `argparse`.
- If `--web` is checked:
    - Construct the path to `app.py`.
    - Execute `streamlit run app.py` using `subprocess`.
    - Exit after launching.

## Verification Plan

### Automated Tests
- None.

### Manual Verification
- Run `python stock_tool.py --web` and verify it attempts to launch Streamlit (I can check the console output or command status).
- Run `python stock_tool.py 7203` to ensure standard CLI functionality remains unchanged.
