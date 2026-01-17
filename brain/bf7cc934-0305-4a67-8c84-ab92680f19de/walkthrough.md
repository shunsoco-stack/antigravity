# Web Visualization Walkthrough

I have implemented the ability to view stock data in a web browser.

## Changes

### `stock_tool.py`
- Added `--web` command line argument.
- Implemented logic to launch the existing `app.py` using Streamlit when `--web` is used.

## Verification Results

### CLI Verification
Ran `python stock_tool.py --help` and confirmed the `--web` option is available.

```text
options:
  -h, --help  show this help message and exit
  --csv FILE  Output to CSV file
  --web       Launch web interface
```

## How to Run

To open the web interface, run:
```bash
python stock_tool.py --web
```
This will launch the Streamlit application in your default web browser.
