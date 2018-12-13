"""
https://hattusa.org/ sitesinden tüm kategori ve kitap listesi
"""
import mysql.connector
import requests
from bs4 import BeautifulSoup

# Sitede toplamda 29 sayfalık kategori var
for i in range(1, 30):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0;"
               "Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"}
    with requests.get("https://hattusa.org/kategoriler?page=" + str(i),
                      headers=headers) as url:
        data = url.content
    soup = BeautifulSoup(data, features="html.parser")
    # kategoriler sitede list-group-item class'ında duruyor
    kategoriler = soup.find_all("a", attrs="list-group-item")
    # Her kitapta bulunan fazladan boşlukları ve \n karakteri düzeltelim
    for j in range(len(kategoriler)):
        kategori = kategoriler[j].attrs["href"]  # Kategorinin linkini al
        # Birden çok kelimesi olanlara " tırnak ekle
        kategoriadi = "\"" + kategoriler[j].contents[1].contents[0] + "\""
        with requests.get(kategori, headers=headers) as url:
            data = url.content
        soup = BeautifulSoup(data, features="html.parser")
        # Kitap isimlerini al
        kitaplar = soup.find_all("h4", attrs="list-group-item-heading")
        for k in range(len(kitaplar)):
            # İçinde " ları eklerken hatayı engellemek için ' dönüştür
            kitap = "\"" + str(kitaplar[k].contents[0]).replace("\"", "'") + "\""
            try:
                cnx = mysql.connector.connect(
                    host='localhost', database='test1',
                    user='root', password='')
                cursor = cnx.cursor()
                query = "INSERT INTO kategoriler (kitap, kategori) VALUES (" + kitap + ", " + kategoriadi + ")"
                data_kitap = (kitap, kategoriadi)
                cursor.execute(query)
                cnx.commit()
            except mysql.connector.Error as error:
                cnx.rollback()  # rollback if any exception occured
                print("Tabloya ekleyemedi {}".format(error))
            finally:
                # bağlantıları kapatalım
                if(cnx.is_connected()):
                    cursor.close()
                    cnx.close()
    print("sayfa", i)
