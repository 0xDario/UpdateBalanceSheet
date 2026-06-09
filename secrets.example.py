# this is the file that contains all the secret information
# make a copy of this and rename it secrets.py and fill in the information below with your own credentials
WEALTHSIMPLE_USERNAME=''
WEALTHSIMPLE_PASSWORD=''
WEALTHIMSPLE_RRSP_ACCOUNT_ID=''
WEALTHIMSPLE_TFSA_ACCOUNT_ID=''
# Wealthsimple fetching is enabled by default. Uncomment the line below to skip
# it on this machine (e.g. if you don't have Wealthsimple accounts configured).
# ENABLE_WEALTHSIMPLE = False
IBKR_TFSA_ACCOUNT_ID=''
IBKR_CASH_ACCOUNT_ID=''
IBKR_RRSP_ACCOUNT_ID=''
# Questrade now uses a rotating refresh token instead of the interactive OAuth
# flow, so QT_APP_CLIENT_ID / QT_CONSUMER_KEY / QT_REDIRECT_URI are no longer
# needed. Generate a refresh token once from the Questrade "My apps" page and
# paste it in when the script first asks; it is then rotated and stored for you.
# Optional: override where the refresh token is saved (defaults to
# qt_refresh_token.txt next to main.py).
# QT_REFRESH_TOKEN_PATH=''
# Optional: practice/sandbox accounts must use the practice login host.
# QT_TOKEN_URL='https://practicelogin.questrade.com/oauth2/token'
ACCOUNT_BALANCE_EXCEL_PATH_WINDOWS=''
ACCOUNT_BALANCE_EXCEL_PATH_MACOS=''