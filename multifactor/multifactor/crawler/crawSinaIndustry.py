# -*- coding: utf-8 -*-

# 导入必要模块
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import VARCHAR
import json as json
from pandas.core.frame import DataFrame
from tools import HttpApi
import json
import logging
import time
import pymysql.cursors

# 初始化数据库连接，使用pymysql模块
# MySQL的用户：root, 密码:147369, 端口：3306,数据库：mydb
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/finance')

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='dai693122',
                             db='finance',
                             charset='utf8mb4')

def makeTopNode(jnode,allNodes,industryName):
    curLevel=0
    for childNode in jnode:
        if(len(childNode)<=3):
            curCode ,curName = childNode[2],childNode[0]
            allNodes.append([curCode,curName,curLevel,"-1","-1", industryName]) 
        elif (len(childNode)==4):
            curCode ,curName = childNode[3],childNode[0]
            allNodes.append([curCode,curName,curLevel,"-1","-1", industryName]) 
            for childNode2 in childNode[1]:
                if(isinstance(childNode2,list) and len(childNode2)<=3):
                    allNodes.append([childNode2[2],childNode2[0],curLevel+1,curCode ,curName, industryName]) 
                    # makeNode(curCode,curName,childNode,curLevel+1,allNodes)

def  save2DB2():
    with open("/Users/admin/Desktop/doc/finance/multifactor/data/industry/sina_config_data.txt",'r') as f:
        configstr = f.read().replace("\\'", "'")
        ldict = json.loads(configstr)
        #申万二级
        ind =ldict[1][0][1][2][1]
        allNodes=[]
        # for ind2 in ind:
        #     ind3 = ind2[1]
        makeTopNode(ind,allNodes,"申万二级")
        data ={
            'indcode'
        }
        # print(ldict)
        pdind = DataFrame(allNodes)
        pdind.columns=['indcode','indname','level','par_indcode','par_indname','classname']
         # pdmean.to_sql('statistic2', engine)
        pdind.to_sql('industry',engine,if_exists='append')

def  save2DB():
    with open("/Users/admin/Desktop/doc/finance/multifactor/data/industry/sina_config_data.txt",'r') as f:
        configstr = f.read().replace("\\'", "'")
        ldict = json.loads(configstr)
        #申万二级
        ind =ldict[1][0][1][3][1]
        allNodes=[]
        # for ind2 in ind:
        #     ind3 = ind2[1]
        makeTopNode(ind,allNodes,"热门概念")
        data ={
            'indcode'
        }
        # print(ldict)
        pdind = DataFrame(allNodes)
        pdind.columns=['indcode','indname','level','par_indcode','par_indname','classname']
         # pdmean.to_sql('statistic2', engine)
        pdind.to_sql('industry',engine,if_exists='append')

    
import traceback
def insert(args):
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO stocks (code, name, industry, industry_code, pe) VALUES (%s, %s, %s, %s, %s)"       
            cursor.execute(sql, args)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    #except :
    except Exception as e:
        # ogging.error("error insert")  
        print(traceback.print_exc())
    finally:
        # connection.close()
        pass



def queryIndustrys():
    try:
      with connection.cursor() as cursor:
        # Read a single record
        sql = "select indcode,indname from industry  ORDER BY indcode asc "
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        return result
    finally:
        # connection.close()
        pass
    



def crawIndustry2DBForStock(indcode,indname):
    content = HttpApi.httpGet2(u'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=1000&sort=symbol&asc=1&node='+indcode+'&symbol=&_s_r_a=page')
    if(content is None):
        logging.error("null content:"+indcode)
        return 
    for data in content:
        line = [str(data[key]) for key in [ 'code', 'name']]
        line.append(indname)
        line.append(indcode)
        line.append("")
        insert(tuple(line))


def crawIndustryStocks2DB():
    stocks = queryIndustrys()
    # ('000001', '平安银行'), ('000002', '万 科Ａ'))
    # print(stocks[0][0])

    begin = False
    count =0 
    for ind in stocks:
        if(ind[0]=="chgn_730016"):
            begin = True
        if(begin==False):
            continue
        time.sleep(2)
        crawIndustry2DBForStock(ind[0],ind[1])
        count+=1
        logging.debug("-------------crawIndustryStocks2DB-end------------"+ind[0]+" count:"+str(count))
    
     
def main():
    # save2DB2()
    # crawIndustry2DBForStock("sw2_270100","test")
    crawIndustryStocks2DB()

if __name__ == '__main__':
    main()

