import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv(r'data.csv', encoding='utf-8') #读取csv文件

df = df.drop_duplicates() # 数据清洗，去除重复数据

# 使内容转化为xlsx 结尾的excle格式
df.to_excel(r'data.xlsx', sheet_name='data')
ms_engine = create_engine("mysql+pymysql://root:root@localhost:3306/food")
df.to_sql('data', con=ms_engine, index=True)