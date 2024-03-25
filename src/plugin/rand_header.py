import random
import socket
import string
import struct
from pprint import pprint

from fake_useragent import UserAgent

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': "",
    'Referer': "",
    'X-Forwarded-For': "",
    'X-Real-IP': "",
    'Connection': 'keep-alive',
}

def get_ua()->dict:
    """ 返回随机请求头 """
    ua = UserAgent()
    key = random.randint(1,10)
    topsubname = ['.com', '.org', '.net', '.gov','.site','.store','.xyz']
    referer = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(int(key))])
    referer = 'www.' + referer.lower() + random.choice(topsubname)
    ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    HEADERS["User-Agent"] = ua.random
    HEADERS["Referer"] = referer
    HEADERS["X-Forwarded-For"] = HEADERS["X-Real-IP"] = ip

    return HEADERS


if __name__ == "__main__":
    
    get_ua()["cookies"] = "aaa"
    pprint(get_ua())
    # print("*"*100)
    # import requests
    # for i,v in (requests.get("https://www.baidu.com",headers=get_ua()).headers).items():
    #     print(i+":"+v)