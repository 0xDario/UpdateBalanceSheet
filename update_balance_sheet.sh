#!/bin/bash

# update_balance_sheet.sh

echo "Starting balance sheet update..."

# Detect terminal emulator: Ghostty or fallback to macOS Terminal
open_terminal_window() {
    local cmd="$1"
    if open -Ra Ghostty 2>/dev/null; then
        open -na Ghostty --args -e zsh -c "$cmd"
    else
        osascript -e "tell application \"Terminal\" to do script \"$cmd\""
    fi
}

# Step 1: Open client portal in a new terminal window
echo "[1/2] Starting IB Client Portal gateway..."
open_terminal_window "cd ~/repos/UpdateBalanceSheet/clientportal && ./bin/run.sh ./root/conf.yaml; exec zsh"

# Step 2: Wait for the gateway to start and user to authenticate
echo ""
echo ">>> Please open https://localhost:5001 in your browser and log in to Interactive Brokers. <<<"
echo ""
echo "Waiting for authentication..."

while true; do
    # Check if gateway is up and authenticated
    auth_response=$(curl -s -k https://localhost:5001/v1/api/iserver/auth/status 2>/dev/null)
    if echo "$auth_response" | grep -q '"authenticated":true'; then
        echo "Authentication confirmed!"
        break
    fi
    sleep 3
done

# Step 3: Open main Python script in another new terminal window
echo "[2/2] Running main.py..."
open_terminal_window "cd ~/repos/UpdateBalanceSheet && source venv/bin/activate && python3 main.py; exec zsh"

echo "All terminal windows launched."