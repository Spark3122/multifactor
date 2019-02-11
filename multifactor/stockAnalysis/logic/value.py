# 计算股票的估值数据
# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randn
# import app as engine
import pandas as pd 
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/finance')



import os
import logging as logging
from gevent.pool import Pool
pool = Pool(10)

def value_for_code(code ):
    
    # 估值语句
    vsql = 'select * from value where secID ='+code

    # read_sql_query的两个参数: sql语句， 数据库连接
    vdf2 = pd.read_sql_query(vsql, engine)
    vdf = vdf2
   
    vdf =vdf.drop(['secID', 'f1',"PS","PCF"], axis=1)
    # vdf['date_formatted']=pd.to_datetime(vdf['tr÷adeDate'], format='%Y/%m/%d.')
    # vdf.set_index("date_formatted")
    vdf = vdf.set_index("tradeDate")
    vdf =  vdf.dropna()
    return vdf
#     vdf[0:5]

def percent(array):
#     print(type(array))
    return (array.values[-1]-array.min())/(array.max()-array.min())

def  rank_S(x):
    '''
    值越大，分越大
    '''
    r = x.rank(ascending=True,method='min')
    sz = x.count()
    s = r/sz
#     afters = np.where(s<=0.1 , 0 , np.where(s>=0.9 , 1 , s))
    return s.values[-1]

def lastValue(array):
#     print(type(array))
    return array.values[-1]

def values( ):
    vsql = " select * from value"
#     vsql = " select * from value where secID ='000651.XSHE' "
#     vsql = " select * from value  where  tradeDate >= '2008-01' "
    # read_sql_query的两个参数: sql语句， 数据库连接 where secID like '002466%' and tradeDate >= '2018'
    vdf = pd.read_sql_query(vsql, engine)
#     vdf = vdf2
    vdf[['PE', 'PB']]  = vdf[['PE', 'PB']].astype(float)
    group = vdf[['secID','PE', 'PB']].groupby("secID")
    
    # 返回pandas.core.frame.Series
#     mean =group['PE'].mean()
#     quantile =group['PE'].quantile(0.1)

    # 返回pandas.core.frame.DataFrame
    result = group[['PE']].agg(["mean","max","min",percent,lastValue,rank_S])
    result.columns=["pemean","pemax","pemin","percent","lastv","rankS"]
#     mean =group[['PE']].mean()
#     mean.columns=["pemean"]
    quantile =group[['PE']].quantile(0.1)
    quantile.columns=["pequan1"]
    quantile2 =group[['PE']].quantile(0.2)
    quantile2.columns=["pequan2"]
    quantile8 =group[['PE']].quantile(0.8)
    quantile8.columns=["pequan8"]
    quantile9 =group[['PE']].quantile(0.9)
    quantile9.columns=["pequan9"]
    result = result.join(quantile).join(quantile2).join(quantile8).join(quantile9)


    return result
#     return mean,quantile,mmax,mmin,perce,lastv
#     vdf[0:5]

def  plot(vdf,code,path="."):

    fig = plt.figure(); 
    vdf[['PE', 'PB']]  = vdf[['PE', 'PB']].astype(float)
    # vdf[['PE']]  = vdf[['PE']].astype(float)

    # print(vdf.quantile(.1))
    # 
    # print()

    s = vdf.mean()
    s10=vdf.quantile(.1)
    s20=vdf.quantile(.2)
    s80=vdf.quantile(.8)
    s90=vdf.quantile(.9)
    print(s)
    print(s10)
    print(s20)
    print(s90)
    data  = vdf
    # data.plot(figsize=(20,10))
    plt.figure() 
    ax1 = data.PE.plot(figsize=(20,10),style='r', x_compat=True,label="pe")
    # ax1.text(200,10,"PE")
    # ax1.set_xticks(data.index, x_compat=True)
    ax1.axhline(y=s.values[0], xmin=.05, xmax=0.95, ls='-', color='r', label="mean")
    ax1.axhline(y=s20.values[0], xmin=.05, xmax=.95, ls='--', color='r', label="20%")
    ax1.axhline(y=s10.values[0], xmin=.05, xmax=.95, ls='-.', color='r', label="10%")
    ax1.axhline(y=s80.values[0], xmin=.05, xmax=.95, ls=':', color='r', label="80%")
    ax1.axhline(y=s90.values[0], xmin=.05, xmax=.95, ls=':', color='m', label="90%")
    ax1.legend()
    ax1.set_ylabel('PE')

    ax2 = data.PB.plot(secondary_y=True, style='b' ,x_compat=True,label="pb") 
    ax2.axhline(y=s.values[1], xmin=.05, xmax=.95, ls='-', color='b')
    ax1.axhline(y=s20.values[1], xmin=.05, xmax=.95, ls='--', color='b')
    ax2.axhline(y=s10.values[1], xmin=.05, xmax=.95, ls='-.', color='b')
    ax2.axhline(y=s80.values[1], xmin=.05, xmax=.95, ls=':', color='b')
    ax2.axhline(y=s90.values[1], xmin=.05, xmax=.95, ls=':', color='b')
    ax2.legend()
    ax1.right_ax.set_ylabel('PB')

    # path,url = getValueImgUrl(code)
    logging.error("path:"+path)
    plt.savefig(path)
   
    # plt.show()
    # plt.close()
   
#格力

def  getValueImgUrl(code):
    url = "static/valueimage/"+code+".png"
    d = os.path.dirname(os.path.dirname(__file__))  #返回当前文件所在的目录    
    fn =os.path.join(d, url)
    return fn,"/"+url

def draw(t):
    try:
        code ,path = t[0],t[1]
        data =value_for_code(code)
        plot(data,code,path)
    except Exception  as e:
        logging.error("eror:"+path)
        logging.error(str(e))

def  getValueImgUrlOrCreate(code):
     path,url = getValueImgUrl(code)
     if not os.path.exists(path):
        logging.info("not exist:"+path)
        pool.map(draw,[(code,path)])
     return url



if __name__ == "__main__":
    code = '600056'
    # print(getValueImgUrl(code))
    # data =value_for_code(code)
    # plot(data,code)
    u = getValueImgUrlOrCreate(code)
    print(u)