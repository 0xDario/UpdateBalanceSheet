import requests
from urllib.parse import urlparse
from decimal import Decimal
import secrets
import urllib3
import openpyxl
from wsimple.api import Wsimple

TWOPLACES = Decimal(10) ** -2

# hide non https ssl cert warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API endpoints
ib_api_url = "https://localhost:5000/v1/api"


def extract_access_token(url):
    fragment = urlparse(url).fragment
    token_parts = fragment.split("&")
    token_dict = {part.split("=")[0]: part.split("=")[1] for part in token_parts}
    access_token = token_dict.get("access_token")
    return access_token


def extract_api_server(url):
    fragment = urlparse(url).fragment
    token_parts = fragment.split("&")
    token_dict = {part.split("=")[0]: part.split("=")[1] for part in token_parts}
    api_server = token_dict.get("api_server")
    return api_server


def fetch_qt_portfolio_accounts(access_token, url):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(f"{url}v1/accounts", headers=headers, verify=False)
    return response.json()


def fetch_ib_portfolio_accounts():
    response = requests.get(f"{ib_api_url}/portfolio/accounts", verify=False)
    return response.json()

def fetch_interactive_brokers_data():
    try:
        print("Fetching Interactive Brokers account balances...\n")
        ib_portfolio_accounts = fetch_ib_portfolio_accounts()
        for account in ib_portfolio_accounts:
            data = requests.get(f"{ib_api_url}/portfolio/{account['accountId']}/allocation", verify=False).json()

            stk_value = data['assetClass']['long']['STK']
            cash_value = data['assetClass']['long']['CASH']

            # Calculate the formatted total
            total_value = stk_value + cash_value

            # Account description setup
            account_desc = account['desc']
            if account_desc == secrets.IBKR_CASH_ACCOUNT_ID:
                account_desc = 'IBKR (CASH)'
            if account_desc == secrets.IBKR_TFSA_ACCOUNT_ID:
                account_desc = 'IBKR (TFSA)'
            if account_desc == secrets.IBKR_RRSP_ACCOUNT_ID:
                account_desc = 'IBKR (RRSP)'

            # Call the update_spreadsheet function to update the spreadsheet
            update_spreadsheet(account_desc, total_value)
        print("Interactive Brokers account balances fetched and spreadsheet updated successfully!\n")
    except Exception as e:
        print("An error occurred:", e)


def fetch_questrade_data():
    try:
        print("Redirect the user to the authorization URL...\n")

        auth_params = {
            "response_type": "token",
            "client_id": secrets.QT_APP_CLIENT_ID,
            "redirect_uri": secrets.QT_REDIRECT_URI
        }

        auth_url = "https://login.questrade.com/oauth2/authorize"
        auth_response = requests.get(auth_url, params=auth_params)

        # Print the URL for user redirection
        print("Redirect the user to:", auth_response.url)

        # After the user is redirected back to the redirect_uri
        redirected_url = input("Enter the redirected URL after authorization: ")
        access_token = extract_access_token(redirected_url)
        qt_api_url = extract_api_server(redirected_url)
        if access_token:
            print("Authentication successful. Access token:", access_token)
            print("\nFetching Questrade account balances...\n")
            qt_portfolio_accounts = fetch_qt_portfolio_accounts(access_token, qt_api_url)
            for account in qt_portfolio_accounts['accounts']:
                account_number = account['number']
                headers = {
                    "Authorization": f"Bearer {access_token}"
                }
                data = requests.get(f"{qt_api_url}v1/accounts/{account_number}/balances", headers=headers,
                                    verify=False).json()
                account_desc = 'QT ('+account['type']+')'
                for record in data['combinedBalances']:
                    if record['currency'] == 'CAD':
                        # Call the update_spreadsheet function to update the spreadsheet
                        update_spreadsheet(account_desc, record['totalEquity'])
            print("Questrade account balances fetched and spreadsheet updated successfully!\n")
        else:
            print("Failed to obtain access token.")

    except Exception as e:
        print("An error occurred:", e)


def get_otp():
    return input("Enter OTP number: \n>>>")


def fetch_wealthsimple_trade_data():
    # use the credentials from the secrets.py file
    # check the current authentication tokens, use the auth.tokens API
    ws = Wsimple(secrets.WEALTHSIMPLE_USERNAME, secrets.WEALTHSIMPLE_PASSWORD, otp_callback=get_otp)

    # always check if Wealthsimple is working (return True if working or an error)
    positions = ws.get_positions()
    accounts = ws.get_accounts()

    positions = positions['results']
    accounts = accounts['results']
    rrsp_cash = 0.00
    tfsa_cash = 0.00

    for account in accounts:
        if account['id'] == secrets.WEALTHIMSPLE_RRSP_ACCOUNT_ID:
            rrsp_cash = Decimal(account['current_balance']['amount']).quantize(TWOPLACES)
        if account['id'] == secrets.WEALTHIMSPLE_TFSA_ACCOUNT_ID:
            tfsa_cash = Decimal(account['current_balance']['amount']).quantize(TWOPLACES)

    rrsp_positions = []
    tfsa_positions = []

    for position in positions:
        if position['account_id'] == secrets.WEALTHIMSPLE_RRSP_ACCOUNT_ID:
            rrsp_positions.append(int(position['quantity']) * Decimal(position['quote']['amount']))
        if position['account_id'] == secrets.WEALTHIMSPLE_TFSA_ACCOUNT_ID:
            tfsa_positions.append(int(position['quantity']) * Decimal(position['quote']['amount']))

    update_spreadsheet('WST (RRSP)', Decimal(sum(rrsp_positions)).quantize(TWOPLACES) + rrsp_cash)
    update_spreadsheet('WST (TFSA)', Decimal(sum(tfsa_positions)).quantize(TWOPLACES) + tfsa_cash)

    print("Wealthsimple Trade account balances fetched and spreadsheet updated successfully!\n")


def update_spreadsheet(account_desc, formatted_total):
    # Load the Excel spreadsheet
    spreadsheet_path = secrets.ACCOUNT_BALANCE_EXCEL_PATH
    workbook = openpyxl.load_workbook(spreadsheet_path)
    # Select the specific sheet by name
    sheet = workbook['Sheet1']

    # Find the matching account in the spreadsheet and update the adjacent cell
    for row_index, row in enumerate(sheet.iter_rows(min_row=2, max_col=sheet.max_column, values_only=True), start=2):
        for col_index, cell_value in enumerate(row):
            if cell_value == account_desc:
                adjacent_col_index = col_index + 2  # Get the column index immediately to the right

                # Update the cell in the adjacent column
                sheet.cell(row=row_index, column=adjacent_col_index, value=formatted_total)
                break

    # Save the updated spreadsheet
    workbook.save(spreadsheet_path)


# Main function
def main():
    try:
        fetch_questrade_data()
        fetch_interactive_brokers_data()
        fetch_wealthsimple_trade_data()
        print("All account balances fetched and spreadsheet updated successfully!\n")

    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    main()
