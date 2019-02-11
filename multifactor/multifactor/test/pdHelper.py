# -*- coding: utf-8 -*-

# 导入必要模块
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import VARCHAR

# 初始化数据库连接，使用pymysql模块
# MySQL的用户：root, 密码:147369, 端口：3306,数据库：mydb
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/finance')

# 查询语句，选出employee表中的所有数据
sql = '''
      select * from finance_rp ; 
      '''

# read_sql_query的两个参数: sql语句， 数据库连接
df = pd.read_sql_query(sql, engine)

df[['yyzsrtbzz','ldbl']] = df[['yyzsrtbzz','ldbl']].apply(pd.to_numeric)

pdmean = df.groupby('stock_code')["yyzsrtbzz","ldbl"].mean()
# pdmean.to_sql('statistic2', engine)
pdmean.to_sql('statistic3',engine,if_exists='replace',dtype={'stock_code':VARCHAR(pdmean.index.get_level_values('stock_code').str.len().max())})

import pdb;pdb.set_trace()
# 输出employee表的查询结果
# print(df)
# df.groupby('stock_code')["yyzsrtbzz"]

# 新建pandas中的DataFrame, 只有id,num两列
df = pd.DataFrame({'id':[1,2,3,4],'num':[12,34,56,89]})

# 将新建的DataFrame储存为MySQL中的数据表，不储存index列
df.to_sql('statistic', engine, index= False)

print('Read from and write to Mysql table successfully!')

