"""
https://hattusa.org/ sitesinden tüm kitap listesi
"""
import os
import requests
from bs4 import BeautifulSoup

the_folder = os.path.dirname(os.path.abspath(__file__))

# 68 sayfalık kitap var
for i in range(1, 69):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0;"
               "Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"}
    with requests.get("https://hattusa.co/kitaplar?page=" + str(i),
                      headers=headers) as url:
        data = url.content
    soup = BeautifulSoup(data, features="html.parser")
    # kitaplar sitede list-group-item class'ında duruyor
    kitaplar = soup.find_all(class_="list-group-item")
    out = os.path.join(the_folder, "kitap.txt")
    # Her kitapta bulunan fazladan boşlukları ve \n karakteri düzeltelim
    for j in range(len(kitaplar)):
        kitap = kitaplar[j].contents[1].contents[0]
        yazarham1 = kitaplar[j].contents[3].contents[0].replace("  ", "")
        yazar = yazarham1.replace("\n", "@")
        # class'ı col-md-4 olanları "Son İndirilenler" vs. elemek için
        if kitaplar[j].contents[3].contents[0].parent.parent.parent.parent. \
                attrs["class"][0] != "col-md-4":
            with open(out, 'a', encoding='utf-8') as ff:
                print(kitap, yazar, file=ff)
    print("sayfa", i)
