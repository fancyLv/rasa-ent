# -*- coding: utf-8 -*-
# @File  : third_ent.py
# @Author: LVFANGFANG
# @Date  : 2021/1/5 9:54 下午
# @Desc  :

import re
import urllib.parse

import requests

data_map = {
    'KnowledgePledge': '知识产权出质',
    'abnormal': '经营异常',
    'chattelmortgage': '动产抵押',
    'clearaccount': '清算组信息',
    'discredit': '失信被执行人',
    'equitypledge': '股权出质',
    'executedPerson': '被执行人',
    'filinginfo': '立案信息',
    'getCourtNoticeData': '法院公告',
    'illegal': '严重违法',
    'judicialauction': '司法拍卖',
    'lawWenshu': '裁判文书',
    'opennotice': '开庭公告',
    'penalties': '行政处罚',
    'restrictedConsumer': '限制高消费',
    'simplecancellation': '简易注销公告',
    'stockFreeze': '股权冻结',
    'taxviolation': '税务违法',
    'terminationcase': '终本案件'
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'aiqicha.baidu.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def get_basic_info(ent_name):
    """
    获取基本信息
    :param ent_name:
    :return:
    """
    url = 'https://aiqicha.baidu.com/s/l'
    params = {
        'q': ent_name,
        't': '',
        'p': 1,
        's': 10,
        'o': 0,
        'f': '{}'
    }
    headers_copy = headers.copy()
    headers_copy['Referer'] = f'https://aiqicha.baidu.com/s?q={urllib.parse.quote(ent_name)}&t=0'

    response = requests.get(url, params=params, headers=headers_copy)
    resultList = response.json()['data']['resultList']
    result = {}
    for item in resultList:
        entName = re.sub('<.*?>', '', item['entName'])
        if entName.replace('（','(').replace('）',')') == ent_name.replace('（','(').replace('）',')'):
            result = {
                'pid': item['pid'],
                '企业名称': entName,
                '经营状态': item['openStatus'],
                '法定代表人': item['titleLegal'],
                '注册资本': item['regCap'],
                '成立时间': item['validityFrom'],
                '地址': item['titleDomicile'],
                '经营范围': item['scope'],
                '更多信息': f'https://aiqicha.baidu.com/company_detail_{item["pid"]}?tab=basic'
            }
    return result


def get_hot_news(ent_name):
    """
    热点新闻
    :param ent_name:
    :return:
    """
    info = get_basic_info(ent_name)
    if info:
        pid = info['pid']
        url = f'https://aiqicha.baidu.com/yuqing/hotpotNewsAjax?pid={pid}'
        response = requests.get(url, headers=headers)
        news = response.json()['data']
        if news:
            news['link'] = 'https://aiqicha.baidu.com' + news['link']
    else:
        news = {}
    return news


def get_negative_info(ent_name):
    """
    负面信息
    :param ent_name:
    :return:
    """
    info = get_basic_info(ent_name)
    if info:
        pid = info['pid']
        url = f'https://aiqicha.baidu.com/detail/focalPointAjax?pid={pid}'
        response = requests.get(url, headers=headers)
        data = response.json()['data']
        result = {data_map[key]: data[key]['total'] for key in data if data[key]['total'] and data_map.get(key)}
        result['更多信息'] = f'https://aiqicha.baidu.com/company_detail_{pid}?tab=risk'
    else:
        result = {}
    return result


if __name__ == '__main__':
    print(get_hot_news('泉州德顺玻璃有限公司'))
