# -*- coding: utf-8 -*-
__author__ = 'cht'

import threading
import Queue
import urllib
import os

from mymidtest.mydownutils.redisutil import operatRedis


queue=Queue.Queue(maxsize=10) ## 可以设置队列的大小  0或小于0为无限大
con = threading.Condition()
downThreadNumb = 3  # 下载线程个数  可以设置下载线程数量


allnumb = 0 # 需要下载的总数  此处不可修改


def addDownloadTask(task):
    queue.put(task,1)


def getDownloadTaskFromQueue():
    return queue.get(True)


def downloadAndSave(url,savePath,threadName):
    folder=savePath[:savePath.rfind('/')]
    # 判断文件夹是否存在  不存在就创建文件夹
    # 这里多线程会有bug   os.path有可能已经存在  需要加锁
    con.acquire()
    if not os.path.exists(os.environ['HOME'] + folder):
        os.makedirs(os.environ['HOME'] + folder)
    con.release()
    # 判断文件件是否存在创建文件件  可能存在的问题不同链接 相同存储地址会导致异常
    if not os.path.exists(os.environ['HOME']+savePath):
        try:
            print threadName + u'正在下载一个文件'
            urllib.urlretrieve(url,os.environ['HOME']+savePath)
        except Exception,e:
            # print e
            pass
        ##取消解压    下面代码会自动解压压缩文件
        # if '.rar' in savePath:
        #     command='unrar x '+os.environ['HOME']+savePath+' '+os.environ['HOME'] + folder
        #     commands.getstatusoutput(command)
        # if '.zip' in savePath:
        #     f = zipfile.ZipFile(os.environ['HOME']+savePath, 'r')
        #     for file in f.namelist():
        #         file_name = os.path.join(os.environ['HOME']+folder+'/'+ file.decode('gb2312'))
        #         # print file_name
        #         with open(file_name, 'wb')as code:
        #             code.write(f.read(file))
    pass


def dowork(name):
    myredis = operatRedis(name)
    Redis = myredis.get_instent()
    global allnumb
    allnumb = len(Redis.hkeys(name))
    threadPool = []
    ss = AddQueueThread(name, Redis)
    threadPool.append(ss)
    # #创建下载线程 和队列放置线程  并开始下载
    for i in range(downThreadNumb):
        thread = DownloadThread()
        threadPool.append(thread)
    for t in threadPool:
        print u'开启' + t.myname() + u'线程'
        t.start()
    for t in threadPool:
        t.join()

    return Redis


class DownloadMission(object):
    def __init__(self, url='', path=''):
        self.url = url
        self.savePath = path


class DownloadThread(threading.Thread):

    ''' 拿取队列数据  下载线程 '''

    def __init__(self):
        super(DownloadThread, self).__init__()
        pass

    def run(self):
        global allnumb
        while allnumb > 0:
            con.acquire()
            allnumb -= 1
            if allnumb > -1:
                task = getDownloadTaskFromQueue()
                con.release()
                downloadAndSave(task.url, task.savePath,self.name)  # #执行下载任务
            else:
                con.release()
                continue
        print u'下载线程  ' + self.name + u'  结束'

    def myname(self):
        return u'下载线程  ' + self.name


class AddQueueThread(threading.Thread):

    '''
    添加队列线程
    '''
    def __init__(self,name,Redis):
        super(AddQueueThread, self).__init__()
        self.spiderName = name
        self.Redis = Redis
        pass

    def run(self):
        for key in self.Redis.hkeys(self.spiderName):
            url = key
            filepath = self.Redis.hget(self.spiderName,key)
            addDownloadTask(DownloadMission(url, filepath))
        print u'队列线程  ' + self.name + u'结束'

    def myname(self):
        return u'队列线程  ' + self.name


