import requests
import db  # 自己写的模块：同文件夹的 db.py，文件名就是模块名

# ============================================================
# 阶段一：采集（开发期断网，暂不请求服务器）
# ============================================================

# url = "https://www.autohome.com.cn/grade/carhtml/B.html"
# r = requests.get(url)
# with open("car.html", "w", encoding="utf-8") as f:
#     f.write(r.text)

# ============================================================
# 阶段二：解析（从本地快照提取结构化数据）
# ============================================================

from bs4 import BeautifulSoup  # 解析工具：HTML 字符串织成结构树

html = open("car.html", encoding="utf-8").read()  # 只读快照，不碰服务器
soup = BeautifulSoup(html, "html.parser")

h4_list = soup.find_all("h4")  # 全页点名：每个 h4 里装一个车系

cars = []
for h4 in h4_list:
    a = h4.find("a")
    name = a.text                          # 车名：a 标签肚子里的文字

    series_id = a["href"].split("/")[3]    # 车系ID：藏在 href 属性里，切出来

    li = h4.parent                         # 价格不在 h4 里，回父级 li 找
    price_tag = li.find("a", class_="red") # 红字=有报价，灰字=停售
    if price_tag:
        price = price_tag.text
    else:
        price = "暂无"                     # 残缺是常态，优雅记录不硬编

    cars.append([name, price, series_id])

print(f"共提取 {len(cars)} 个车系")

# ============================================================
# 阶段三：存储（细节全在 db.py，主流程只留一行）
# ============================================================

db.save_to_db(cars)

# ============================================================
# 阶段四：验货（写入后必须验证）
# ============================================================

db.show_first_5()




















