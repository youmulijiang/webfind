import os
from colorprint import cprint,Color

os_columns = os.get_terminal_size().columns
def zone_print(color):
    def wapper(func):
        def inner_wapper(*arg):
            line = "*"*os_columns
            cprint(line,color)
            print("\n")
            func(*arg)
            print("\n")
            cprint(line,color)
        return inner_wapper
    return wapper

if __name__ == "__main__":
    @zone_print(Color.PURPLE)
    def world(s):
        print("hello",s)

    world("aaa")
