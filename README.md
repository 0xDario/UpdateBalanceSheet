# UpdateBalanceSheet
Python script that updates account balances utilizing APIs from various stock brokerages (Interactive Brokers, Questrade and Wealthsimple Trade)

# How To Run

1. Clone this repository


### Interactive Brokers API Setup
1. set the following env variables in secrets.py
- IBKR_TFSA_ACCOUNT_ID
- IBKR_CASH_ACCOUNT_ID
- IBKR_RRSP_ACCOUNT_ID
2. Download the [Interactive Brokers Client Portal Gateway](https://download2.interactivebrokers.com/portal/clientportal.gw.zip)
3. Extract the clientportal.gw.zip into the root of the UpdateBalanceSheet directory
4. In the root of the UpdateBalanceSheet directory, create a python virtual environment venv and activate it
```
python -m venv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
```
5. run the following command from the clientportal.gw inside prompt/terminal of your choice (CMD, PowerShell):
```
bin\run.bat root\conf.yaml
```
6. Open https://localhost:5000 to login to your Interactive Brokers account Authorization the gateway proxy with your account credentials


### Questrade API Setup
1. register the app in Questrade Apps
2. set the following env variables in secrets.py to match the REDIRECT_URI and CLIENT_ID set when registering the app
- QT_REDIRECT_URI
- QT_APP_CLIENT_ID


### Wealthsimple Trade API Setup
1. set the following env variables in secrets.py
2. if you use a 2fa code you will need to enter that upon fetching the data from the wsimple.api
- WEALTHSIMPLE_USERNAME
- WEALTHSIMPLE_PASSWORD
- WEALTHIMSPLE_RRSP_ACCOUNT_ID
- WEALTHIMSPLE_TFSA_ACCOUNT_ID

### This is an example of the spreadsheet i'm updating with this script

- Column A is the Account_Name
- Column B is the Account_Balance

![image](https://github.com/0xDario/UpdateBalanceSheet/assets/61662791/b3522b87-e75b-45d6-a738-c4b4a288e667)
