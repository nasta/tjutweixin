#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import urllib
import urllib2
import json

url = 'http://pm25.in/api/querys/aqi_details.json?city=tianjin&token=g5Fr9gbhkznsKsVbP4Yv'

command = u'空气'
help_info = u'显示空气质量'
detail_info = u''

def test(data):
    try:
        msg = data['Content']
        if msg == '空气':
            return True
    except:
        return False

def handle(data):
    AQI = {"aqi":None, "area":None, "pm2_5":None, "pm10":None, "quality":None, "time_point":None}
    try:
        rawinfo = urllib2.urlopen(url).read()
        airinfo = json.loads(rawinfo)
        airinfo = airinfo[-1]
        for key in list(airinfo.viewkeys()):
            AQI[key] = airinfo[key]
    except:
        return u"暂时无法获取空气质量详情，请稍后再试"
    
    content = u"%s空气质量指数：%s\nPM2.5: %s \t PM10: %s\n空气质量类别为：%s\n 数据来源网络 更新时间 %s" % (AQI["area"], AQI["aqi"], AQI["pm2_5"], AQI["pm10"], AQI["quality"], AQI["time_point"])
    return content

if __name__ == '__main__':
    print test({'Content': '空气'})
    print handle({})
