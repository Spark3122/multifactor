from sqlalchemy import create_engine
import pandas as pd 
from logic import value as valueHelper
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/finance')



def getStockScore(stockCode):
    # sql =  "select * from stockScore where code = "+stockCode
    # # result = engine.execute(sql,stockCode)
    # # data = result.fetchone() # 获取所有数据.
    # df = pd.read_sql_query(sql, engine)

    # jsn =df.to_json(orient='records')
    jsn = getStockScoreWithSta(stockCode)
    return  jsn

def getStockSta(stockCode,fields,needValueImg=True):
    sql =  "select * from stockScore where code = "+stockCode
    # result = engine.execute(sql,stockCode)
    # data = result.fetchone() # 获取所有数据.
    df = pd.read_sql_query(sql, engine)
    indname = df.at[0,'industry']
   #  import pdb;pdb.set_trace()
    if indname:
        gsql =  "select * from stockScore where industry = '"+indname+"'"
        gdf = pd.read_sql_query(gsql, engine)
        group = gdf[fields].groupby(gdf['industry']).quantile(0.5)
        columnNames = [f+"Median" for f in group.columns.values]
        group.columns =columnNames;
        group['industry']=group.index

        # jsn =df.to_json(orient='records')
        df = df.merge(group)

        if needValueImg:
            df["valueurl"] = ""
            df.ix[0,"valueurl"]=valueHelper.getValueImgUrlOrCreate(stockCode)
    return df

def getStockScoreWithSta(stockCode,fields=['pe','jqjzcsyl','kfjlrtbzz','ldbl','zzczzy','jyxjlyysr']):
    df = None
    if ";" not in stockCode:
        df = getStockSta(stockCode,fields)
    else :
        codes = stockCode.split(';')
        codes = [code for code in codes if code]
        if codes:
            df = getStockSta(codes[0],fields,False)
        for i,code in enumerate(codes):
            if i==0:
                continue
            curd = getStockSta(code,fields,False)
            df = pd.concat([df,curd])
           
    jsn =df.to_json(orient='records')
    return  jsn


def getIndustryStockScore(industry):
    sql =  "select * from stockScore where industry = '"+industry+"'"
    # result = engine.execute(sql,stockCode)
    # data = result.fetchone() # 获取所有数据.
    df = pd.read_sql_query(sql, engine)
    jsn =df.to_json(orient='records')
    return  jsn


def getAllIndustry():
    sql =  "select distinct(industry) from stockScore  "
    # result = engine.execute(sql,stockCode)
    # data = result.fetchone() # 获取所有数据.
    df = pd.read_sql_query(sql, engine)
    jsn =df.to_json(orient='records')
    return  jsn



if __name__ == "__main__":
    # code ="601229;"
    # ar =code.split(";")
    # print(ar)
    # ar = [code for code in ar if code]
    # print(ar)
    d = getStockScoreWithSta("601229")
    print(d)

    # d = getAllIndustry()
    # print(d)

    # d,i,g = getStockScoreWithSta("000651",['pe','jqjzcsyl','kfjlrtbzz','ldbl','zzczzy','jyxjlyysr'])
    # d = getIndustryStockScore("银行")
    # print(d)
    # import pdb;pdb.set_trace()
    # print(d.head(10))
