#### 2017-7-21

两个脚本，

mongo_data.py 是从mongo数据库里获取'micon', 的唯一标识，
然后按此标识去'/recordata/recordfile/micon/' 里提取
特定的日志文件， 并保存在各种用户id的目录中。分A 。B类文件

psql_data.py 从Psql数据库中按上面的id提取用户名，并用正则筛选出地产用户