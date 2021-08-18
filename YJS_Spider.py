from random import random
import requests.utils
from fake_useragent import UserAgent
from lxml import etree
from data_filter import filter_data,judge_exist
from get_session import run_get_session,reload_file
import time
import random
import urllib
import re
from tqdm import tqdm
from urllib.error import HTTPError

session = run_get_session()

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cache-contro': 'max-age=0',
        'referer': 'https://www.leshetu.com/other/yjs',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'
        # 'user-agent': UserAgent(use_cache_server=False).chrome
     }

def get_response():
    '''
        get index response
    '''
    for i in range(1, 3):
        target_url ="https://www.leshetu.com/tag/12/page/1"
        response_data = requests.get(target_url, headers=headers)
        parse_response(response_data)

def parse_response(response_data):
    '''
        parse url_list data
        return detail_list
    '''
    data = response_data.content.decode()
    with open('YJS.html','w') as f:
        f.write(data)
    xpath_data_ob = etree.HTML(data)
    xpath_data_list = xpath_data_ob.xpath('//div[@class="entry-media"]//a/@href')
    # print(xpath_data_list)
    get_content_response(session=session, data_list=xpath_data_list)


def get_content_response(session, data_list):
    '''
    get download url
    return detail_ulr, detail_title
    '''
    if data_list == []:
        print('empty list')
        return
    print('************************************')
    for i in data_list:
        time.sleep(random.randint(0,10))
        content_res = session.get(i, headers=headers).content.decode()
        try:
            xpath_data_list = etree.HTML(content_res)
            detail_url = xpath_data_list.xpath('//div[@class="pay-box"]/a[2]/@href')[0]
            detail_title = xpath_data_list.xpath("//h1/text()")[0]
            print(detail_title,detail_url)
            save_detail_data(detail_title=detail_title, detail_url=detail_url, session=session)
        except Exception as e:
            print('重载Cookie')
            if re.search('登录后购买', content_res).group():
                session = reload_file()
                return get_content_response(session,data_list)

def save_detail_data(detail_title, detail_url, session):
    '''
        save_file
    '''
    if judge_exist(detail_url):
        return 
    else:
        try:
            file_url_data= session.get(detail_url, headers=headers).content.decode()
            file_url =  re.search('https://.+\.zip', file_url_data).group()
            request_1 = urllib.request.Request(file_url,headers=headers)
            response2 = urllib.request.urlopen(request_1)
            print('開始下載')
            file_size = int(response2.headers.get('Content-Length'))  # 获取视频的总大小
            print(file_size)
            if (int(file_size)/1073741824)>1.5:
                print("大于1Gb")
                return
            pbar = tqdm(total=file_size)
            pbar.set_description('正在下载中......')
            with open('F:/LTS/'+detail_title+'.zip', 'wb',) as f:
                while True:
                    file_data = response2.read(1024)
                    if file_data:
                        f.write(file_data)           
                        pbar.update(1024)  # 更新进度条长度
                    else:
                        print('下載結束')
                        pbar.close()
                        filter_data(detail_url)
                        return
        except Exception as e:
            if isinstance(e, HTTPError):
                print(e)
                time.sleep(600)
                save_detail_data(detail_title, detail_url, session)


if __name__ == '__main__':
    get_response()

    print('######################################')
