import requests


#请求服务器
#url = "https://www.autohome.com.cn/grade/carhtml/B.html"
#r = requests.get(url)

#print(r.status_code)

#保存快照
#with open("car.html","w",encoding = "utf-8") as f:
#   f.write(r.text)

from bs4 import BeautifulSoup #解析工具：把HTML 字符串解析成结构树

#读取本地快照
html = open("car.html",encoding = "utf-8").read()

#织树，乱码变成可搜索的结构
soup = BeautifulSoup(html,"html.parser")


#找出 dd 标签
dd = soup.find("dd")
#print(dd.text[:300])

#点名：摘下全页所有 h4，每个h4里面有一个车系
h4_list  = soup.find_all("h4")
print(len(h4_list))



#逐个剥壳取车名，装进篮子
cars = []
for h4 in h4_list:
    #车名：h4里面的 a 标签
    a = h4.find("a")
    name = a.text # type: ignore

    #车系ID：藏在 href 网址里面，先取属性再切出来
    series_id = a["href"].split("/")[3] # type: ignore

    #价格：回到父级li，再找红字 a（class = "red" 才是报价，灰字是停售车）
    li = h4.parent
    price_tag = li.find("a",class_="red") # type: ignore
    if price_tag:
        price = price_tag.text
    else:
        price = "暂无"

    cars.append([name,price,series_id])

print(cars[:10])






import sqlite3 #依赖管理

# 文件已存在就打开数据库（文件不存在会自动创建，这就是，SQlite：单文件数据库
conn = sqlite3.connect("cars.db")#connect 建立连接，连接是稀有资源，所以文件末尾必须 close 归还
cursor = conn.cursor() #游标是传菜窗口，我不直接触碰数据库，依靠游标传递命令，换数据库不换套路

# 建表：车系档案表
#series_id是主键（PRIMARY KEY) = 数据库里的身份证，重复会冲突
#把约束写进结构中，用主键防止程序偷懒
cursor.execute("""
CREATE TABLE IF NOT EXISTS series (
     series_id TEXT PRIMARY KEY,
     name TEXT,
     price TEXT
)      
""")

#逐条写入
# ？ 占位符 = 永远假设数据是脏的
# INERT OR REPLACE = 借力打力。 好的工程师的标志：不是代码写的多，是知道那段逻辑该让系统替你写
for car in cars:
    cursor.execute(
        "INSERT OR REPLACE INTO series (series_id,name,price) VALUES (?,?,?)",
        (car[2],car[0],car[1])
    )


# commie = 盖章发货，保证事务完整性
conn.commit()

print("写入完成")


#查出来验货
#LIMI 5 是抽样检查
cursor.execute("SELECT * FROM series LIMIT 5")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.close()
























