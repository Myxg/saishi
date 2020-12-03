import pymysql
import requests
import json
import time
import calendar

t1 = time.localtime(time.time())
date = ''.join([str(int(t1.tm_mday)), '-', calendar.month_abbr[int(t1.tm_mon)], '-', str(t1.tm_year)])

url = 'https://creator.zoho.com.cn/api/json/saishi/view/form_ShuangDaZuHePaiMing_Report?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Added_Time.After("' + date + '"))'
data = requests.get(url).text
data = data.replace(' ', '').split('=')[1][:-1]
data = json.loads(data)['form_ShuangDaZuHePaiMing']

url1 = 'https://creator.zoho.com.cn/api/json/saishi/view/form_ShuangDaZuHePaiMing_Report?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Modified_Time.After("' + date + '"))'
data1 = requests.get(url1).text
data1 = data1.replace(' ', '').split('=')[1][:-1]
data1 = json.loads(data1)['form_ShuangDaZuHePaiMing']

data = data+data1
#
for i in data:
    fie = ['ID', 'form_ShuangDaZuHe', 'form_ShuangDaZuHe_Single_Line_MingCheng', 'form_ShuangDaZuHe_Single_Line1', 'Dropdown_BiSaiXiangMu', 'Date_field_PaiMingRiQi', 'Formula_RiQi',
           'Dropdown_PaiMingFenLei', 'Number_PaiMing', 'Number_PaiMingBianHua', 'Number_Ying', 'Number_Shu', 'Number_JiFen', 'Number_CanSaiZhanShu']
    val = [str(i['ID']), str('"'+i['form_ShuangDaZuHe']+'"'), str('"'+i['form_ShuangDaZuHe.Single_Line_MingCheng']+'"'), str('"'+i['form_ShuangDaZuHe.Single_Line1']+'"'),
           str('"'+i['Dropdown_BiSaiXiangMu']+'"'), str('"'+i['Date_field_PaiMingRiQi']+'"'), str('"'+str(i['Formula_RiQi'])+'"'), str('"'+i['Dropdown_PaiMingFenLei']+'"'), str(i['Number_PaiMing']),
           str('"'+str(i['Number_PaiMingBianHua'])+'"'), str('"'+str(i['Number_Ying'])+'"'), str('"'+str(i['Number_Shu'])+'"'), str(i['Number_JiFen']), str('"'+str(i['Number_CanSaiZhanShu'])+'"')]

    db = pymysql.connect('video.hbang.com.cn', 'video', 'P@ssw0rd235', 'video')
    cursor = db.cursor()
    sql = "replace into form_ShuangDaZuHePaiMing(" + ','.join(fie) + ") " + "values(" + ','.join(val) + ")"
    cursor.execute(sql)
    db.commit()
    db.rollback()
    db.close()
