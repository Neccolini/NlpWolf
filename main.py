import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
import numpy as np

vil_total_num = 2087
vil_current_num = 2
total_count = 0
vil_no = []
names = []
category = ['村No.', 'Name', '対話ログ']
dialogs = []


def setUpDriver():
    CHROMEDRIVER = './chromedriver.exe'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--disable-extensions")
    chrome_service = fs.Service(executable_path=CHROMEDRIVER)
    driver = webdriver.Chrome(service=chrome_service, options=options)

    return driver


def setUpDefaultLink():
    # https://ninjinix.x0.com/wolfg/index.rb?vid=1&meslog=000_ready
    # https://ninjinix.x0.com/wolfg/index.rb?vid=2&meslog=000_ready
    # https://ninjinix.x0.com/wolfg/index.rb?vid=3&meslog=000_ready

    link = 'https://ninjinix.x0.com/wolfg/index.rb?vid=2&meslog=000_ready&mode=say'

    return link


# 次の村に遷移
def toAnotherVillage(vil_current_num):
    vil_current_num += 1
    print('move to next village')
    link = 'http://ninjinix.x0.com/wolfg/index.rb?vid=' + str(vil_current_num) + '&meslog=000_ready&mode=say'

    return link


def incrementVillageNo(vil_current_num):
    vil_current_num += 1
    return vil_current_num


#
# //*[@id="all"]/div[2]/div[3]/a[2]
# //*[@id="all"]/div[2]/div[5]/a
# //*[@id="all"]/div[2]/div[7]/a
# //*[@id="all"]/div[2]/div[9]/a
# //*[@id="all"]/div[2]/div[183]/a
def getSmallTalk(driver, vil_current_num, total_count):
    counter = 0
    a_counter = 0
    name_index = 3
    announce_counter = driver.find_elements(By.CLASS_NAME, "announce")
    for item in announce_counter:
        a_counter +=1

    a_counter -= 2
    print(a_counter)

    while (counter < 30):  # 何番目の村までデータをとるかを選択

        Xpath = f"//*[@id='all']/div[2]/div[{name_index}]/a[2]"
        name_check = driver.find_elements(By.XPATH, Xpath)
        # print(Xpath)
        if (len(name_check) != 0):
            names.append(name_check[0].text)
            # print(name_check[0].text)
            name_check == []
            vil_no.append(vil_current_num)
            name_index += 1

        elif (a_counter != 0):
            name_index+=1
            a_counter-=1
            # print(a_counter)
        else:
            temp_comments = driver.find_elements(By.CLASS_NAME, "mes_say_body1")

            for item in temp_comments:
                dialogs.append(item.text)
                total_count +=1
                # print(item.text)
                # print('\n')

            # 次の村に遷移
            link = toAnotherVillage(vil_current_num)
            vil_current_num = incrementVillageNo(vil_current_num)
            driver.get(link)
            # print(vil_current_num)
            counter += 1
            name_index = 3
            announce_c = driver.find_elements(By.CLASS_NAME, "announce")
            a_counter = 0
            for item in announce_c:
                a_counter += 1

            # print(a_counter)
            a_counter -= 2

    return total_count



def add_dataframe(category, length, vil_no, name, dialog):

    df_t = pd.DataFrame(columns=category)

    for i in range(length):
        data_ = [[vil_no[i], name[i], dialog[i]]]
        df = pd.DataFrame(data = data_, columns=category)
        df_t = pd.concat([df_t, df], ignore_index=True, axis = 0)

    return df_t



def save_data_to(df):
    filename = './chitchat.xlsx'
    df.to_excel(filename, encoding='utf-8-sig')

def main():
    driver = setUpDriver()
    link = setUpDefaultLink()
    driver.get(link)
    total = getSmallTalk(driver, vil_current_num, total_count)
    print(total)
    save_data_to(add_dataframe(category, total, vil_no, names, dialogs))


    print('---Done!!!---')


    driver.stop_client()
    driver.close()


if __name__ == '__main__':
    main()
