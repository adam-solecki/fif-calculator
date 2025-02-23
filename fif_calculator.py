#!/usr/bin/env python3
import requests

# API endpoint for exchange rates with NZD as the base currency.
EXCHANGE_RATE_API_URL = "https://open.er-api.com/v6/latest/NZD"

def get_exchange_rates():
    """
    Fetch exchange rates with NZD as the base currency.
    Returns a dictionary of rates if successful, otherwise None.
    """
    try:
        response = requests.get(EXCHANGE_RATE_API_URL)
        data = response.json()
        if data.get("result") == "success":
            return data.get("rates", {})
        else:
            print("Error fetching exchange rates:", data.get("error-type"))
            return None
    except Exception as e:
        print("Exception occurred while fetching exchange rates:", e)
        return None

def convert_to_nzd(amount, currency, rates):
    """
    Convert the given amount from the specified currency to NZD.
    Since the API's base is NZD, the rate for a foreign currency indicates how many units of that currency one NZD buys.
    Therefore, conversion is done as: amount_in_NZD = amount / rate.
    """
    if currency.upper() == "NZD":
        return amount
    rate = rates.get(currency.upper())
    if rate is None:
        print(f"Exchange rate for {currency} not found. Skipping conversion.")
        return None
    return amount / rate

def main():
    print("Welcome to the FIF Calculator (Fair Dividend Rate Method)")
    print("---------------------------------------------------------\n")
    
    # Retrieve real-time exchange rates.
    rates = get_exchange_rates()
    if rates is None:
        print("Unable to retrieve exchange rates. Exiting.")
        return
    
    # Get portfolio data.
    try:
        num_investments = int(input("Enter the number of investments in your portfolio: "))
    except ValueError:
        print("Invalid input for number of investments. Exiting.")
        return

    total_market_value_nzd = 0.0
    investments = []
    
    for i in range(num_investments):
        print(f"\nInvestment #{i+1}:")
        name = input("Investment name: ")
        try:
            market_value = float(input("Market value: "))
        except ValueError:
            print("Invalid market value. Skipping this investment.")
            continue
        currency = input("Currency (e.g., USD, EUR, NZD): ")
        
        converted_value = convert_to_nzd(market_value, currency, rates)
        if converted_value is None:
            print("Conversion error encountered. Skipping this investment.")
            continue
        
        investments.append({
            "name": name,
            "market_value": market_value,
            "currency": currency.upper(),
            "market_value_nzd": converted_value
        })
        total_market_value_nzd += converted_value

    # Display portfolio summary.
    print("\nPortfolio Summary:")
    for inv in investments:
        print(f"{inv['name']} - {inv['market_value']} {inv['currency']} (converted: {inv['market_value_nzd']:.2f} NZD)")
    
    print(f"\nTotal Portfolio Market Value in NZD: {total_market_value_nzd:.2f}")
    
    # Calculate FIF taxable income (5% of the total market value).
    fif_taxable_income = total_market_value_nzd * 0.05
    print(f"FIF Taxable Income (5% of market value): {fif_taxable_income:.2f} NZD")
    
    try:
        marginal_tax_rate_input = input("Enter your marginal tax rate (as a percentage, e.g., 33 for 33%): ")
        marginal_tax_rate = float(marginal_tax_rate_input) / 100
    except ValueError:
        print("Invalid tax rate. Exiting.")
        return
    
    tax_liability = fif_taxable_income * marginal_tax_rate
    print(f"Your estimated tax liability at a {marginal_tax_rate*100:.2f}% tax rate is: {tax_liability:.2f} NZD")
    
if __name__ == "__main__":
    main()
