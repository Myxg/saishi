import pymysql
import requests
import json
import time
import calendar

t1 = time.localtime(time.time())
date = ''.join([str(int(t1.tm_mday)), '-', calendar.month_abbr[int(t1.tm_mon)], '-', str(t1.tm_year)])

url = 'https://creator.zoho.com.cn/api/json/saishi/view/form_BiSaiJieGuo_ShuangDa_Report?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Added_Time.After("' + date + '"))'
data = requests.get(url).text
data = data.replace(' ', '').split('=')[1][:-1]
data = json.loads(data)['form_BiSaiJieGuo_ShuangDa']

url1 = 'https://creator.zoho.com.cn/api/json/saishi/view/form_BiSaiJieGuo_ShuangDa_Report?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Modified_Time.After("' + date + '"))'
data1 = requests.get(url1).text
data1 = data1.replace(' ', '').split('=')[1][:-1]
data1 = json.loads(data1)['form_BiSaiJieGuo_ShuangDa']

data = data+data1
#
for i in data:
    fie = ['ID', 'Dropdown_BiSaiXiangMu', 'form_SaiShi', 'Dropdown_LunCi', 'Date_field_BiSaiRiQi', 'form_ShuangDaZuHe_A', 'form_ShuangDaZuHe_B1',
           'form_ShuangDaZuHe_ShengLi', 'Dropdown_BiSaiJieGuo', 'Single_Line_BiFen', 'form_ShiPin']
    val = [str(i['ID']), str('"'+i['Dropdown_BiSaiXiangMu']+'"'), str('"'+i['form_SaiShi']+'"'), str('"'+i['Dropdown_LunCi']+'"'),
           str('"'+i['Date_field_BiSaiRiQi']+'"'), str('"'+i['form_ShuangDaZuHe_A']+'"'), str('"'+i['form_ShuangDaZuHe_B1']+'"'), str('"'+i['form_ShuangDaZuHe_ShengLi']+'"'),
           str('"'+i['Dropdown_BiSaiJieGuo']+'"'), str('"'+i['Single_Line_BiFen']+'"'), str('"'+i['form_ShiPin']+'"')]

    db = pymysql.connect('video.hbang.com.cn', 'video', 'P@ssw0rd235', 'video')
    cursor = db.cursor()
    sql = "replace into form_BiSaiJieGuo_ShuangDa(" + ','.join(fie) + ") " + "values(" + ','.join(val) + ")"
    cursor.execute(sql)
    db.commit()
    db.rollback()
    db.close()
