# UpdateBalanceSheet
Python script that updates account balances utilizing APIs from various stock brokerages (Interactive Brokers, Questrade and Wealthsimple Trade)

# How To Run

1. Clone this repository
2. Copy `secrets.example.py` to `secrets.py` and fill in your own credentials. `secrets.py` is gitignored, so your credentials stay local. Each brokerage's required variables are listed in the sections below; optional settings (`ENABLE_WEALTHSIMPLE`, `QT_TOKEN_URL`, `QT_REFRESH_TOKEN_PATH`) are documented in `secrets.example.py`.


### Interactive Brokers API Setup
1. set the following env variables in secrets.py
- IBKR_TFSA_ACCOUNT_ID
- IBKR_CASH_ACCOUNT_ID
- IBKR_RRSP_ACCOUNT_ID
2. Download the [Interactive Brokers Client Portal Gateway](https://download2.interactivebrokers.com/portal/clientportal.gw.zip)
3. Install Java [Java Download](https://www.java.com/download/ie_manual.jsp)
4. Extract the clientportal.gw.zip into the root of the UpdateBalanceSheet directory
5. In the root of the UpdateBalanceSheet directory, create a python virtual environment venv and activate it
```
python -m venv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
```
6. run the following command from the clientportal.gw inside prompt/terminal of your choice (CMD, PowerShell):
```
bin\run.bat root\conf.yaml
```
7. Open https://localhost:5000 to login to your Interactive Brokers account Authorization the gateway proxy with your account credentials


### Questrade API Setup

Questrade uses a **rotating refresh token**: you authorize once, and on every run
the script exchanges its stored refresh token for a fresh access token (and a new
refresh token, which it saves). This reuses a single device authorization instead
of registering a new one each run.

1. Go to the Questrade **My apps** page and register a personal app (any redirect
   URI works — it is not used by this flow).
2. From that app, click **generate a new token** to obtain a **refresh token**.
   Do this **once** — each manual generation creates a new device authorization.
3. The first time you run the script it will prompt you to paste that refresh
   token. It is then saved to `qt_refresh_token.txt` (gitignored) and rotated
   automatically on every subsequent run — no further prompts.

> If you previously used the old interactive flow, you can safely delete the
> accumulated device authorizations from the Questrade **My apps** page; this
> flow keeps just one alive.
>
> Optional: set `QT_REFRESH_TOKEN_PATH` in `secrets.py` to store the token
> somewhere other than the default location next to `main.py`.
>
> Practice/sandbox accounts: set `QT_TOKEN_URL='https://practicelogin.questrade.com/oauth2/token'`
> in `secrets.py` (the default targets the live login host).


### Wealthsimple Trade API Setup
1. set the following env variables in secrets.py
2. if you use a 2fa code you will need to enter that upon fetching the data from the wsimple.api
- WEALTHSIMPLE_USERNAME
- WEALTHSIMPLE_PASSWORD
- WEALTHIMSPLE_RRSP_ACCOUNT_ID
- WEALTHIMSPLE_TFSA_ACCOUNT_ID

Wealthsimple fetching is **enabled by default**. If you don't use Wealthsimple,
set `ENABLE_WEALTHSIMPLE = False` in your `secrets.py` to skip it on that machine
(no need to touch `main.py` or maintain a separate branch).

### Running the script

The portable way to run it on any OS:

1. Start the IB Client Portal gateway and **log in / authenticate** it (see the Interactive Brokers section). `main.py` calls IB immediately with no auth wait, so the gateway must be authenticated *before* you run the script, or it will error out.
2. Activate your venv and run `python main.py`.

On the **first** run, Questrade prompts you to paste a refresh token (see the Questrade section above); it is saved to `qt_refresh_token.txt` and reused automatically afterward.

> The repo also ships the maintainer's personal launcher scripts. They **hard-code local paths** (repo location, gateway folder name, Windows username), so edit them to match your own environment before use:
> - `update_balance_sheet.sh` (macOS): opens the gateway in a new terminal, waits for you to authenticate at https://localhost:5001, then runs `main.py`.
> - `UpdateBalanceSheet.bat` (Windows): opens the gateway and `main.py` in separate windows. It does **not** wait for authentication, so make sure the gateway is logged in at https://localhost:5000 before `main.py` reaches it (simplest: just run `python main.py` yourself once the gateway is authenticated).

### This is an example of the spreadsheet i'm updating with this script

- Column A is the Account_Name
- Column B is the Account_Balance

![image](https://github.com/0xDario/UpdateBalanceSheet/assets/61662791/b3522b87-e75b-45d6-a738-c4b4a288e667)
