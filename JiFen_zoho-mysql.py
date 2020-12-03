import pymysql
import requests
import json
import time
import calendar

t1 = time.localtime(time.time())
date = ''.join([str(int(t1.tm_mday)), '-', calendar.month_abbr[int(t1.tm_mon)], '-', str(t1.tm_year)])

url = 'https://creator.zoho.com.cn/api/json/saishi/view/form_JiFen_Report?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Added_Time.After("' + date + '"))'
data = requests.get(url).text
data = data.replace(' ', '').split('=')[1][:-1]
data = json.loads(data)['form_JiFen']

url1 = 'https://creator.zoho.com.cn/api/json/saishi/view/form_JiFen_Report?authtoken=d51ecfa14f98e8f14c91ac894bf8e7d4&scope=creatorapi&criteria=(Modified_Time.After("' + date + '"))'
data1 = requests.get(url1).text
data1 = data1.replace(' ', '').split('=')[1][:-1]
data1 = json.loads(data1)['form_JiFen']

data = data+data1

for i in data:
    fie = ['ID', 'form_YunDongYuan', 'Number_Nian', 'Number_Zhou', 'Query_SaiShi', 'Dropdown_XiangMu', 'Dropdown_MingCi', 'Number_JiFen']
    val = [str(i['ID']), str('"'+i['form_YunDongYuan']+'"'), str(i['Number_Nian']), str(i['Number_Zhou']), str('"'+i['Query_SaiShi']+'"'),
                    str('"'+i['DropdownXiangMu']+'"'), str('"'+i['Dropdown_MingCi']+'"'), str(i['Number_JiFen'])]

    db = pymysql.connect('video.hbang.com.cn', 'video', 'P@ssw0rd235', 'video')
    cursor = db.cursor()
    sql = "replace into form_JiFen(" + ','.join(fie) + ") " + "values(" + ','.join(val) + ")"
    cursor.execute(sql)
    db.commit()
    db.rollback()
    db.close()
