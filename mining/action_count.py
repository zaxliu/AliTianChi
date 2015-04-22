# -*- coding:utf8 -*- #
"""
----------------------------
探究加购物车行为与对应的购买行为时延的关系
----------------------------
"""
import numpy as np
import time
import cPickle

# 时间参数
lookAhead = 3   # 前看时间长度
numDays = 31 - lookAhead
startDay = 18   # 11.18

# 生成字典名字时间, time.mktime()中的tuple比实际得到的日期多一天
# anchorDayList = [D1,D2,D3...]
anchorEpochs = np.array(time.mktime((2014, 11, startDay+lookAhead+1, 0, 0, 0, 1, 0, 0)))\
    + np.arange(0, numDays, 1)*60*60*24  # 前面留出look-ahead的实际
anchorDayList = []
for epoch in anchorEpochs:
    anchorDayList.append(time.strftime("%m-%d", time.gmtime(epoch)))
# aheadDaysList = [[A1D1,A1D2,....],[A1D1,A1D2..],...]
aheadEpochsList = []
for idx_ahead in range(lookAhead):
    aheadEpochsList.append(np.array(time.mktime((2014, 11, startDay+lookAhead-idx_ahead, 0, 0, 0, 1, 0, 0)))
                           + np.arange(0, numDays, 1)*60*60*24)
aheadDaysList = []
for epochs in aheadEpochsList:
    aheadDays = []
    for epoch in epochs:
        aheadDays.append(time.strftime("%m-%d",time.gmtime(epoch)))
    aheadDaysList.append(aheadDays)

# 变量初始化
# 行为计数器
cnt_view = np.zeros((2, numDays, 24*lookAhead))
cnt_like = np.zeros((2, numDays, 24*lookAhead))
cnt_addChart = np.zeros((2, numDays, 24*lookAhead))
cnt_buy = np.zeros((2, numDays, 24*lookAhead))

# item列表
item = cPickle.load(open("D:/My Documents/GitHub/Tianchi/AliTianChi_data/dictionary/item.pkl", "rb"))

# 计数主循环
for idxDay in range(numDays):
    # 读取相应词典
    anchorDay = anchorDayList[idxDay]
    anchorDayDict = cPickle.load(open("D:/My Documents/GitHub/Tianchi/AliTianChi_data/dictionary/date/2014-"+anchorDay+".pkl","rb"))
    aheadDaysDictList = []
    for idx_ahead in range(lookAhead):
        aheadDay = aheadDaysList[idx_ahead][idxDay]
        aheadDaysDictList.append(cPickle.load(open("D:/My Documents/GitHub/Tianchi/AliTianChi_data/dictionary/date/2014-"+aheadDay+".pkl","rb")))
    print "Counting for " + anchorDay
    # 循环读取anchorDay中出现的购买行为，并对前序窗口内行为进行计数
    for key in anchorDayDict:
        uid, iid = key
        if item.has_key(iid):
            flag = anchorDayDict[key][0][3] > 0 # 指示计数器第一维度的坐标，无购买=0，有购买=1
            for idx_ahead in range(lookAhead):  # 逐项计数
                # print "Ahead day " + str(idx_ahead+1)
                if aheadDaysDictList[idx_ahead].has_key(key):
                    for hour in aheadDaysDictList[idx_ahead][key][3][0]:
                        cnt_view[flag, idxDay, idx_ahead*24+hour] += 1
                    for hour in aheadDaysDictList[idx_ahead][key][3][1]:
                        cnt_like[flag, idxDay, idx_ahead*24+hour] += 1
                    for hour in aheadDaysDictList[idx_ahead][key][3][2]:
                        cnt_addChart[flag, idxDay, idx_ahead*24+hour] += 1
                    for hour in aheadDaysDictList[idx_ahead][key][3][3]:
                        cnt_buy[flag, idxDay, idx_ahead*24+hour] += 1

# 存储数据
print "Saving results..."
f = open("D:/My Documents/GitHub/Tianchi/AliTianChi_data/count/cnt_view.pkl", 'wb')
cPickle.dump(cnt_view, f, -1)
f.close()
f = open("D:/My Documents/GitHub/Tianchi/AliTianChi_data/count/cnt_like.pkl", 'wb')
cPickle.dump(cnt_like, f, -1)
f.close()
f = open("D:/My Documents/GitHub/Tianchi/AliTianChi_data/count/cnt_addChart.pkl", 'wb')
cPickle.dump(cnt_addChart, f, -1)
f.close()
f = open("D:/My Documents/GitHub/Tianchi/AliTianChi_data/count/cnt_buy.pkl", 'wb')
cPickle.dump(cnt_buy, f, -1)
f.close()
