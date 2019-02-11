import pymysql.cursors
# from tools import HttpApi
import json
import logging
import time
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='finance',
                             charset='utf8mb4')


import requests
# import logging
import json
import demjson

from selenium import webdriver
browser = webdriver.Chrome("/Users/admin/Desktop/soft/chromedriver")

def crawKForcode(code,filename):
    #知识图谱爬取
    print("-------------begin------"+code+" ---"+filename)
    url =u'https://www.iwencai.com/diag/block-detail?pid=11666&codes='+code+'&codeType=stock&info={"view":{"nolazy":1,"parseArr":{"_v":"new","dateRange":[],"staying":[],"queryCompare":[],"comparesOfIndex":[]},"asyncParams":{"tid":137}}}'
    browser.get(url)
    source = browser.page_source
    source = source.encode('utf-8').decode('unicode_escape')
    print(source)
    with open(filename, "w") as f:
        f.write(str(source))
        f.close()
    print("-------------end------")


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

def queryDStocks():
    try:
      with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT DISTINCT(code) FROM stocks ORDER BY code  asc"
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        return result
    finally:
        # connection.close()
        pass
        
if __name__ == '__main__':
    # stocks = queryStocks()
    stocks = queryDStocks()
    # ('000001', '平安银行'), ('000002', '万 科Ａ'))
    # print(stocks[0][0])

    codes = [] 
    for stockname in stocks:
        codes.append(stockname[0])
    
    print(len(codes))
    dir = "/data/knowledge/"

    count =0 
    for stockname in stocks:
        time.sleep(0.5)
        # crawFinance2Db(stockname[0])
        crawKForcode(stockname[0],dir+stockname[0]+".txt")
        count+=1
        logging.debug("-------------crawKnowledge2Db-end------------"+stockname[0]+" count:"+str(count))
        # if(count>=2):
        #     break
   
    print(codes)
    logging.debug("--------------end------------")