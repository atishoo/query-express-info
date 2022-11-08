import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import numpy as np
from selenium.webdriver.support.wait import WebDriverWait
from kuaidi100 import Kuaidi100,Kuaidi100State

def element_is_visible(browser):
    time.sleep(2)
    ele1 = browser.find_element(By.CSS_SELECTOR, '.op_express_delivery_errro_msg')
    result1 = ele1 is not None and ele1.is_displayed()
    ele2 = browser.find_element(By.CSS_SELECTOR, '.op_express_delivery_main')
    result2 = ele1 is not None and ele2.is_displayed()
    return result1 or result2


BAIDU = 'https://www.baidu.com/'

if __name__ == '__main__':
    express_result = []
    open("result.csv", 'w').close()
    # 载入待查询数据
    data = np.loadtxt('11-01-430.csv', dtype=str, delimiter=',', usecols=(0, 3, 4, 11, 12), skiprows=1)
    for i in data:
        kuaidi = Kuaidi100()
        result = kuaidi.setNum(i[4]).track()
        if result['message'] == 'ok':
            # 查询成功
            # 物流状态 Kuaidi100State[int(result['state'])]
            # 物流最新的一条信息 result['data'][0]['context']
            express_info = result['data'][0]['context']
            express_info = express_info.replace(',', '，')
            print('%s: [%s]%s' % (i[4], Kuaidi100State[int(result['state'])], express_info))
            express_result.append(','.join(i) + ',%s,%s'%(Kuaidi100State[int(result['state'])], express_info) + '\n')
        else:
            # 暂无物流
            express_result.append(','.join(i) + ',没有物流信息,注意📢注意📢注意📢\n')
            print('%s: 没有查询到物流' % (i[4], ))

    with open('result.csv', 'a') as file_for_result:
        for row in express_result:
            file_for_result.write(row)
    quit()
    # 打开浏览器
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    browser.get(BAIDU)
    # 清空结果文件内容
    open("result.csv", 'w').close()
    # 载入待查询数据
    data = np.loadtxt('11-05-187.csv', dtype=str, delimiter=',', usecols=(0, 3, 4, 11, 12), skiprows=1)
    for i in data:
        express_no = i[4]
        input = browser.find_element(By.ID, 'kw')
        input.clear()
        input.send_keys(express_no)
        browser.find_element(By.ID, 'su').click()

        result = WebDriverWait(browser, 30).until(element_is_visible)
        if result:
            no_express_msg = browser.find_element(By.CSS_SELECTOR, '.op_express_delivery_errro_msg').is_displayed()
            if not no_express_msg:
                express_elements = browser.find_elements(By.CSS_SELECTOR, '.op_express_delivery_timeline_box>li')
                if len(express_elements) == 1:
                    # 没有物流信息
                    express_info = express_elements[0].find_element(By.CSS_SELECTOR, '.op_express_delivery_timeline_info').text
                    express_info = express_info.replace(',', '，')
                    express_result.append(','.join(i) + ',物流信息仅有一条：' + express_info + '\n')
            else:
                # 没有物流信息
                err_text = browser.find_element(By.CSS_SELECTOR, '.op_express_delivery_errro_msg').text
                if err_text.find('暂未查到与您单号相关的物流信息') > 0:
                    express_result.append(','.join(i) + ',没有物流信息\n')
                else:
                    # 其他错误
                    print(','.join(i) + ',%s\n'%(err_text))
                    break

        time.sleep(2)

    with open('result.csv', 'a') as file_for_result:
        for row in express_result:
            file_for_result.write(row)

    browser.quit()


