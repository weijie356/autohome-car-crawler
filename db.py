import sqlite3

def save_to_db(cars):
    """把车系列表写入 SQLite 数据库。cars: [[车名, 价格, 车系ID], ...]"""
    # 打开数据库（文件不存在会自动创建——SQLite：单文件数据库）
    conn = sqlite3.connect("cars.db")
    cursor = conn.cursor()# 游标是传菜窗口：命令经它转达，不直接碰数据库

     # 建表（IF NOT EXISTS = 幂等：重复运行不炸，自动化脚本的及格线）
        # PRIMARY KEY 把"去重约束"写进结构，不靠程序自觉
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS series (
        series_id TEXT PRIMARY KEY,
        name TEXT,
        price TEXT
    )
""")
 
 # 逐条写入。? 占位符：永远假设数据是脏的，防 SQL 注入
    # OR REPLACE：撞主键就覆盖——去重交给数据库，借力打力
    for car in cars:
        cursor.execute(
                "INSERT OR REPLACE INTO series (series_id,name,price) VALUES (?,?,?)",
                (car[2],car[0],car[1])
            )
    

    conn.commit() # 盖章发货：一个事务打包确认，数据才真正落盘
    cursor.close() #先关抽屉
    conn.close() #再锁柜子：借来的资源必须还
    print("写入完成")


def show_first_5():
     """写入后必须验货：抽样查前5行，不拉全表（1007行会刷爆屏幕）"""
     conn =  sqlite3.connect("cars.db")
     cursor = conn.cursor()

     cursor.execute("SELECT * FROM series LIMIT 5")
     rows = cursor.fetchall()
     for row in rows:
        print(row)

     cursor.close()
     conn.close()







