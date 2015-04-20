#-*- coding:utf8 -*-#
'''
----------------------------
在已有的数据集中进行测试，并查看算法的性能
预测方法：前两天内加了购物车但是没有购买的，预测后一天会购买
----------------------------
'''
import cPickle
import numpy as np
import time
import csv
import pdb

#pdb.set_trace()

#存储 (uid,iid)
result = {}

#item列表
item = cPickle.load(open("../data/dictionary/item.pkl","rb"))

#
tr1Day = "12-17"
dictTr1Day = cPickle.load(open("../data/dictionary/date/2014-"+tr1Day+".pkl","rb"))
tr2Day = "12-18"
dictTr2Day = cPickle.load(open("../data/dictionary/date/2014-"+tr2Day+".pkl","rb"))  

#预测（规则：对于商品子集里的商品，前一天加购物车且没买的，预测下一天购买）
for key in dictTr2Day:
    uid,iid = key     
    if  item.has_key(iid) and dictTr2Day[key][0][2]>0 and dictTr2Day[key][0][3]==0: 
        result[key] = 1
for key in dictTr1Day:
    uid,iid = key     
    if  item.has_key(iid) and dictTr1Day[key][0][2]>0 and dictTr1Day[key][0][3]==0:
        if (not dictTr2Day.has_key(key)) or (dictTr2Day[key][0][3]==0):
            result[key] = 1

#写入文件
f = open("tianchi_mobile_recommendation_predict_"+time.strftime("%y%m%d_%H%M%S",time.gmtime(time.time()))+".csv","wb")
write = csv.writer(f)
write.writerow(["user_id","item_id"])
total = 0
for key in result:
    write.writerow(key)
    total += 1 
print "generate submission file,total %d  (uid,iid)" %total
f.close()
