_A='price_overview'
import requests,json
steam_app_id='524220'
regions=['US','UA','RU','PL','KZ','KR','BR','MX','IN','UY','KW','ZA','CR','CO','NO','CL','VN','TH','IL','SG','PE','EU','CH','JP','MY','PH','HK','GB','CA','TR']
def get_currency_symbol(currency_code):A='$';symbols={'USD':A,'EUR':'€','GBP':'£','JPY':'¥','RUB':'₽','UAH':'₴','BRL':'R$','CAD':'C$','AUD':'A$','CHF':'Fr','CNY':'¥','KRW':'₩','INR':'₹','MXN':'Mex$','PLN':'zł','ZAR':'R','TRY':'₺','AED':'د.إ','THB':'฿','TWD':'NT$','SAR':'ر.س','QAR':'ر.ق','KWD':'د.ك','KZT':'₸','MYR':'RM','IDR':'Rp','ILS':'₪','COP':A,'CRC':'₡','PEN':'S/','PHP':'₱','VND':'₫','CLP':A,'GEL':'₾','HRK':'kn','HUF':'Ft','LKR':'Rs','MDL':'L','NOK':'kr','RON':'lei','SEK':'kr','UGX':'USh','MNT':'₮','TZS':'TSh','NAD':A,'ZWL':A,'BAM':'KM','GHS':'₵','BND':A,'SBD':A,'MOP':'MOP$','PGK':'K'};return symbols.get(currency_code,currency_code)
price_data=[]
for region in regions:
	url=f"https://store.steampowered.com/api/appdetails?appids={steam_app_id}&cc={region.lower()}&l=english&v=1";response=requests.get(url);data=response.json()
	if data[str(steam_app_id)]['success']and _A in data[str(steam_app_id)]['data']:
		price_overview=data[str(steam_app_id)]['data'][_A];price=price_overview['final']/100;currency_code=price_overview['currency']
		if region=='EU':currency_code='EUR'
		currency_symbol=get_currency_symbol(currency_code);item={'region':region,'price':price,'currency_code':currency_code,'currency_symbol':currency_symbol};price_data.append(item)
with open('price_standalone.json', 'w') as file:
    file.write('[\n')
    for i, item in enumerate(price_data):
        json_line = json.dumps(item, separators=(',', ':'))
        file.write(json_line)
        print(json_line)
        if i < len(price_data) - 1:
            file.write(',\n')
    file.write('\n]')
