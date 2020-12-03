import pymysql
import requests
import json
import time
import calendar

t1 = time.localtime(time.time())
date = ''.join([str(int(t1.tm_mday)), '-', calendar.month_abbr[int(t1.tm_mon)], '-', str(t1.tm_year)])

url = 'https://creator.zoho.com.cn/api/json/saishi/view/form_SaiShi_Report?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Added_Time.After("' + date + '"))'
data = requests.get(url).text
data = data.replace(' ', '').split('1529=')[1][:-1]
data = json.loads(data)['form_SaiShi']

url1 = 'https://creator.zoho.com.cn/api/json/saishi/view/form_SaiShi_Report?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Modified_Time.After("' + date + '"))'
data1 = requests.get(url1).text
data1 = data1.replace(' ', '').split('=')[1][:-1]
data1 = json.loads(data1)['form_SaiShi']

data = data+data1
#
for i in data:
    fie = ['ID', 'Image_LOGO', 'Single_Line_SaiShiZhongWenMing', 'Single_Line_SaiShiYingWenMing', 'Dropdown_SaiShiJiBie', 'Date_field_KaiShiRiQi', 'Date_field_JieShuRiQi',
           'form_DiQu', 'form_DiQu_Single_Line_DiQu', 'Single_Line_ChengShi']
    val = [str(i['ID']), str('"'+''+'"'), str('"'+i['Single_Line_SaiShiZhongWenMing']+'"'), str('"'+i['Single_Line_SaiShiYingWenMing']+'"'), str('"'+i['Dropdown_SaiShiJiBie']+'"'),
                    str('"'+i['Date_field_KaiShiRiQi']+'"'), str('"'+i['Date_field_JieShuRiQi']+'"'), str('"'+i['form_DiQu']+'"'), str('"'+i['form_DiQu.Single_Line_DiQu']+'"'),
           str('"'+i['Single_Line_ChengShi']+'"')]

    db = pymysql.connect('video.hbang.com.cn', 'video', 'P@ssw0rd235', 'video')
    cursor = db.cursor()
    sql = "replace into form_SaiShi(" + ','.join(fie) + ") " + "values(" + ','.join(val) + ")"
    cursor.execute(sql)
    db.commit()
    db.rollback()
    db.close()
