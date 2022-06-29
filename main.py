import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from styleframe import StyleFrame, Styler, utils
# Excelの保存最適化の為のライブラリー未使用


# chrome driver link : Chromeのバージョンに合わせてインストールが必要
# https://sites.google.com/chromium.org/driver/downloads
CHROMEDRIVER = './chromedriver.exe'
options = webdriver.ChromeOptions()

# 人狼BBSの対話ログは村ごとにログが蓄積してあるが為、村のURLを順に回る、その際対話ログは日にちごとに違うため、Dayを変えつつクローリングを続ける

vil_total_num = 2087
vil_current_num = 1
dialog_status = ['ready', 'progress']
dialog_day = 0
dialog_mode = ['say', 'whisper', 'groan']
category = ['村No.', 'Day', 'Name', '対話ログ']
vil_no = []
names = []
days = []
dialogs = []
total_count = 0
link = 'http://ninjinix.x0.com/wolfg/index.rb?vid=' + str(vil_current_num) + '&meslog=00' + str(
    dialog_day) + '_progress&mode=say'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--disable-extensions")
chrome_service = fs.Service(executable_path=CHROMEDRIVER)
driver = webdriver.Chrome(service=chrome_service, options=options)
driver.get(link) # 村１の1日目のリンクから
time.sleep(1)




def incrementDialogDay(dialog_day):
    dialog_day += 1
    return dialog_day




def incrementVillageNo(vil_current_num):
    vil_current_num += 1
    return vil_current_num

# 次の日のページに遷移
def toNextDay(vil_current_num, dialog_day):
    link = 'http://ninjinix.x0.com/wolfg/index.rb?vid=' + str(vil_current_num) + '&meslog=00' + str(
        dialog_day) + '_progress&mode=say'
    return link

# 次の村に遷移
def toAnotherVillage(vil_current_num):
    vil_current_num += 1
    dialog_day = 0
    link = 'http://ninjinix.x0.com/wolfg/index.rb?vid=' + str(vil_current_num) + '&meslog=00' + str(
        dialog_day) + '_progress&mode=say'
    return link


def add_dataframe(category, length, vil_no, day, name, dialog):

    df = pd.DataFrame(columns=category)

    for i in range(length):
        df = df.append({
            '村No.': vil_no[i],
            'Day': day[i],
            'Name': name[i],
            '対話ログ': dialog[i],
        }, ignore_index=True)


    return df


def save_data_to(df):

    filename = './Dialog_Data_From_BBS.xlsx'
    df.to_excel(filename, encoding='utf-8-sig')


# Crawling start...
i = 3
print(link)
while (True):
    try:
        isMessage = driver.find_element(By.XPATH, '//*[@id="all"]/div[2]/div[1]/div')
    except NoSuchElementException:

        if (vil_current_num < 4): # 何番目の村までデータをとるかを選択
            print('move to next village')
            dialog_day = 0
            link = toAnotherVillage(vil_current_num)
            vil_current_num = incrementVillageNo(vil_current_num)
            driver.get(link)
            i = 3
            print(link)
            isMessage = driver.find_element(By.XPATH, '//*[@id="all"]/div[2]/div[1]/div')
        else:
            break

    if (isMessage.is_displayed()):

        # time.sleep(1)
        # print(i)
        Xpath = f"//*[@id='all']/div[2]/div[{i}]/a[2]"
        temp = driver.find_elements(By.XPATH, Xpath)
        # print(Xpath)

        if (len(temp) != 0):
            names.append(temp[0].text)
            # print(temp[0].text)
            temp == []
            days.append(dialog_day + 1)
            vil_no.append(vil_current_num)
            i += 1

        else:
            temp_comments = driver.find_elements(By.CLASS_NAME, "mes_say_body1")

            for item in temp_comments:
                dialogs.append(item.text)
                # print(item.text)
                # print('\n')
            # 次の日に遷移
            dialog_day = incrementDialogDay(dialog_day)
            link = toNextDay(vil_current_num, dialog_day)
            i = 4
            driver.get(link)
            # print(link)

print(len(dialogs))
print(len(names))
print(len(days))
print(len(vil_no))

total_count = len(dialogs)

# def add_dataframe(category, length, vil_no, day, name, dialog):
save_data_to(add_dataframe(category, total_count, vil_no, days, names, dialogs))


# //*[@id='all']/div[2]/div[3]/a[2]
# //*[@id="all"]/div[2]/div[4]/a[2]
# //*[@id="all"]/div[2]/div[5]/a[2]
# //*[@id="all"]/div[2]/div[6]/a[2]
# //*[@id="all"]/div[2]/div[207]/a[2]
# //*[@id="all"]/div[2]/div[4]/a[2]
# //*[@id="all"]/div[2]/div[5]/a[2]



def main():
    print('---Done!!!---')
    driver.stop_client()
    driver.close()


if __name__ == '__main__':
    main()
