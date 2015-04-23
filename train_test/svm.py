# -*- coding:utf8 -*- #
"""
根据历史数据利用支持向量机做预测
"""
import time
import numpy as np
import cPickle

def genDayStrList(month, day, total, adjustment):
    """
    # 根据时间参数生成一组（月，日）字符串list
    # month, day: 起始月份、日期
    # total：总时间长度
    # adjustment: 日期调整
    """
    epochs = np.array(time.mktime((2014, month, day+adjustment, 0, 0, 0, 1, 0, 0))) + \
             np.arange(0, total, 1)*60*60*24  # 前面留出look-ahead的时间，做+1 adjustment，日期为0或负数没关系
    dayStrList = []
    for epoch in epochs:
        dayStrList.append(time.strftime("%m-%d", time.gmtime(epoch)))
    return dayStrList
def genXYDayStrList(month, day, total, ratio, window, adjust):
    """
    计算将用到的X，Y日期向量
    :param month:
    :param day:
    :param totalDays:
    :param ratio: 从总日期中的抽取比例
    :param window:
    :return:
    """
    XDayStrListList = []
    for idx_window in range(window):
        XMonth, XDay, XLength = month, day+idx_window, int(total*ratio)-window
        XDayStrListList.append(genDayStrList(XMonth, XDay, XLength, adjust))
    yMonth, yDay, yLength = month, day+window, int(total*ratio)-window
    yDayStrList = genDayStrList(yMonth, yDay, yLength, adjust)
    return XDayStrListList, yDayStrList
def genXY(XDayStrListList, yDayStrList):
    """
    生成SVM输入
    :param XDayStrListList:
    :param yDayStrList:
    :return:
    """
    X, y = [], []
    # Feature生成主循环
    for idx_day in range(len(yDayStrList)):
        # 读取词典
        yDayStr = yDayStrList[idx_day]
        yDayDict = cPickle.load(open("../../AliTianChi_data/dictionary/date/2014-"+yDayStr+".pkl","rb"))
        XDayDictList = []
        for idx_w in range(len(XDayStrListList)):
            XDayStr = XDayStrListList[idx_w][idx_day]
            XDayDictList.append(cPickle.load(open("../../AliTianChi_data/dictionary/date/2014-"+XDayStr+".pkl","rb")))
        # 汇总在历史中出现过得(uid,iid)
        allKeys = yDayDict.keys()
        for idx_w in range(len(XDayStrListList)):
            allKeys.append(XDayDictList[idx_w].keys())
        allKeys = list(set(allKeys))    # 去重
        # 生成当天的向量
        X_sub, y_sub = [],[]
        for key in allKeys:
            # Output
            if yDayDict.has_key(key) and yDayDict[key][0][3] > 0:
                y_sub += [1]
            else:
                y_sub += [0]
            # Input X_sub_sub = [W1H1A1,W1H1A2,...W1H24A4,...W3H24A4]
            X_sub_sub = [0]*len(XDayDictList)*24*4
            for idx_w in range(len(XDayDictList)):
                    for idx_hour in range(24):
                        for idx_action in range(4):
                            if XDayDictList[idx_w].has_key(key):
                                X_sub_sub[idx_w*24+idx_hour*4+idx_action] = XDayDictList[key][3][idx_action].count(idx_hour)
            X_sub.append(X_sub_sub)
        X.append(X_sub)
    return X,y

# 设置参数
window = 3   # 前看时间长度
totalDays = 31  # 数据集中总时间长度
rTr, rVal, rTest = .4, .3, .3
adjust = 1  # time.mktime()中的tuple比实际得到的日期多一天

# 生成训练、验证、测试集日期
[XDayStrListList_Tr, yDayStrList_Tr] = genXYDayStrList(11, 18, totalDays, rTr, window, adjust)
[XDayStrListList_Val, yDayStrList_Val] = genXYDayStrList(11, 30, totalDays, rVal, window, adjust)
[XDayStrListList_Test, yDayStrList_Test] = genXYDayStrList(12, 9, totalDays, rTest, window, adjust)
# 生成训练、验证、测试集向量
[X, y] = genXY(XDayStrListList_Tr, yDayStrList_Tr)


# 训练得到模型

# 在测试集上检验预测精度