R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'  # white
Y = '\033[33m'  # yellow

from bs4 import BeautifulSoup
import requests
from colorama import init, Fore

def get_domain_historical_ip_address(domain):
    print("正在爬取中")
    try:
        url = f"https://viewdns.info/iphistory/?domain={domain}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",

        }
        response = requests.get(url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', {'border': '1'})

        if table:
            rows = table.find_all('tr')[2:]
            print(f"\n{Fore.GREEN}[+] {Fore.YELLOW}Historical IP Address Info from {C}Viewdns{Y} for {Fore.GREEN}{domain}:{W}")
            for row in rows:
                columns = row.find_all('td')
                ip_address = columns[0].text.strip()
                location = columns[1].text.strip()
                owner = columns[2].text.strip()
                last_seen = columns[3].text.strip()
                print(f"\n{R} [+] {C}IP Address: {R}{ip_address}{W}")
                print(f"{Y}  \u2514\u27A4 {C}Location: {G}{location}{W}")
                print(f"{Y}  \u2514\u27A4 {C}Owner: {G}{owner}{W}")
                print(f"{Y}  \u2514\u27A4 {C}Last Seen: {G}{last_seen}{W}")
        else:
            print("没有")
            None
    except ConnectionError as e:
        print(e)
        None

get_domain_historical_ip_address("baidu.com")

