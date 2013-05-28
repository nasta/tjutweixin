#-*- coding:utf-8 -*-


import webapp2
import time
import hashlib
import urllib
import urllib2
import xml.etree.ElementTree as ET

from ai import magic
from bae.core.wsgi import WSGIApplication

index = """
<!DOCTYPE html><html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>Test Page</title>
    </head>
    <body>
        This is a test page for tjutweixin
    </body>
</html>
"""
 
TOKEN = 'notimetoplay'

welcome_msg = u"""
欢迎关注天理助手
查询帮助信息请回复"help"或"h"

"""

help_info = u"""消息    功能
天气        天气
空气        空气
"""

report_info = u"""
报告Bug或有任何建议请发邮件至nasta@foxmail.com
"""


def checkSignature(request):
    global TOKEN

    signature = request.get('signature')
    timestamp = request.get('timestamp')
    nonce = request.get('nonce')
    echostr = request.get('echostr')

    token = TOKEN
    tmpList = [token, timestamp, nonce]
    tmpList.sort()
    tmpstr = '%s%s%s' % tuple(tmpList)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return echostr
    else:
        return None

def responseMsg(request):
    post_data = request.body
    data = paraseMsgXml(post_data)
    if 'Content' not in data.keys():
        content = welcome_msg
    else:
        content = process(data)
    return getReplyXml(data, content)

def process(data):
    data['CreateTime'] = int(data['CreateTime'])
    return magic(data)

def paraseMsgXml(raw_msg):
    root = ET.fromstring(raw_msg)
    msg = {}
    if root.tag == 'xml':
        for child in root:
            msg[child.tag] = child.text
    return msg

def getReplyXml(msg, replyContent):
    textTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>";
    echostr = textTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', replyContent)
    return echostr



class MainApp(webapp2.RequestHandler):
    global index
    def get(self):
        if(len(self.request.GET) == 0):
            self.response.write(index)
        else:
            self.response.write(checkSignature(self.request))
    def post(self):
        self.response.write(responseMsg(self.request))

app = webapp2.WSGIApplication([ ('/', MainApp)], debug=True)
application = WSGIApplication(app)
