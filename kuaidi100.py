import hashlib
import json
import requests

'''
"state": 
0->在途
1->揽件
2->疑难
3->签收
4->退件
5->派件
6->退回
'''
Kuaidi100State = ['在途', '揽件', '疑难', '签收', '退件', '派件', '退回']

class Kuaidi100():
    BASE_URL = 'http://poll.kuaidi100.com/poll/query.do'
    DETECT_CARRIER = 'http://www.kuaidi100.com/autonumber/auto?num=%s&key=%s'
    __param = {
        'com': '',  # 物流运营商
        'num': '',  # 物流单号
    }

    __post_data = {
        'customer': '',
        'sign': '',
        'param': ''
    }
    def __init__(self, customer = '', key = ''):
        self.__customer = customer
        self.__key = key
        self.__post_data['customer'] = customer

    def setNum(self, num):
        self.__param['num'] = num
        return self

    def track(self):
        self.__post_data['sign'] = hashlib.md5(bytes(json.dumps(self.__param, ensure_ascii=False) + self.__key + self.__customer, 'utf-8')).hexdigest().upper()
        self.__post_data['param'] = json.dumps(self.__param, ensure_ascii=False)
        response = requests.post(self.BASE_URL, data=self.__post_data)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return None

    def detect_carrier(self):
        response = requests.get(self.DETECT_CARRIER%(self.__param['num'], self.__key))
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return None
