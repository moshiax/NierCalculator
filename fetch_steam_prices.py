import aiohttp
import asyncio
import json
import socket
import time

steam_app_id = '524220'
regions = ['US', 'UA', 'RU', 'PL', 'KZ', 'KR', 'BR', 'MX', 'IN', 'UY', 'KW', 'ZA', 'CR', 'CO', 'NO', 'CL', 'VN', 'TH', 'IL', 'SG', 'PE', 'EU', 'CH', 'JP', 'MY', 'PH', 'HK', 'GB', 'CA', 'TR']

def get_currency_symbol(currency_code):
    symbols = {
        'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥', 'RUB': '₽', 'UAH': '₴', 'BRL': 'R$', 'CAD': 'C$', 
        'AUD': 'A$', 'CHF': 'Fr', 'CNY': '¥', 'KRW': '₩', 'INR': '₹', 'MXN': 'Mex$', 'PLN': 'zł', 'ZAR': 'R',
        'TRY': '₺', 'AED': 'د.إ', 'THB': '฿', 'TWD': 'NT$', 'SAR': 'ر.س', 'QAR': 'ر.ق', 'KWD': 'د.ك',
        'KZT': '₸', 'MYR': 'RM', 'IDR': 'Rp', 'ILS': '₪', 'COP': '$', 'CRC': '₡', 'PEN': 'S/', 'PHP': '₱',
        'VND': '₫', 'CLP': '$', 'GEL': '₾', 'HRK': 'kn', 'HUF': 'Ft', 'LKR': 'Rs', 'MDL': 'L', 'NOK': 'kr',
        'RON': 'lei', 'SEK': 'kr', 'UGX': 'USh', 'MNT': '₮', 'TZS': 'TSh', 'NAD': '$', 'ZWL': '$',
        'BAM': 'KM', 'GHS': '₵', 'BND': '$', 'SBD': '$', 'MOP': 'MOP$', 'PGK': 'K'
    }
    return symbols.get(currency_code, currency_code)

async def fetch_region_price(session, region):
    url = f"https://store.steampowered.com/api/appdetails?appids={steam_app_id}&cc={region.lower()}&l=english&v=1"
    async with session.get(url) as response:
        data = await response.json()
        if data[str(steam_app_id)]['success'] and 'price_overview' in data[str(steam_app_id)]['data']:
            price_overview = data[str(steam_app_id)]['data']['price_overview']
            price = price_overview['final'] / 100
            currency_code = price_overview['currency']
            if region == 'EU':
                currency_code = 'EUR'
            currency_symbol = get_currency_symbol(currency_code)
            return {'region': region, 'price': price, 'currency_code': currency_code, 'currency_symbol': currency_symbol}
        return None

async def fetch_all_prices():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_region_price(session, region) for region in regions]
        results = await asyncio.gather(*tasks)
        return [result for result in results if result]

def connect(timeout=666):
    while True:
        try:
            socket.create_connection(("1.1.1.1", 53), timeout=timeout)
            return True
        except OSError:
            time.sleep(5)
            
async def main():
    connect()
    price_data = await fetch_all_prices()
    with open('price_standalone.json', 'w') as file:
        file.write('[\n')
        for i, item in enumerate(price_data):
            json_line = json.dumps(item, separators=(',', ':'))
            file.write(json_line)
            print(json_line)
            if i < len(price_data) - 1:
                file.write(',\n')
        file.write('\n]')

if __name__ == "__main__":
    asyncio.run(main())
