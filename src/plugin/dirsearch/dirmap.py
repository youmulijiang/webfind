import requests
from concurrent.futures import ThreadPoolExecutor,as_completed
from urllib.parse import urljoin
# import sys

# sys.path.append(r"D:\开发系列\开发练习\安全开发1\webfind\src") 
# from module.test import pinta

url_list = []
def read_url(raw_url,save_path)->list:
    with open(save_path,"r+") as dir_dict:
        for url_path in dir_dict.readlines(1208*4):
            full_url = urljoin(raw_url,url_path)
            url_list.append(full_url)
    return url_list


# print(read_url("http://baidu.com","D:\开发系列\开发练习\安全开发1\webfind\src\plugin\dirsearch\dirlist.txt"))
allow_status_code = ["200","302","403"]

def head_request(url,allow_status_code):
    line = "=" * 20 + ">"
    try:
        response = requests.head(url)
        response_code = response.status_code
        response_url = response.url
        # print("code:",response_code)
        if response_code in allow_status_code:
            if response_code == 302:
                return f"url:{url} {line} 重定向后的url:{response_url},状态码是{response_code}"
            return f"url:{url} {line} 状态码是{response_code}"
    except:
        pass


def dirsearch_run(raw_url,dict_path,allow_status_code=allow_status_code):
    url_list:list = read_url(raw_url,dict_path)
    # [head_request(url,allow_status_code=allow_status_code) for url in url_list]

    with ThreadPoolExecutor() as pool:
        futures = {pool.submit(head_request,url,allow_status_code) for url in url_list}
        for future in as_completed(futures):
            if future.result() != None:
                print(future.result())

# dirsearch_run("http://baidu.com")


