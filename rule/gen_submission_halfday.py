#-*- coding:utf8 -*-#
'''
----------------------------
在已有的数据集中进行测试，并查看算法的性能
预测方法：前日后半天加了购物车但是没有购买的，预测为后一天会购买
----------------------------
'''
import cPickle
import csv
import numpy as np
import time
#import pdb

#item列表
item = cPickle.load(open("../data/dictionary/item.pkl","rb"))

result = {}
trDay = '12-18'
dictTrDay = cPickle.load(open("../data/dictionary/date/2014-"+trDay+".pkl","rb")) 
#预测（规则：对于商品子集里的商品，前一天加购物车且没买的，预测下一天购买）
for key in dictTrDay:
    uid,iid = key     
    if  item.has_key(iid) and dictTrDay[key][0][2]>0 and dictTrDay[key][0][3]==0 and dictTrDay[key][3][2][-1]>12: 
        result[key] = 1

#写入文件
f = open("predict"+time.strftime("%y%m%d_%H%M%S",time.gmtime(time.time()))+".csv","wb")
write = csv.writer(f)
write.writerow(["user_id","item_id"])
total = 0
for key in result:
    write.writerow(key)
    total += 1 
print "generate submission file,total %d  (uid,iid)" %total
f.close()