# -*- coding: utf-8 -*-

# 导入必要模块
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import VARCHAR
import json as json
from pandas.core.frame import DataFrame
import json
import logging
import time
import pymysql.cursors
import os
# 初始化数据库连接，使用pymysql模块
# MySQL的用户：root, 密码:147369, 端口：3306,数据库：mydb
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/finance')

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='dai693122',
                             db='finance',
                             charset='utf8mb4')

from datetime import datetime

def loadMapNodeIdNames():
    try:
      with connection.cursor() as cursor:
        # Read a single record
        sql = "select _id,name from knowledgemap_node  ORDER BY id asc "
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        return result
    finally:
        # connection.close()
        pass

def loadMapRelaIdNames():
    try:
      with connection.cursor() as cursor:
        # Read a single record
        sql = "select _id,name from knowledgemap_relation  ORDER BY id asc "
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        return result
    finally:
        # connection.close()
        pass

import demjson,traceback
import re
               
def parse2DB():
    # "事件标题":""世界之手"推高中国物价 
    #bold = re.compile(r'([\u4e00-\u9fa5]+)"')
    # bold = re.compile(r'([\u4e00-\u9fa5]+|:")"(?![,}:])')
    bold = re.compile(r'([\u4e00-\u9fa5]+|:")"(?![,}]|:")')
    regex = re.compile(r'\\(?![/u"])')
    path = "/data/knowledge/"
    parents = os.listdir(path)
    ids = loadMapNodeIdNames()
    currentIdData = {}
    for nodeid in ids:
        currentIdData[nodeid[0]]=nodeid[1]

    
    relaS = loadMapRelaIdNames()
    currentRelaData = {}
    for rels in relaS:
        currentRelaData[rels[0]]=rels[1]


    for filename in parents:
        file_path = os.path.join(path,filename)
        #print("-----------------"+file_path)
        if file_path.endswith(".txt") == False:
            continue
        with open(file_path,'r') as f:
          
            configstr = f.read()
             #configstr = configstr.replace("\\x0","").replace("\\v","")
          
            configstr = regex.sub(r"\\\\", configstr)
            # \/\
            # configstr = deal_json_invaild(f.read())     
            s = configstr.find('>{"success')  
            e = configstr.find('}</pre>')  
            if s!=-1 and e!=-1 :
                configstr = configstr[s+1:e+1]
            else:
                print("not right content---")
                continue


            # print(configstr)
            # ldict = demjson.decode(configstr)
            
            # ldict = json.loads(json.dumps(eval(configstr)),strict=False)
            try:

                # print('Bold:', bold.sub(r'\1', text))
                configstr = bold.sub(r'\1', configstr)
                ldict = json.loads(configstr,strict=False)
            except Exception as e:
                 print("-----------------"+file_path)
                 print(traceback.print_exc())
                 continue

            #申万二级
            if 'data' not in ldict:
                print("not right farmat content---")
                continue
            datastr = ldict['data']['data']['result']['data'][0] 
            code = datastr['__code']
            nodes = datastr['nodes']
        

            now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            allDataNodes=[]
            for node in nodes:
                _id = node.get('_id',"")
                if _id in currentIdData:
                    continue

                node_domain = node.get('node_domain',"") 
                node_id = node.get('node_id',"") 
                node_name = node.get('node_name',"") 
                node_property = node.get('node_property',"")  
                expire_day_cnt = node.get('expire_day_cnt',"") 
                group = node.get('group',"") 
                allDataNodes.append(["wencai",_id,node_name,node_domain,node_id, str(expire_day_cnt),"","group",str(group),"indexdata",code,"","",now_time,now_time, str(node_property),str(node)]) 
                currentIdData[_id]=node_name

            if len(allDataNodes)>0:
                pdind = DataFrame(allDataNodes)
                pdind.columns=['familytype','_id',"name",'domain','node_id','expire_day_cnt',"desc",'field1name','field1value','field2name','field2value','field3name','field3value',"create_time","update_time","node_property",'original_data']
                # pdmean.to_sql('statistic2', engine)
                pdind.to_sql('knowledgemap_node',engine,if_exists='append')


            ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 解析所有的关系 ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 
            allEdgeNodes=[]
            edges = datastr['edges']
            for node in edges:
                _id = node.get('_id',"")
                if _id in currentRelaData:
                    continue
                 #_id 去重复
                relation_name = node.get('relation_name',"")
                from_node = node.get('from_node',"")   #对应node id
                from_label = node.get('from_label',"") 
                to_node = node.get('to_node',"") 
                to_label = node.get('to_label',"")  
                expire_day_cnt = node.get('expire_day_cnt',"") 
                score = node.get('score',"") 
                relation_property = node.get('relation_property',"") 
            
                glast_modify_timestr= node.get('last_modify_time',"") 
                update_time = glast_modify_timestr.get('$date',"") 

                expire_timestr= node.get('expire_time',"") 
                expire_time = expire_timestr.get('$date',"") 
                currentRelaData[_id]=relation_name
                allEdgeNodes.append(["wencai",_id,relation_name,"", relation_name,from_node,from_label,to_node,to_label, str(expire_day_cnt),str(score),"expire_time",expire_time,"indexdata",code,"","",now_time,update_time,str(relation_property),str(node)]) 
            
            if len(allEdgeNodes)>0:
                pdind = DataFrame(allEdgeNodes)
                pdind.columns=['familytype','_id',"name","desc","domain",'from_node','from_label','to_node',"to_label","expire_day_cnt","score",'field1name','field1value','field2name','field2value','field3name','field3value',"create_time","update_time","relation_property",'original_data']
                # pdmean.to_sql('statistic2', engine)
                pdind.to_sql('knowledgemap_relation',engine,if_exists='append')
       
def demo():
    #     d=  u"{\"node_name\":\"热门产\"品\"涨价\"}"
#     d = d.replace('[^:{},]\"',"")
#     d = d.replace('[\u4e00-\u9fa5]+\"',"")
        # import re
        # # bold = re.compile(r'([\u4e00-\u9fa5]+)"(?![,}])')
        # bold = re.compile(r'([\u4e00-\u9fa5]+|:")"(?![,}]|:")')
        # # ":
        # text = '{\"node_name\":\"热门产\"品\"涨价\",\"node_name2\":\"男单\"}'
        # print('Text:', text)
        # print('Bold:', bold.sub(r'\1', text))

        # text = u'"事件标题":""世界之手"推高中国物价 "'
        # print('Text:', text)
        # print('Bold:', bold.sub(r'\1', text))

        # text = u'"中国花生价格涨势"危险":花生油供不应求""'
        # print('Text:', text)
        # print('Bold:', bold.sub(r'\1', text))

        # text = u'"事件标题":"英媒称中国花生价格涨势"危险":花生油供不应求"}'  
        # print('Text:', text)
        # print('Bold:', bold.sub(r'\1', text))
    
#    #  "事件标题":"去年申城商品住宅价格涨了12% 购房者或"被中高端"","相关提示":"热门产品涨价  r'\*{2}(.*?)\*{2}
#     deal_json_invaild(d)
#     # ldict = json.loads(d,strict=False)
#     # m = eval(d)
#     m = ast.literal_eval(d,strict=False)
#     l = json.dumps()
    # ldict = json.loads(l)

if __name__ == '__main__':
        parse2DB()
