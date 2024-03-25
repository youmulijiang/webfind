import csv

with open(r'D:\开发系列\开发练习\安全开发1\webfind\test\test.csv', 'w', newline='') as csvfile:
    file = csv.writer(csvfile)
    file.writerow(["h","a","b","c"])
    # fieldnames = ['first_name', 'last_name']
    # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # writer.writeheader()
    # writer.writerow({'first_name': ['Baked',"aaaa"], 'last_name': 'Beans'})
    # writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    # writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})