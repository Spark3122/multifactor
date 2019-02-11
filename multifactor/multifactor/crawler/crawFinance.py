import pymysql.cursors
from tools import HttpApi
import json
import logging
import time
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='finance',
                             charset='utf8mb4')


def insert(args):
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO finance_rp (stock_code, date, jbmgsy, kfmgsy, xsmgsy, mgjzc,mggjj, mgwfply,mgjyxjl, yyzsr, mlr, gsjlr,kfjlr ,yyzsrtbzz, gsjlrtbzz, kfjlrtbzz,  yyzsrgdhbzz, gsjlrgdhbzz, kfjlrgdhbzz, jqjzcsyl, tbjzcsyl, tbzzcsyl, mll, jll, sjsl, yskyysr, xsxjlyysr, jyxjlyysr, zzczzy, yszkzzts, chzzts, zcfzl, ldzczfz, ldbl, sdbl) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
            cursor.execute(sql, args)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    except :
        logging.error("error insert")  
    finally:
        # connection.close()
        pass


def query(idarg):
    try:
      with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM 'finance_rp' WHERE 'id'=%s"
        cursor.execute(sql, (idarg,))
        result = cursor.fetchone()
        print(result)
    finally:
        connection.close()
        pass
    pass

def queryStocks():
    try:
      with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT code,name FROM stocks"
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        return result
    finally:
        # connection.close()
        pass
    

def crawFinance2DbYear(code):
    '''
    按年维度
    '''
    market = "SH"
    if int(code[0:1])<=3:
        market ="SZ"
    content = HttpApi.httpGet2(u'http://emweb.securities.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?ctype=4&type=1&code='+market+code)
    for data in content:
        line = [str(data[key]) for key in ['date', 'jbmgsy', 'kfmgsy', 'xsmgsy', 'mgjzc','mggjj', 'mgwfply','mgjyxjl', 
        'yyzsr', 'mlr', 'gsjlr', 'kfjlr' , 'yyzsrtbzz', 'gsjlrtbzz', 'kfjlrtbzz',  'yyzsrgdhbzz', 'gsjlrgdhbzz', 
        'kfjlrgdhbzz', 'jqjzcsyl', 'tbjzcsyl', 'tbzzcsyl', 'mll', 'jll', 'sjsl', 'yskyysr', 'xsxjlyysr', 'jyxjlyysr',
         'zzczzy', 'yszkzzts', 'chzzts', 'zcfzl', 'ldzczfz', 'ldbl', 'sdbl']]
        line.insert(0, str(code))
        insert(tuple(line))
    
def crawFinance2Db(code):
    '''
    按年维度
    '''
    market = "SH"
    if int(code[0:1])<=3:
        market ="SZ"
    content = HttpApi.httpGet2(u'http://emweb.securities.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?ctype=4&type=0&code='+market+code)
    for data in content:
        line = [str(data[key]) for key in ['date', 'jbmgsy', 'kfmgsy', 'xsmgsy', 'mgjzc','mggjj', 'mgwfply','mgjyxjl', 
        'yyzsr', 'mlr', 'gsjlr', 'kfjlr' , 'yyzsrtbzz', 'gsjlrtbzz', 'kfjlrtbzz',  'yyzsrgdhbzz', 'gsjlrgdhbzz', 
        'kfjlrgdhbzz', 'jqjzcsyl', 'tbjzcsyl', 'tbzzcsyl', 'mll', 'jll', 'sjsl', 'yskyysr', 'xsxjlyysr', 'jyxjlyysr',
         'zzczzy', 'yszkzzts', 'chzzts', 'zcfzl', 'ldzczfz', 'ldbl', 'sdbl']]
        line.insert(0, str(code))
        insert(tuple(line))

if __name__ == '__main__':
    # data =[str(i) for i in range(1,36)]
    # t =tuple(data)
    # import pdb; pdb.set_trace()
    # insert(t)
# 'stock_code', 
    # query(str(1))
   
    stocks = queryStocks()
    # ('000001', '平安银行'), ('000002', '万 科Ａ'))
    # print(stocks[0][0])

    codes = [] 
    for stockname in stocks:
        codes.append(stockname[0])
    


    count =0 
    for stockname in stocks:
        time.sleep(0.1)
        crawFinance2Db(stockname[0])
        count+=1
        logging.debug("-------------crawFinance2Db-end------------"+stockname[0]+" count:"+str(count))
   
    # code = "000651"  
    # crawFinance2Db(code)

    # code = "600339"  
    # crawFinance2Db(code)
    # connection.close()
    print(codes)
    logging.debug("--------------end------------")