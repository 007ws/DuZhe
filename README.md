简易的分布式爬虫: 爬取最近8年的读者文章。
利用scrapy-redis 爬取最近8年的读者文章。利用 Master-Slave 模式爬取。做此爬虫的目的是学习分布式爬虫。

分布式爬虫策略: 
Master端(核心服务器)：使用 Fedora26，搭建一个Redis数据库，不负责爬取，只负责url指纹判重、Request的分配，以及数据的存储。
Slaver端(爬虫程序执行端) ：使用 3台 Fedora26 ，负责执行爬虫程序，运行过程中提交新的Request给Master。
首先Slaver端从Master端拿任务（Request、url）进行数据抓取，Slaver抓取数据的同时，产生新任务的Request便提交给 Master 处理；Master端只有一个Redis数据库，负责将未处理的Request去重和任务分配，将处理后的Request加入待爬队列，并且存储爬取的数据。
