import re
import requests

text=requests.get("https://pss.bdstatic.com/r/www/cache/static/protocol/https/global/js/all_async_search_3dd8f20.js").text

a = re.findall(r'1(3|4|5|6|7|8|9)\d{9}',text)
if a:
    print(a)