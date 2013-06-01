#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import plugins
import traceback
from bae.api import logging

plugin_modules = []

detail_help = u"""    帮助 - %s
%s
"""

help_info = ''

for plugin_name in plugins.__all__:
    __import__('plugins.%s' % plugin_name)
    plugin_modules.append(getattr(plugins, plugin_name))

def help_info():
    msg = u'帮助信息\n'
    for plugin_module in plugin_modules:
        msg += u'回复%s, %s\n' % (plugin_module.command, plugin_module.help_info)
    return msg

def detail_info(name):
    msg = ''
    for plugin_module in plugin_modules:
        if name == plugin_module.command:
            return detail_help % (plugin_module.command, plugin_module.detail_info)


def magic(data):
    logging.error(data)
    if data['Content'] == u'帮助' or data['Content'] == u'help':
        return help_info()
    for plugin_module in plugin_modules:
        try:
            if plugin_module.test(data):
                return plugin_module.handle(data)
        except Exception, e:
            exstr = traceback.format_exc()
            logging.error(exstr)
    return u'指令无法解析，回复help获取帮助'

if __name__ == '__main__':
    print help_info()
    print detail_info(u'天气')
