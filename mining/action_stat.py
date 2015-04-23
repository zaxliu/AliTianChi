# -*- coding:utf8 -*- #
"""
计算行为计数的统计信息并进行可视化
"""

import cPickle
import numpy as np
import matplotlib.pyplot as plt

# 时间参数
lookAhead = 3   # 前看时间长度

# 读取计数数据
cnt_view = cPickle.load(open("../../AliTianChi_data/count/cnt_view.pkl", 'rb'))
cnt_like = cPickle.load(open("../../AliTianChi_data/count/cnt_like.pkl", 'rb'))
cnt_addChart = cPickle.load(open("../../AliTianChi_data/count/cnt_addChart.pkl", 'rb'))
cnt_buy = cPickle.load(open("../../AliTianChi_data/count/cnt_buy.pkl", 'rb'))

# 分正负样本，并对一个月进行平均
mean_view_pos = np.reshape(np.mean(cnt_view[1, :, :], 0), lookAhead*24)
mean_like_pos = np.reshape(np.mean(cnt_like[1, :, :], 0), lookAhead*24)
mean_addChart_pos = np.reshape(np.mean(cnt_addChart[1, :, :], 0), lookAhead*24)
mean_buy_pos = np.reshape(np.mean(cnt_buy[1, :, :], 0), lookAhead*24)
mean_view_neg = np.reshape(np.mean(cnt_view[0, :, :], 0), lookAhead*24)
mean_like_neg = np.reshape(np.mean(cnt_like[0, :, :], 0), lookAhead*24)
mean_addChart_neg = np.reshape(np.mean(cnt_addChart[0, :, :], 0), lookAhead*24)
mean_buy_neg = np.reshape(np.mean(cnt_buy[0, :, :], 0), lookAhead*24)

# 进行绘图
t = np.linspace(1, lookAhead*24, lookAhead*24)
plt.plot(t, mean_buy_pos/np.max( mean_buy_pos), 'b-')
plt.plot(t, mean_buy_neg/np.max( mean_buy_neg), 'r-')
plt.show()
