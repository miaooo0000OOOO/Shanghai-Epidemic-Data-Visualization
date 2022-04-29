import requests
import time

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

with open("htmllist.txt") as file:
    urls = file.readlines()
    for i in range(len(urls)):
        urls[i] = urls[i].replace('\n', '')
        resq = requests.get(urls[i], headers=headers)
        assert resq.status_code==200
        with open("htmls/{}.html".format(i), "w", encoding="utf-8") as f:
            f.write(resq.text)
        time.sleep(3)