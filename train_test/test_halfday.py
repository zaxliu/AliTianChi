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
import pdb

# pdb.set_trace()
#测试天数,用每天预测后一天，因此是31-1
numDays = 30

#生成训练集每天月份-日期的字符串
trEpochs = np.array(time.mktime((2014,11,19,0,0,0,1,322,0))) + np.arange(0,30,1)*60*60*24
trDays = []
for epoch in trEpochs:
    trDays.append(time.strftime("%m-%d",time.gmtime(epoch)))
#生成测试集每天月份-日期的字符串
ttEpochs = np.array(time.mktime((2014,11,20,0,0,0,1,322,0))) + np.arange(0,30,1)*60*60*24
ttDays = []
for epoch in ttEpochs:
    ttDays.append(time.strftime("%m-%d",time.gmtime(epoch)))
#存储 (uid,iid)
resultList = []

#item列表
item = cPickle.load(open("../data/dictionary/item.pkl","rb"))

#precision和recall
prec = np.zeros([numDays])
recall = np.zeros([numDays])
F1 = np.zeros([numDays])

#根据训练集进行每天的预测,并求得测试集上的prec和recall
for idxDay in range(numDays):
    A = 0.0 #预测对的购买数目
    B = 0.0 #总共的预测购买数目
    C = 0.0 #总共的测试购买条目
    result = {}
    #训练集和测试集
    trDay = trDays[idxDay]
    dictTrDay = cPickle.load(open("../data/dictionary/date/2014-"+trDay+".pkl","rb")) 
    ttDay = ttDays[idxDay]
    dictTtDay = cPickle.load(open("../data/dictionary/date/2014-"+ttDay+".pkl","rb"))
    #预测（规则：对于商品子集里的商品，前一天加购物车且没买的，预测下一天购买）
    for key in dictTrDay:
        uid,iid = key     
        if item.has_key(iid) and dictTrDay[key][0][2] > 0 and dictTrDay[key][0][3] == 0 and dictTrDay[key][3][2][-1] > 11:
            result[key] = 1
            B += 1
            if dictTtDay.has_key(key) and dictTtDay[key][0][3]>0:
                A += 1
    for key in dictTtDay:
        uid,iid = key
        if item.has_key(iid) and dictTtDay[key][0][3]>0:
            C += 1
    resultList.append(result)
    prec[idxDay] = A/B
    recall[idxDay] = A/C
    F1[idxDay] = 2*prec[idxDay]*recall[idxDay]/(prec[idxDay]+recall[idxDay])
    print trDay+'->'+ttDay+' prec=%5.2f%%,rec=%5.2f%%,F1=%5.2f%%,A=%5.0f,B=%5.0f,C=%5.0f' %(prec[idxDay]*100,recall[idxDay]*100,F1[idxDay]*100,A,B,C)
print 'Mean: prec=%5.2f%%,rec=%5.2f%%,F1=%5.2f%%' %(prec.mean()*100,recall.mean()*100,F1.mean()*100)