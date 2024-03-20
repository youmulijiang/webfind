import requests
def detect_web_server(domain):
    try:
        response = requests.head(f"http://{domain}", timeout=5)
        server_header = response.headers.get("Server")
        if server_header:
            return server_header.strip()
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError):
        pass

    return "UNKNOWN"

# print(detect_web_server("163.com"))


def response_banner(url):
    try:
        option_response = requests.options(url)
        if 'Allow' in option_response.headers:
            all_method = option_response.headers["Allow"]
            print(f"该网站支持的请求方法有{all_method}")
        head_response = requests.head(url)
        # print(head_response)
        server_header = head_response.headers.get('Server')
        if server_header:      
            print(f"该网站服务器使用的中间件是{server_header.lower()}")
            return server_header
    except:
        pass

    return "UNKNOWN"

response_banner("http://163.com")