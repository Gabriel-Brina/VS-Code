import requests

def get_btc_usd_rate():
    """
    Fetches the latest BTC/USD exchange rate from CoinGecko API.
    Returns the rate as a float.
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin',
        'vs_currencies': 'usd'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        rate = data['bitcoin']['usd']
        return rate
    except Exception as e:
        print(f"Error fetching BTC/USD rate: {e}")
        return None

if __name__ == "__main__":
    rate = get_btc_usd_rate()
    if rate is not None:
        print(f"Latest BTC/USD exchange rate: ${rate}")
    else:
        print("Failed to retrieve BTC/USD exchange rate.")