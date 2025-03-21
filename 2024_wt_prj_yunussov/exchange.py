import httpx
from colorama import init, Fore, Style

init(True)

url = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date=13.02.2025"

try:
    response = httpx.get(url)
    response.raise_for_status()
    data = response.text
except httpx.HTTPStatusError as e:
    print(Fore.RED + f"Error downloading data: {e}")
    exit(1)

lines = data.split('\n')
exchange_rates = {}

for line in lines[2:]: # Skip headers
    parts = line.split('|')
    if len(parts) > 4:
        country = parts[0].strip()
        currency = parts[1].strip()
        amount = int(parts[2].strip())
        code = parts[3].strip()
        rate = float(parts[4].strip().replace(',', '.'))
        exchange_rates[code] = rate / amount

exchange_rates['CZK'] = 1.0

def convert(amount, from_currency, to_currency):
    if from_currency not in exchange_rates or to_currency not in exchange_rates:
        print(Fore.RED + "Invalid currency code")
        return None
    rate = exchange_rates[from_currency] / exchange_rates[to_currency]
    print(f"Rate: {rate}")
    return amount * rate

print(Fore.GREEN + "Welcome to the CNB exchange rate converter!")
while True:
    print(Style.BRIGHT + "\nAvailable currencies:\n", ', '.join(exchange_rates.keys()))
    from_currency = input("From currency (ex. EUR): ").upper()
    to_currency = input("To currency (ex. CZK): ").upper()
    amount_str = input("Amount to convert: ")

    try:
        amount = float(amount_str)
    except ValueError:
        print(Fore.RED + "Invalid amount. Please enter a number")
        continue

    result = convert(amount, from_currency, to_currency)
    if result is not None:
        print(Fore.YELLOW + f"{amount} {from_currency} = {result:.2f} {to_currency}")

    again = input("Continue? Y/N ").strip().lower()
    if again != 'y':
        print(Fore.BLUE + "Have a nice day!")
        exit(0)
