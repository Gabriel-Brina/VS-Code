import requests

def get_btc_usd_rate():
    """
    Fetches the latest BTC/USD exchange rate from the CoinGecko API.
    Returns the exchange rate as a float, or None if there was an error.
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        btc_usd = data.get("bitcoin", {}).get("usd")
        if btc_usd is not None:
            print(f"Latest BTC/USD rate: {btc_usd}")
            return btc_usd
        else:
            print("Could not retrieve BTC/USD rate.")
            return None
    except Exception as e:
        print(f"Error fetching BTC/USD rate: {e}")
        return None

if __name__ == "__main__":
    get_btc_usd_rate()