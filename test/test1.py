import argparse
from gooey import Gooey

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("-o",help="指定输出位置")
    parse.add_argument("-u",const="aaa",help="指定网站",nargs="?",default="hello")
    global parses
    parses = parse.parse_args()

main()
print(parses._get_args())

if parses.u == "aaa":
    print("ok")
