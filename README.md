# pyScrapyDownUtils
#### 在用scrapy爬取数据的时，有时候会有文件数据的下载。
### 如何使用
####导入包  
        from mymidtest.mydownutils.redisutil import operatRedis  
#### 在自己的spider类文件中加入custom_settings配置如下  
class MytestSpider(scrapy.Spider):  
　　　　name = "mytest"  
　　　　custom_settings = {  
　　　　　　　　　'EXTENSIONS': {  
　　　　　　　　　　　'mymidtest.mydownutils.extension.SpiderOpenCloseLogging': 500,  
　　　　　　　　　},  
　　　　　　　　'MYEXT_ENABLED': True,  
　　　　　}  
'mymidtest.mydownutils.extension.SpiderOpenCloseLogging'为工具包在项目下的路径
'项目名称.包名.文件名.类名'  
#### 并在类的__init__方法中添加  
    def __init__(self, ):
        super(MytestSpider, self).__init__()
        self.myredis = operatRedis(self.name)
        self.Redis = self.myredis.get_instent()
####  在使用时添加
	self.myredis.add_url_filepath(self.Redis,url,filepath_all)
	url为下载地址，filepath_all为文件存储路径

### 该工具包使用Redis作为scrapy爬下来链接存储的地址使用时需要redis模块
### 可以为程序设置下载线程的数量
######在downuitls.py文件中可以设置下面  
	queue=Queue.Queue(maxsize=10) ## 可以设置队列的大小  0或小于0为无限大  
	downThreadNumb = 3  # 下载线程个数  可以设置下载线程数量 















	
