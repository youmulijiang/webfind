import ast
import re
from prettytable import PrettyTable,PLAIN_COLUMNS,MSWORD_FRIENDLY
import requests
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from src.lib.colorprint  import create_clickable_link,cprint,Color
from pathlib import Path 
import csv
from pathlib import Path
import atexit

table = PrettyTable()

# table.custom_format
table.set_style(MSWORD_FRIENDLY)

with open(r"D:\开发系列\开发练习\安全开发1\webfind\config\regex_conf.txt","r",encoding="utf-8") as file:
    sensitive_regex_conf = file.read()
try:
    sensitive_regex:dict = ast.literal_eval(sensitive_regex_conf)
except:
    print("配置文件出错,请检查配置文件")
field_names = ["id","Info_name","Info_value","From_url"]
table.field_names = ["id","Info_name","Info_value","From_url"]
table.align["From_url"]="l"

id = 0
# save_path = fr'webfind\sensitive_save.csv'

file = open(r".\sensitive_find.csv","w+",newline='',encoding="utf-8",errors="ignore")
csv_file = csv.writer(file)
csv_file.writerow(["id","Info_name","Info_value","From_url"])
regex_value_list = []

class SensitiveFind():
    def text_sensitive_regex_find(self,text ,url):
        """ 在文本中找到敏感信息 """
        global id
        for sensitive_key,regex_value in sensitive_regex.items():
            for regex_value in re.finditer(regex_value,text):
                id+=1
                table.add_row([id,sensitive_key,regex_value.group(),url])
        
        return self

    def request_text_sensitive_regex_find(self,url,method="GET"):
        global id
        headers = {
            "User-Agent":UserAgent().random
        }

        try:
            response = requests.request(method=method,url=url,headers=headers)
            response.encoding = response.apparent_encoding
            response_text = response.text
            if response.status_code == 200:
                for sensitive_key,regex_value in sensitive_regex.items():
                    for regex_value in re.finditer(regex_value,response_text):
                        if regex_value.group() not in regex_value_list:
                            id+=1 
                            table.add_row([str(id),sensitive_key,regex_value.group() ,response.url])
                            regex_value_list.append(regex_value.group())
                        else:
                            continue
                        csv_file.writerow([str(id),sensitive_key,regex_value.group(),response.url])                         
                    
        except requests.ConnectionError as e:
            print("连接错误",e)
        
        return self

    def urllist_request_text_sensitive_find(self,url_list:list):
        with ThreadPoolExecutor(max_workers=100) as pool:
            for url in url_list:
                pool.submit(self.request_text_sensitive_regex_find(url))
        return self
    
    def doc_urllist_request_text_sensitive_find(self,url_list:list):
        with ThreadPoolExecutor(max_workers=100) as pool:
            for url in url_list:
                if Path(url).suffix in [".js",".ts",".txt",".xml"]:
                    pool.submit(self.request_text_sensitive_regex_find(url))
        return self
    
    @property
    def print_table(self):
        print(table)
        save_path = Path(r"output\sensitive_find.csv").absolute()
        cprint(f"爬取结果保存为{save_path}",style=Color.YELLOW)
        # file.close()

@atexit.register
def close_csv():
    file.close()



# if __name__ == "__main__":
#     url = "http://baidu.com" 
#     headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
#     url_list = ["http://baidu.com/ccc","http://163.com"]
#     text = requests.get(url="http://baidu.com",headers=headers).text

#     sfind = SensitiveFind()
#     sfind.urllist_request_text_sensitive_find(url_list).print_table
 
    