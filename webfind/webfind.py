# ----------------------------  导入python库 ------------------------------------
try:
    import re
    import os
    import requests
    from urllib.parse import urljoin,urlparse
    from pathlib import Path
    from concurrent.futures import ThreadPoolExecutor
    import random
    import argparse
    from src.plugin.rand_header import get_ua
    from pprint import pprint
    from src.lib.signal_exit import ctrl_c_exit
    from src.lib.sensitive_regex_find import SensitiveFind
    import queue
    from src.lib.colorprint import zone_print,Color as zone_color
    from src.lib.pause import Pause

except ImportError as e:
    print(e)
    ok:str = str(input("是否下载第三方依赖(Yes/No):"))
    ok = ok.lower()
    if ok =="yes":
        os.chdir(Path(__file__).parent)
        os.system(r"pip install -r requirements.txt ")
    else:
        exit("缺少第三方依赖,程序无法正常运行,程序退出")

# -----------------------------  插件运行函数区域 --------------------------------
@zone_print(zone_color.PURPLE)    
def plugin_wapp_run():
    # terminal_columns = os.get_terminal_size().columns
    # print("\n"*2)
    # cprint("*"*terminal_columns,style=Color.PURPLE)
    print("分析到的指纹结果是")
    from src.plugin.finger.Wappalyzer import wappalyzer_main_analyze
    for i,b in (wappalyzer_main_analyze(url=url_scheme_check(args.url),headers=get_ua())).items():
        print(i,b)
    # cprint("*"*terminal_columns,style=Color.PURPLE)
    print("扫描结束")

@zone_print(zone_color.PURPLE)
def plug_dirsearch_run():
    print("开始目录扫描")
    from src.plugin.dirsearch.dirmap import dirsearch_run
    dirsearch_run(url_scheme_check(args.url),dict_path=args.dirmap_dict,allow_status_code=args.allow_status_code)

# ---------------------------- banner和命令行解析区域 ------------------------------
act_banner = """ 
  _     _                     _        __   _               _ 
 | |   (_)                   | |      / _| (_)             | |
 | |    _  __      __   ___  | |__   | |_   _   _ __     __| |
 | |   | | \ \ /\ / /  / _ \ | '_ \  |  _| | | | '_ \   / _` |
 | |   | |  \ V  V /  |  __/ | |_) | | |   | | | | | | | (_| |
 |_|   | |   \_/\_/    \___| |_.__/  |_|   |_| |_| |_|  \__,_|
      _/ |                                                    
     |__/   
"""

usage = """ 
 webfind [-h] [--version] -u URL [-j] [-v] [-c COOKIES] [-m METHOD] [-t THREADING] [-d] [-S]
               [-o {url,domain,file,all}] [-s SAVE_PATH] [--module MODULE] [--list-module LIST_MODULE]
               {wapp,dirmap} ...

例子:   python webfind.py -h 列出帮助
        python webfind.py -u http://www.baidu.com 该命令对网页进行基本探测
        python webfind.py -u http://www.baidu.com -d 该命令对网页进行深度探测
        python webfind.py -u http://www.baidu.com wapp 使用wappalyzer插件进行探测
"""

epilog = """ 
    version:0.1
 """

def main_parse():
    parse = argparse.ArgumentParser(prog="webfind")
    # parse.usage = usage
    parse.epilog = epilog

    parse.add_argument("--version",action="version",help="列出版本号",version="webfind version:0.01")
    find_group = parse.add_argument_group(description="对目标网站进行爬取")
    find_group.add_argument("-u","--url",dest="url",required=True,help="指定的url")
    find_group.add_argument("-j","--js",action="store_true",default=False,help="在js中探测信息")
    find_group.add_argument("-v",default=False,help="输出详细的信息",action="store_true")

    conf_group = parse.add_argument_group(description="爬取配置")
    conf_group.add_argument("-c","--cookies",type=str,help="指定cookies")
    conf_group.add_argument("-m","--method",default="GET",help="指定请求方法")
    conf_group.add_argument("-t","--threading",default=20,type=int,help="指定爬取线程数")
    conf_group.add_argument("-d","--depth",default=False,help="深度爬取",action="store_true")
    conf_group.add_argument("-S","--sfind",dest="sfind",action="store_true",help="敏感信息收集")

    save_group = parse.add_argument_group(description="保存结果")
    save_group.add_argument("-o",help="保存指定信息,保存结果为txt文件",choices=["url","domain","file","all"])
    save_group.add_argument("-s",dest="save_path",help="指定保存路径,默认保存在当前路径")

    # module_group = parse.add_argument_group(description="模块")
    # module_group.add_argument("--module",help="指定模块")
    # module_group.add_argument("--list-module",help="列出插件列表")

    sub_parse = parse.add_subparsers(title="插件系统",help="对网站进行指纹探测")
    wappalyzer = sub_parse.add_parser("wapp",help="使用Wapplyzer对网站指纹进行探测",add_help=False)
    dirmap = sub_parse.add_parser("dirmap",help="使用dirmap插件进行目录扫描")
    dirmap.add_argument("-w",dest="dirmap_dict",help="指定字典扫描",default=r"webfind\src\wordlist\dirlist.txt")
    dirmap.add_argument("-a",dest="allow_status_code",help="指定状态码",type=list)
    wappalyzer.set_defaults(func=plugin_wapp_run)
    dirmap.set_defaults(func=plug_dirsearch_run)

    global args
    args = parse.parse_args()

main_parse()
v = args.v
  


# ------------------------------ 功能函数区域 ---------------------------------------------
    
def print_banner():
    #\033[显示方式;前景色;背景色m + 结尾部分：\033[0m
    for i in act_banner:
        a = random.randint(30,37)
        print(f"\033[1;{a};13m"+i+"\033[0m",end="")
    
    print("version:0.1 ")
    #正式版发布!!!

print_banner()
terminal_columns:int = os.get_terminal_size().columns

url_re_pattern = r"""
    (?:"|')                               # Start newline delimiter
    (
    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
    |
    ((?:/|\.\./|\./)                    # Start with /,../,./
    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
    [^"'><,;|()]{1,})                   # Rest of the characters can't be
    |
    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
    [a-zA-Z0-9_\-/]{1,}                 # Resource name
    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
    (?:[\?|/][^"|']{0,}|))              # ? mark with parameters
    |
    ([a-zA-Z0-9_\-]{1,}                 # filename
    \.(?:php|asp|aspx|jsp|json|
            action|html|js|txt|xml|md)             # . + extension
    (?:\?[^"|']{0,}|))                  # ? mark with parameters
    )
    (?:"|')                               # End newline delimiter
"""

class ThreadPoolExecutorWithQueueSizeLimit(ThreadPoolExecutor):
    def __init__(self, maxsize=50, *args, **kwargs):
        super(ThreadPoolExecutorWithQueueSizeLimit, self).__init__(*args, **kwargs)
        self._work_queue = queue.Queue(maxsize=maxsize)

url_re = re.compile(url_re_pattern,re.VERBOSE)

spider_url_list = []
spider_domain_list = []
spider_file_list = []
spider_query_params_list = []
spider_js_file_list = []
depth_spider_domain_list = []
depth_spider_url_list = []

# ctrl_c_exit()


requests_header = get_ua() # 获取随机http头

if args.cookies:
    requests_header["cookies"] = args.cookies

def url_scheme_check(url: str)->str:
    if not url.startswith("http://") and not url.startswith("https://"):
        updated_url = "https://"+url
        return updated_url
    return url

def collect_url(url:str,method:str="GET",timeout=30):
    url = url_scheme_check(url)
    response = requests.request(method,url=url,stream=True,headers=requests_header,timeout=timeout)
    response.encoding = response.apparent_encoding
    if v:
        cprint(f"正在爬取{response.url},状态码是{response.status_code}")
    try:
        # response.raise_for_status()
        url_list = re.finditer(url_re,response.text)
        url_path = []
        path_list = [match.group().strip('"').strip("'") for match in url_list if match.group() not in url_path]
        domain_raw = response.url + "."
        url_list = list(map(lambda x:urljoin(domain_raw,x),path_list))
        domain_url_list = list(set(url_list))
        return domain_url_list
    except requests.ConnectionError as e:
        print(f"请求发生错误,url是{response.url}\t,状态码是{response.status_code}")
        print(e)
        pass
    
class Color:
    # 定义彩色字体
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[97m'

def cprint(text,style:Color=Color.WHITE,isstr:bool=False):
    """ 定义彩色输出函数 """
    if isstr:
        return style+text+"\033[0m"
    print(f"{style}{str(text)}\033[0m")

def create_clickable_link(url):
    """ 定义cmd跳转链接 """
    # return f"\033]8;;{url}\a{url}\033]8;;\a"
    return url

    
def find_last(string,str):
	positions = []
	last_position=-1
	while True:
		position = string.find(str,last_position+1)
		if position == -1:break
		last_position = position
		positions.append(position)
	return positions

def find_subdomain(urls, mainurl:str) ->list:
    """ 该函数能够匹配子域名 """
    if not mainurl.endswith("/"):
        mainurl = mainurl + "/"
    url_raw = urlparse(mainurl)
    domain = url_raw.netloc
    miandomain = domain
    positions = find_last(domain, ".")
    if len(positions) > 1:miandomain = domain[positions[-2] + 1:]
    subdomains = []
    for url in urls:
        suburl = urlparse(url)
        subdomain = suburl.netloc
        #print(subdomain)
        if subdomain.strip() == "": continue
        if miandomain in subdomain:
            if subdomain not in subdomains:
                subdomains.append(subdomain)
    return list(set(subdomains))
   
class UrlAnalyzer():
    """ 定义url分析器 """
    def __init__(self,raw_url:str,url_list:list) -> None:
        self._url_list:list = url_list
        self._raw_url:str = url_scheme_check(raw_url)
        pass

    def find_sub_domain(self)->list: 
        subdomain_list = find_subdomain(self._url_list,self._raw_url)

        
        return subdomain_list

    def find_js(self)->list:
        js_list = []
        for url_path in self._url_list:
            if Path(url_path).suffix == '.js':
                js_list.append(url_path)
        
        return list(set(js_list))

    def find_document(self)->list:
        file_extensions = [
    '.txt', '.csv', '.md',".woff2",
    '.zip', '.tar.gz', '.tgz', '.rar',
    '.mp4', '.avi', '.mov',
    '.mp3', '.wav', '.ogg',
    '.exe', '.app', '.sh',".apk",".eot",".git"
]
        document_list = []
        for url_path in self._url_list:
            # if Path(url_path).suffix != '' and Path(url_path).suffix != '.js':
            if Path(url_path).suffix in file_extensions:
                document_list.append(url_path)
                # spider_file_list.append(url_path)
        return list(set(document_list))
    
    def find_params(self)->list:
        for url_path in self._url_list:
            query = urlparse(url_path).query
            matches = re.findall(r'([^&=]+)=', query)
        return list(set(matches))
    
    def find_all(self)->dict[list]:
        all_find = {
            "sub_domain":self.find_sub_domain(),
            "js_list":self.find_js(),
            "document_list":self.find_document(),
            "find_params":self.find_params()
        }

        return all_find
    
        
def js_url_find(url):
    """ 定义js链接深度寻找函数 """
    url_list = []
    if Path(url).suffix in ["js","ts"]:
        url_list = collect_url(url,args.method)
        global v
        if v:
            if len(url_list) != 0:
                cprint(f"正在查找{url},该url有信息",Color.BLUE)
                # find = UrlAnalyzer(url,url_list).find_all() 
                # cprint(find,Color.DARKCYAN)
            else:
                cprint(f"{url}找不到信息",Color.RED)
    
    return url_list
    
def url_code_len(url):
    response = requests.get(url=url,headers=requests_header)
    # status_code = cprint(response.status_code,style=Color.YELLOW,isstr=True)
    # if 400 <=response.status_code < 500:
    #     status_code = cprint(response.status_code,isstr=True,style=Color.RED)
    # if 200 <= response.status_code < 300:
    #     status_code = cprint(response.status_code,isstr=True,style=Color.GREEN)
    url = cprint(response.url,Color.DARKCYAN,isstr=True)
    cprint(f"正在爬取{url}\t响应码是{response.status_code}\t长度是{len(response.content)}\n")


def depth_spider(url:list)->list:
    """ 定义深度爬取函数 """
    cprint(f"正在爬取{url}",Color.YELLOW)
    url_list = collect_url(url)
    analyzer = UrlAnalyzer(args.url,url_list)
    depth_spider_url_list.extend(url_list)
    subdoamin = analyzer.find_sub_domain()
    depth_spider_domain_list.extend(subdoamin)
    cprint(f"在{url}找到{len(url_list)}条url | 和{len(subdoamin)}条子域名")

def js_depth_find(url):
    url_list = collect_url(url,method=args.method)
    with ThreadPoolExecutorWithQueueSizeLimit(max_workers=args.threading) as pool:
            result = pool.map(js_url_find,url_list)
    for i in result:
        url_list.extend(i)
    url_list = list(set(url_list))
    return url_list

def response_banner(url):
    cprint("*"*terminal_columns,style=Color.PURPLE)
    print("\n")
    print("分析网站指纹的结果")
    try:
        # header = get_ua()
        option_response = requests.options(url_scheme_check(url),headers=get_ua())
        if 'Allow' in option_response.headers:
            all_method = option_response.headers["Allow"]
            cprint(f"该网站支持的请求方法有{all_method}",Color.DARKCYAN)
        head_response = requests.head(url_scheme_check(url),headers=get_ua())
        print(head_response.headers)
        server_header = head_response.headers.get('Server')
        if server_header:      
            cprint(f"该网站服务器使用的中间件是{server_header.lower()}")
    except:
        pass

    print("\n")
    cprint("*"*terminal_columns,style=Color.PURPLE)


class FileParse():
    """ 文件分析功能快上线啦 """
    def __init__(self,url_list:list,save_name,save_path=".") -> None:
        self.url_lsit = url_list
        self.save_path = save_path
        pass

    def file2csv(self):
        pass

    def file2txt(self):
        pass

    def file2md(self):
        pass

    def file2html(self):
        pass

if __name__ == "__main__":
    def start_main():
        cprint(f"正在爬取{url_scheme_check(args.url)}",Color.YELLOW)
        
        if args.js:
            url_list=js_depth_find(args.url)
        else:
            url_list = collect_url(args.url,args.method)


        if args.v:
            with ThreadPoolExecutor(max_workers=args.threading) as pool:
                    pool.map(url_code_len,url_list)

        if args.depth:
            with ThreadPoolExecutor(max_workers=args.threading) as pool:
                    pool.map(depth_spider,url_list)
                


        def main(url_list:list):
            print("\n")
            print(f"总共爬取{len(url_list)}条url") 
            for url in url_list:
                cprint(url,style=Color.BLUE)
            analyzer = UrlAnalyzer(args.url,url_list)
            print("\n")
            print(f"总共爬取{len(analyzer.find_sub_domain())}条子域名")
            for domain in analyzer.find_sub_domain():
                spider_domain_list.append(domain)
                cprint(domain,Color.BLUE)
            print("\n")
            print(f"总共爬取{len(analyzer.find_js())}个文件")
            for js_file in analyzer.find_js():
                spider_js_file_list.append(js_file)
                cprint(js_file,Color.BLUE)
            print("\n")
            print(f"总共爬取到{len(analyzer.find_document())}个文件")
            for file in analyzer.find_document():
                spider_file_list.append(file)
                cprint(file,Color.BLUE)


            # print("\n")
            # print(f"总共爬取到{len(analyzer.find_params())}个query_params参数")
            # for params in analyzer.find_params():
            #     spider_query_params_list.append(params)
            #     cprint(params,Color.BLUE)
            
        
        spider_url_list:list = url_list + depth_spider_url_list
        main(list(set(spider_url_list)))
        print("\n"*2)
        cprint("*"*terminal_columns,style=Color.PURPLE)
        print("\n"*2)
        print("总结汇报")
        cprint(f"共爬取到{len(spider_url_list)}条链接",Color.YELLOW)
        cprint(f"共爬取到{len(spider_domain_list)}条子域名",Color.YELLOW)
        cprint(f"共爬取到{len(spider_js_file_list)}条js链接",Color.YELLOW)
        cprint(f"共爬取到{len(spider_file_list)}个文件",Color.YELLOW)
        print("\n"*2)
        # cprint(f"共爬取到{len(spider_query_params_list)}个query_params参数",Color.YELLOW)
        

        def save_result():
            if os.path.isdir(args.o):
                args.o = args.o+"/"+"webfind-output"
                print(f"该路径是一个目录,已将文件保存在{args.o}中")
            if args.o == "url":
                save_path = f"{args.save_path}_url.txt"
                with open(f"{args.save_path}_url.txt","w+",encoding="utf-8") as file:
                    for url in spider_url_list:
                        file.write(f"{url}\n")
                print(f"已经将结果保存到{os.path.abspath(save_path)}")

            if args.o == "domain":
                save_path = f"{args.save_path}_domain.txt"
                with open(f"{args.save_path}_domain.txt","w+") as file:
                    for domain in spider_domain_list:
                        file.write(f"{domain}\n")

                path = os.path.abspath(save_path)
                print(f"已经将结果保存到{path}")

            if args.o == "file":
                save_path = f"{args.save_path}_file.txt"
                with open(f"{args.save_path}_file.txt","w+") as file:
                    for document in spider_file_list:
                        file.write(f"{document}\n")
                print(f"已经将结果保存到{os.path.abspath(save_path)}")

            if args.o == "all":
                save_path = f"{args.save_path}_all.txt"
                with open(f"{args.save_path}_all.txt","w+") as file:
                    file.write(f"收集到的url\n")
                    for url in spider_url_list:
                        file.write(f"{url}\n")
                    file.write("\n"*3)
                    file.write(f"收集到的子域名有")
                    for domain in spider_domain_list:
                        file.write(f"{domain}\n")
                    file.write("\n"*3)
                    file.write(f"收集到的文件有")
                    for document in spider_file_list:
                        file.write(f"{document}\n")
                print(f"已经将结果保存到{os.path.abspath(save_path)}")
            else:
                return
        if args.o:
            save_result()
        
        if args.sfind:
            print("\n"*2)
            cprint("*"*terminal_columns,Color.PURPLE)
            cprint("正在探测js文件是否存在敏感信息")
            sfind = SensitiveFind()
            sfind.doc_urllist_request_text_sensitive_find(spider_url_list).print_table
            print("\n"*2)
            cprint("*"*terminal_columns,Color.PURPLE)
            

        if hasattr(args,"func"):
            args.func()
    
    try:
        start_main()
        # response_banner(args.url)
    except KeyboardInterrupt as e:
        # Pause().pause()
        # exit("程序退出")
        cprint("程序已经手动退出",style=Color.RED)
        os._exit(1)



    
    




