import os
import sqlite3
import load_data

DATABASE_PATH = os.path.join(os.getcwd(), 'house.db')

conn = sqlite3.connect(DATABASE_PATH)

def init_db(conn=conn):
    """
    init_db 함수는 DB에 존재할 테이블을 초기화해주는 함수입니다.

    실행을 하게 되면 파라미터로 전해지는 conn 객체가 연결된 데이터베이스에서
    House, Dong_code, Sigungu_code 테이블이 존재하지 않는다면 새로 생성해줍니다.

    """
    # deal_date : year+month+day
    # location : 위치(법정동 시군구, 읍면종 코드)
    # detail_address : 상세 주소 ( 아파트, 몇 층)
    # area_width : 면적 넓이(제곱미터)
    create_table = """CREATE TABLE IF NOT EXISTS House (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        deal_amount INTEGER,
                        build_year INTEGER,
                        deal_date INTEGER,
                        sigungu_code INTEGER,
                        dong_code INTEGER,
                        detail_address VARCHAR(32),
                        floor INTEGER,
                        area_width INTEGER,
                        FOREIGN KEY (sigungu_code) REFERENCES Sigungu_code(id),
                        FOREIGN KEY (dong_code) REFERENCES Dong_code(id)
                        );"""
    # id는 9자리, 앞에 5자리는 남양주시를 나타낸다.
    create_table_Dong_code = """CREATE TABLE IF NOT EXISTS Dong_code (
                        id INTEGER NOT NULL,
                        do_name VARCHAR NOT NULL,
                        si_name VARCHAR NOT NULL,
                        eup_name VARCHAR NOT NULL,
                        lat REAL NOT NULL,
                        lot REAL NOT NULL,
                        PRIMARY KEY (id)
                        );""" # 따로 불러와야할듯 csv
    # deal_date : deal_month + dealday(계약년월일)
    # area_for_exclusive_use : 전용면적(㎡)

    cur = conn.cursor()

    cur.execute(create_table)
    cur.execute(create_table_Dong_code)

    cur.close()

def add_data(house_list, year_month, connection, cursor):
    if len(house_list) == 0 :
      return 0
    
    for data in house_list :
      try :
        deal_amount = data[0]
        build_year = data[2]
        deal_date = year_month*100 + int(data[19]) # year.month.day(8자리)
        sigungu_code = data[14]
        dong_code = data[15]
        detail_address = data[17]
        floor = data[25]
        area_width = data[21]
      except IndexError :
        continue

      insert_user = "INSERT INTO House (deal_amount,build_year,deal_date,sigungu_code,dong_code,detail_address,floor,area_width) VALUES (?, ?, ?,?,?,?,?,?)"
      cursor.execute(insert_user, (deal_amount, build_year, deal_date, sigungu_code, dong_code, detail_address, floor, area_width))
    data = cursor.fetchall()
    connection.commit()
    return data

# 월 증가(12월일 때 연도 추가 후 1월로 변경)
def add_month(ymd) :
  m = ymd%100
  if m == 12 :
    return (ymd+100) - 11 # 연도 더하고 1월로 변경
  return ymd + 1

init_db(conn)
cur = conn.cursor()
count = 1
sum_count = 0
page_num = 1
deal_ymd = 201512

tags, len_tag = [], []

while deal_ymd < 202112 :
  data, count, tags, len_tag = load_data.get_page(41360, deal_ymd, tags, len_tag)
  add_data(data, deal_ymd, conn, cur)
  print(deal_ymd, count)
  deal_ymd = add_month(deal_ymd)


conn.close()