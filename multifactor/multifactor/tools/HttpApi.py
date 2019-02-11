import requests
import logging
import json
import demjson


def httpGet(url):

    #知识图谱爬取
    # host = Config.FNZ_API_HOST
    # url = '{host}{path}'.format(**locals())
    print("httpGet\n"+url)
    headers = {}
    # headers['Cookie'] = 
    # 
    cookies ={
        'cid': "b46d81ed3b52ebfbdb13cc3be1d708a01540442908",
        "ComputerID": "b46d81ed3b52ebfbdb13cc3be1d708a01540442908",
        "vvvv": "1",
        "v": "AqbSmW5CweLB3JVG8Px5kvui8Rcrh-pBvMsepZBPkkmkE0iB-Bc6UYxbbrRj",
        "PHPSESSID": "624b5d09a60622a43811f99cfe876260"
    }
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    headers['Upgrade-Insecure-Requests'] = '1'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate, br'
    headers['Cache-Control'] = 'max-age=0'
    headers['Connection'] = 'keep-alive'
    headers['Host'] = 'www.iwencai.com'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    # headers['Referer'] = 'http://www.iwencai.com/diag/block-detail?pid=11666&codes=002415&codeType=stock&info=%7B%22view%22:%7B%22nolazy%22:1,%22parseArr%22:%7B%22_v%22:%22new%22,%22dateRange%22:[],%22staying%22:[],%22queryCompare%22:[],%22comparesOfIndex%22:[]%7D,%22asyncParams%22:%7B%22tid%22:137%7D%7D%7D'
    # http://www.iwencai.com/diag/block-detail?pid=11666&codes=002415&codeType=stock&info=%7B%22view%22:%7B%22nolazy%22:1,%22parseArr%22:%7B%22_v%22:%22new%22,%22dateRange%22:[],%22staying%22:[],%22queryCompare%22:[],%22comparesOfIndex%22:[]%7D,%22asyncParams%22:%7B%22tid%22:137%7D%7D%7D
    resp = requests.get(url, headers=headers,cookies=cookies,allow_redirects=False)
    try:
        resp = requests.get(url)
        print(resp.status_code)
        print(resp.url)
        print(str(resp.cookies.get_dict()))
        print("--------------")
        # c=requests.cookies.RequestsCookieJar()#利用RequestsCookieJar获取
        # c.set('cookie-name','cookie-value')
        # s.cookies.update(c)
        # print(s.cookies.get_dict())
        return resp.content
    except :
        print("error") 
        raise Exception("Invalid url!")
   


def httpGet2(url):

    #知识图谱爬取
    # host = Config.FNZ_API_HOST
    # url = '{host}{path}'.format(**locals())
    print("httpGet\n"+url)
    headers = {}
    cookies ={}
    # # headers['Cookie'] = 
    # # 
    # cookies ={
    #     'cid': "b46d81ed3b52ebfbdb13cc3be1d708a01540442908",
    #     "ComputerID": "b46d81ed3b52ebfbdb13cc3be1d708a01540442908",
    #     "vvvv": "1",
    #     "v": "AqbSmW5CweLB3JVG8Px5kvui8Rcrh-pBvMsepZBPkkmkE0iB-Bc6UYxbbrRj",
    #     "PHPSESSID": "624b5d09a60622a43811f99cfe876260"
    # }
    # headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    # http://www.iwencai.com/diag/block-detail?pid=11666&codes=002415&codeType=stock&info=%7B%22view%22:%7B%22nolazy%22:1,%22parseArr%22:%7B%22_v%22:%22new%22,%22dateRange%22:[],%22staying%22:[],%22queryCompare%22:[],%22comparesOfIndex%22:[]%7D,%22asyncParams%22:%7B%22tid%22:137%7D%7D%7D
    resp = requests.get(url, headers=headers,cookies=cookies,allow_redirects=False)
    try:
        resp = requests.get(url)
        # print(resp.status_code)
        # print(resp.url)
        # print(str(resp.cookies.get_dict()))
        # print("--------------")
        # c=requests.cookies.RequestsCookieJar()#利用RequestsCookieJar获取
        # c.set('cookie-name','cookie-value')
        # s.cookies.update(c)
        # print(s.cookies.get_dict())
        # return resp.content
        # j = resp.json
        #  return resp.json()
        # return json.load(resp.content.decode('gb2312').replace("'", "\""))
        # return resp.json()
        return demjson.decode(resp.text)
    except Exception as ex:
        print("error error:"+str(ex)+" ======="+url) 
        # raise Exception("Invalid url!")



def crawfin():
    content = httpGet2(u'http://emweb.securities.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?ctype=4&type=1&code=SZ000651')
    fn ="/data/test/10.htm"

    with open(fn, "w") as f:
        # f.write(content.decode("utf-8"))
        f.write(content)
        f.close()
    print("-------------------")
     

        
if __name__ == '__main__':
    #财务数据爬取
    crawfin()

