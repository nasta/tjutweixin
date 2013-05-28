#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import urllib
import urllib2
import json

url = 'http://m.weather.com.cn/data/101030500.html'

command = u'天气'
help_info = u'显示天气状况'
detail_info = u'回复weather或天气显示天气预报'

def test(data):
    try:
        msg = data['Content']
        if msg.find('weather')>=0 or msg.find('天气')>=0 or msg == 'tq':
            return True
    except:
        return False

def handle(data):
    global url
    try:
        rawinfo = urllib2.urlopen(url).read()
        weather = json.loads(rawinfo)
        weather = weather["weatherinfo"]
        content = u"%s, %s, %s\n" % (weather["city"], weather["date_y"], weather["week"]) + u"今天：%s,%s\n" % ( weather["temp1"], weather["weather1"]) + u"明天：%s,%s\n" % ( weather["temp2"], weather["weather2"]) + u"后天：%s,%s\n" % (weather["temp3"], weather["weather3"])
        return content
    except Exception, e:
        return u"天气"

if __name__ == '__main__':
    print test({'Content': u'天气'})
    print handle({})
