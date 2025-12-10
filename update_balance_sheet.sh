#!/bin/bash

# update_balance_sheet.sh

# ---- FIRST COMMAND ----
echo "[2/2] Running client portal..."
osascript -e 'tell application "Terminal" to do script "cd /Users/darioturchi/repos/UpdateBalanceSheet/clientportal && ./bin/run.sh ./root/conf.yaml"'

# ---- SECOND COMMAND ----
echo "[1/2] Running main.py..."
osascript -e 'tell application "Terminal" to do script "cd /Users/darioturchi/repos/UpdateBalanceSheet && source venv/bin/activate && python3 main.py"'

echo "All commands completed."