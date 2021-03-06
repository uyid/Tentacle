#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from script import Script, SERVICE_PORT_MAP

_file_dic = {
    "crossdomain.xml": 'allow-access-from domain="*"',
    ".svn/entries": 'dir',
    ".svn/wc.db": 'sqlite format',
    "WEB-INF/web.xml": "<web-app",
    "robots.txt": 'disallow:',
    ".git": None,
    ".git/HEAD": None,
    ".git/index": 'dirc',
    ".git/config": 'master',
    "README.MD": None,
    "README.md": None,
    "README": None,
    ".DS_store": None,
    "trace": None,
    "WEB-INF/database.propertie": '.driver',
    ".htaccess": 'rewrite',
    "phpinfo.php": 'php.ini',
    'phpmyadmin/index.php' : "phpmyadmin",
    "test.php": None,
    "test.jsp": None,
    "test.jspx": None,
    "test.aspx": None,
    "test.asp": None,
}

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'info file'
        self.keyword = ['web']
        self.info = 'info file'
        self.type = 'info'
        self.level = 'low'
        Script.__init__(self, target=target, service_type=self.service_type)

    def prove(self):
        self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
            ]))
            for path in path_list:
                flag = 5
                for key in _file_dic.keys():
                    if flag == 0 :
                        self.flag = -1
                        break
                    url = path + key
                    res = self.curl('get', url, allow_redirects=False)
                    if res != None:
                        if res.status_code == 200:
                            if _file_dic[key] == None :
                                self.flag = 0
                                self.res.append({"info": url, "key": key})
                            elif _file_dic[key] in res.text.lower():
                                self.flag = 1
                                self.res.append({"info": url, "key": key})
                    else:
                        flag -= 1
