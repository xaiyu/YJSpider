

from random import random
import requests
from fake_useragent import UserAgent
from lxml import etree
from data_filter import filter_data
from demo import run_get_session
import time
import random
import re
import urllib
from tqdm import tqdm
import zipfile


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
        'user-agent' : UserAgent().chrome
    }

# def get_response():
#     '''
#         get index response
#     '''
#     target_url ="https://www.leshetu.com/tag/12/page/1"
#     response_data = requests.get(target_url, headers=headers)
#     return response_data

# def parse_response(response_data):
#     '''
#         parse response data
#     '''
#     data = response_data.content.decode()
#     with open('YJS.html','w') as f:
#         f.write(data)
#     xpath_data_ob = etree.HTML(data)
#     xpath_data_list = xpath_data_ob.xpath('//div[@class="entry-media"]//a/@href')
#     # print(xpath_data_list)
#     return xpath_data_list


# def get_content_response(session, data_list):
#     if data_list == []:
#         print('empty list')
#         return
#     print('************************************')
#     for i in data_list:
#         time.sleep(random.randint(0,10))
#         content_res = session.get(i ,headers=headers).content.decode()
#         xpath_data_list = etree.HTML(content_res)
#         detail_url = xpath_data_list.xpath('//div[@class="pay-box"]/a[2]/@href')[0]
#         detail_title = xpath_data_list.xpath("//h1/text()")[0]
#         print(detail_title,detail_url)
#         save_detail_data(detail_title,detail_url, session)
    
def save_detail_data(detail_title, detail_url, session):
    file_url_data= session.get(detail_url, headers=headers).content.decode()
    file_url =  re.search('https://.+\.zip', file_url_data).group()
    print(file_url)
    response_zip = requests.get(file_url, stream=True)
    file_size = response_zip.headers['content-length']
    print(file_size)
    if int(file_size)/1024/1024>100:
        print("大于100Mb")
        time.sleep(20)
        return
    pbar  = tqdm(total=int(file_size))
    print("开始下载")
    with open(detail_title+'.zip',  'wb') as f:
            for file_data in response_zip.iter_content(1024):
                if file_data:
                    f.write(file_data)
                    pbar.set_description('正在下载')
                    pbar.update(1024)
                else:
                    print('下载结束')
                    break
    pbar.close()

if __name__ == '__main__':
    # response_data = get_response()
    # parse_data = parse_response(response_data)
    session = run_get_session()
    detail_title = "小容仔咕咕咕w - NO.05 白T"
    detail_url = " https://www.leshetu.com/go?post_id=17713"
    print('######################################')
    save_detail_data(detail_title,detail_url, session)
    # detail_title,detail_url = get_content_response(session=session, data_list=parse_data)
