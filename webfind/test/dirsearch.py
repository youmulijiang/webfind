import httpx
import asyncio
from urllib.parse import urljoin
import timeit
import requests
import os
from concurrent.futures import ThreadPoolExecutor,as_completed
from fake_useragent import UserAgent


url_path_list = []


path = "D:\安全系列\字典\Dirpath_List-master\Dirpath_List-master\dirb.txt"



def read_url(raw_url,dirlist_path:str=r"webfind\src\plugin\dirsearch\dirlist.txt")->list[str]:
    if os.path.exists(dirlist_path):
        with open(dirlist_path,"r") as dirlist:
            for line in dirlist.readlines(1208*3):
                url_path_list.append(line.strip())
            url_list = list(set(map(lambda x:urljoin(raw_url,x),url_path_list)))
            return url_list
    else:
        print("字典路径没有找到")
        raise FileExistsError

url_list = read_url(path)

async def AsyncDirsearch(url,method="HEAD"):
    async with httpx.AsyncClient() as Client:
        response = await Client.request(method=method,url=url)
        print(response.status_code)

def Dirsearch(url,method="HEAD"):
    header = {
        "User-Agent": UserAgent().random
    }
    print(url)
    response = requests.request(method=method,url=url,headers=header)
    # print(response.text)
    if response.status_code == 200:
        # return f"url:{response.url},status_code:{response.status_code}"
        return f"url: {response.url}, status_code: {response.status_code}"

dir_path = r"webfind\src\plugin\dirsearch\dirlist.txt"

def Dirsearch_run(raw_url,dir_path:str):
       with ThreadPoolExecutor() as pool:
        futures = {pool.submit(Dirsearch,url) for url in read_url(raw_url,dir_path)}
        for future in as_completed(futures):
            print(future.result())


if __name__ == "__main__":
    # with ThreadPoolExecutor() as pool:
    #     # futures:list[str] = pool.map(Dirsearch,url_list)
    #     futures = {pool.submit(Dirsearch,url) for url in url_list}
    #     for future in as_completed(futures):
    #         # print(future.result())
    #         # result = future.result()
    #         print(future.result())
    url = "http://163.com"

    Dirsearch_run(url,dir_path)
           

 

    