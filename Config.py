# -*- coding: utf-8 -*-
# @Time    : 2024/11/4 16:44
# @Author  : littlewang
# @FileName: Config
# @Software: PyCharm
# @Desc    : initialize parameter
import numpy as np

# 定位信号种类
signal_type = 'AM'

# 实验参数
number = 30             # 实验次数

# AM信号参数
fc = 10000              # 载波频率      单位: Hz
fm = 10                 # 调制信号频率   单位: Hz
am = 1                  # 调制信号的振幅
ac = 0.5                # 载波信号的振幅
fs = 8000000             # 采样频率
duration = 0.01            # 信号持续时间   单位: 秒

# FM信号参数
beta = 5
fm_fc = 1000000         # 载波频率      单位: Hz
fm_fm = 30              # 调制信号频率   单位: Hz
fm_am = 1               # 调制信号的振幅
fm_ac = 0.5             # 载波信号的振幅
fm_fs = 200000          # 采样频率

# 零填充
zero_padding = 1000     # 增加零填充以减小边缘效应

# 信道参数
snr = np.arange(0, 100, 10)  # 信噪比（SNR）
channel_number = 10          # 信道数目, 模拟多径效应
time_factor = 0.35           # 时间扰动因子

# 基站参数
base_number = 10        # 基站数目 至少大于3
base_range = 5000       # 基站随机生成范围 range * range 单位: 平方米

# 传播速度
velocity = 3 * 10**8    # 光速 单位：m/秒

# 数据保存
export_plot = True
export_data = True