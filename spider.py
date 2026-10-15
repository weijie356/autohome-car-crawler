import requests

url = "https://www.autohome.com.cn/grade/carhtml/B.html"
r = requests.get(url)

print(r.status_code)


with open("car.html","w",encoding = "utf-8") as f:
    f.write(r.text)

from bs4 import BeautifulSoup

html = open("car.html",encoding = "utf-8").read()
soup = BeautifulSoup(html,"html.parser")



dd = soup.find("dd")
print(dd.text[:300])
