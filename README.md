# UpdateBalanceSheet
Python script that updates account balances utilizing APIs from various stock brokerages (Interactive Brokers, Questrade and Wealthsimple Trade)

# How To Run

1. Clone this repository
2. Copy the secrets.example.py and rename it to secrets.py, then populate the secrets.py with your usernames/passwords/url/filepaths
3. Open the project in terminal and run the following ```clientportal.gw\Bin\run.bat clientportal.gw\root\conf.yaml``` (this is only needed for the Interactive Brokers API as it utilizes a Client Gateway Proxy Application to connect to its API

## This is an example of the spreadsheet i'm updating with this script

- Column A is the Account_Name
- Column B is the Account_Balance

![image](https://github.com/0xDario/UpdateBalanceSheet/assets/61662791/b3522b87-e75b-45d6-a738-c4b4a288e667)

### Note: 
I'm using Interactive Brokers, Questrade and Wealthsimple Trade, if you aren't utilizing all these brokers you can comment out those function calls in the main() inside main.py
