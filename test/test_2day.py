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
import pdb

#pdb.set_trace()
#测试天数,用每2天预测后1天，因此是31-2
numDays = 29

#生成训练集每天月份-日期的字符串
tr1Epochs = np.array(time.mktime((2014,11,19,0,0,0,1,322,0))) + np.arange(0,29,1)*60*60*24
tr2Epochs = np.array(time.mktime((2014,11,20,0,0,0,1,322,0))) + np.arange(0,29,1)*60*60*24
tr1Days = []
for epoch in tr1Epochs:
    tr1Days.append(time.strftime("%m-%d",time.gmtime(epoch)))
tr2Days = []
for epoch in tr2Epochs:
    tr2Days.append(time.strftime("%m-%d",time.gmtime(epoch)))
#生成测试集每天月份-日期的字符串
ttEpochs = np.array(time.mktime((2014,11,21,0,0,0,1,322,0))) + np.arange(0,29,1)*60*60*24
ttDays = []
for epoch in ttEpochs:
    ttDays.append(time.strftime("%m-%d",time.gmtime(epoch)))

#存储 (uid,iid)
resultList = []

#item列表
item = cPickle.load(open("../data/dictionary/item.pkl","rb"))

#precision和recall
prec = np.zeros([30])
recall = np.zeros([30])
F1 = np.zeros([30])

#根据训练集进行每天的预测,并求得测试集上的prec和recall
for idxDay in range(numDays):
    A = 0.0 #预测对的购买数目
    B = 0.0 #总共的预测购买数目
    C = 0.0 #总共的测试购买条目
    result = {}
    #训练集和测试集
    tr1Day = tr1Days[idxDay]
    dictTr1Day = cPickle.load(open("../data/dictionary/date/2014-"+tr1Day+".pkl","rb"))
    tr2Day = tr2Days[idxDay]
    dictTr2Day = cPickle.load(open("../data/dictionary/date/2014-"+tr2Day+".pkl","rb"))  
    ttDay = ttDays[idxDay]
    dictTtDay = cPickle.load(open("../data/dictionary/date/2014-"+ttDay+".pkl","rb"))
    #预测（规则：对于商品子集里的商品，前一天加购物车且没买的，预测下一天购买）
    for key in dictTr2Day:
        uid,iid = key     
        if  item.has_key(iid) and dictTr2Day[key][0][2]>0 and dictTr2Day[key][0][3]==0: 
            result[key] = 1
            B = B+1
            if dictTtDay.has_key(key) and dictTtDay[key][0][3]>0:
                A = A+1
    for key in dictTr1Day:
        uid,iid = key     
        if  item.has_key(iid) and dictTr1Day[key][0][2]>0 and dictTr1Day[key][0][3]==0:
            if (not dictTr2Day.has_key(key)) or (dictTr2Day[key][0][3]==0):
                result[key] = 1
                B = B+1
                if dictTtDay.has_key(key) and dictTtDay[key][0][3]>0:
                    A = A+1
    for key in dictTtDay:
        uid,iid = key
        if item.has_key(iid) and dictTtDay[key][0][3]>0:
            C = C+1
    resultList.append(result)
    prec[idxDay] = A/B
    recall[idxDay] = A/C
    F1[idxDay] = 2*prec[idxDay]*recall[idxDay]/(prec[idxDay]+recall[idxDay])
    print tr1Day+' and '+tr2Day+' -> '+ttDay+' prec=%5.2f%%,rec=%5.2f%%,F1=%5.2f%%,A=%5.0f,B=%5.0f,C=%5.0f' %(prec[idxDay]*100,recall[idxDay]*100,F1[idxDay]*100,A,B,C)
print 'Mean: prec=%5.2f%%,rec=%5.2f%%,F1=%5.2f%%' %(prec.mean()*100,recall.mean()*100,F1.mean()*100)