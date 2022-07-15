import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
import numpy as np


vil_total_num = 2087
vil_current_num = 1
dialog_day = 0
raw_log = []
names = []
co = []
category = ['村No.', 'Name', 'CO']


def setUpDriver():
    CHROMEDRIVER = './chromedriver.exe'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--disable-extensions")
    chrome_service = fs.Service(executable_path=CHROMEDRIVER)
    driver = webdriver.Chrome(service=chrome_service, options=options)

    return driver


def setUpDefaultLink():
    # https://ninjinix.x0.com/wolfg/index.rb?vid=1&meslog=000_party&mode=say
    # http://ninjinix.x0.com/wolfg/index.rb?vid=2&meslog=004_party&mode=say
    # http://ninjinix.x0.com/wolfg/index.rb?vid=3&meslog=006_party&mode=say
    # http://ninjinix.x0.com/wolfg/index.rb?vid=4&meslog=004_party&mode=say

    # //*[@id="all"]/div[2]/div[4]/div
    # //*[@id="all"]/div[2]/div[4]/div

    link = "https://ninjinix.x0.com/wolfg/index.rb?vid=1&meslog=000_party&mode=say"

    return link


def toNextDay(vil_current_num, dialog_day):
    link = 'http://ninjinix.x0.com/wolfg/index.rb?vid=' + str(vil_current_num) + '&meslog=00' + str(
        dialog_day) + '_party&mode=say'
    return link


# 次の村に遷移
def toAnotherVillage(vil_current_num):
    vil_current_num += 1
    dialog_day = 0
    print('move to next village')
    link = 'http://ninjinix.x0.com/wolfg/index.rb?vid=' + str(vil_current_num) + '&meslog=00' + str(
        dialog_day) + '_party&mode=say'
    return link


def incrementDialogDay(dialog_day):
    dialog_day += 1
    return dialog_day


def incrementVillageNo(vil_current_num):
    vil_current_num += 1
    return vil_current_num


def getRawText(driver, vil_current_num, dialog_day):
    counter = 0

    while (counter < 10): # 何番目の村までデータをとるかを選択

        try:
            temp = driver.find_element(By.XPATH, '//*[@id="all"]/div[2]/div[4]/div')
            # print('\n')
            # print(vil_current_num)
            #
            # print(temp.text)
            # print(link)
            # vil_no.append(vil_current_num)
            raw_log.append(temp.text)
            link = toAnotherVillage(vil_current_num)

            vil_current_num = incrementVillageNo(vil_current_num)
            dialog_day = 0
            driver.get(link)
            counter += 1

        except NoSuchElementException:
            print('move to next day')
            dialog_day = incrementDialogDay(dialog_day)
            link = toNextDay(vil_current_num, dialog_day)
            driver.get(link)

    return raw_log


def extractDataFromRaw(raw_log):
    village = 0
    raw_log_list = []
    # print(type(raw_log))
    # category = ['村No.', 'Name', 'CO']
    df_t = pd.DataFrame(columns=category)

    for item in raw_log:
        raw_log_list = item.split('\n')
        for raw in raw_log_list:
            vil_no = village + 1
            # temp = re.compile(r"[ぁ-んァ-ン 一-龥]", raw)
            result = re.match(r"(.*) （.*。(.*)だった。", raw)
            if result:
                name = result.group(1)
                role = result.group(2)
                print(name, role)
            data_= [[ vil_no, name, role]]
            df = pd.DataFrame(data=data_, columns=category)
            df_t = pd.concat([df_t, df], ignore_index=True, axis=0)

        village+=1

    return df_t


def save_to_csv(df):
    filename = './role_from_BBS.xlsx'
    df.to_excel(filename, encoding='utf-8-sig')



def mapping():
    main_data = pd.read_excel('./raw_data.xlsx')
    role_data = pd.read_excel('./role_from_BBS.xlsx')
    df1 = pd.DataFrame(main_data)
    df2 = pd.DataFrame(role_data)


    print(df1)

    print('\n')
    print('\n')

    df3 = pd.merge(df1, df2, on=['村No.', 'Name'])
    print(df3)


    df3.to_excel("Merged_1.xlsx", encoding='utf-8-sig', index=False)



def main():
    # driver = setUpDriver()
    # link = setUpDefaultLink()
    # driver.get(link)
    # raw_log = getRawText(driver, vil_current_num, dialog_day)
    # df=extractDataFromRaw(raw_log)
    #
    # save_to_csv(df)
    mapping()

    print('---Done!!!---')
    # driver.stop_client()
    # driver.close()


# ガター内の緑色のボタンを押すとスクリプトを実行します。
if __name__ == '__main__':
    main()
