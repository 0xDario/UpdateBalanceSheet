#!/bin/bash

# update_balance_sheet.sh

# ---- FIRST COMMAND ----
echo "[2/2] Running client portal..."
cd clientportal
./bin/run.sh ./root/conf.yaml &

# Save the PID of the first command
CLIENT_PORTAL_PID=$!

# ---- SECOND COMMAND ----
echo "[1/2] Running main.py..."
cd ..
source venv/bin/activate
python3 main.py

# Optionally, you can kill the client portal process if needed
# kill $CLIENT_PORTAL_PID

echo "All commands completed."