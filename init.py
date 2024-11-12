# -*- coding: utf-8 -*-
# @Time    : 2024/10/21 17:13
# @Author  : littlewang
# @FileName: init
# @Software: PyCharm
# @Desc    : initialize the base position and receiver position
import numpy as np


# 初始化AM信号
def init_am_signal(fc, fm, am, ac, fs, duration):
    """
    :param fc: 载波频率，单位Hz
    :param fm: 调制信号频率，单位Hz
    :param am: 调制信号的振幅
    :param ac: 载波信号的振幅
    :param fs: 采样频率
    :param duration: 信号持续时间，单位秒
    :return:
        am_signal: am信号
    """
    # 时间轴
    t = np.arange(0, duration, 1 / fs)

    # 调制信号
    modulating_signal = am * np.cos(2 * np.pi * fm * t)

    # 载波信号
    carrier_signal = ac * np.sin(2 * np.pi * fc * t)

    # 生成AM信号
    am_signal = (1 + modulating_signal) * carrier_signal


    return  modulating_signal, carrier_signal, am_signal


# 初始化FM信号
def init_fm_signal(fc, fm, beta, ac, fs, duration):
    """
    :param fc: 载波频率，单位Hz
    :param fm: 调制信号频率，单位Hz
    :param beta: 调频参数
    :param ac: 载波信号的振幅
    :param fs: 采样频率
    :param duration: 信号持续时间，单位秒
    :return:
        fm_signal: fm信号
    """
    # 时间轴
    t = np.arange(0, duration, 1 / fs)

    # 调制信号（低频信号）
    modulating_signal = np.sin(2 * np.pi * fm * t)

    # FM信号
    carrier_signal = ac * np.cos(2 * np.pi * fc * t + beta * modulating_signal)

    # 生成FM信号
    fm_signal = ac * np.cos(2 * np.pi * fc * t + beta * modulating_signal)

    return  modulating_signal, carrier_signal, fm_signal


# 初始化信道
def init_channel_delay(channel_number):
    """
    :param channel_number: 信道数目
    :return:
        channel_delay: 信道延迟
        channel_attenuation: 信道衰减系数
    """
    channel_delay = np.zeros(channel_number)
    channel_attenuation = np.zeros(channel_number)
    for i in range(channel_number):
        channel_delay[i] = np.random.uniform(0, 10e-6)
        channel_attenuation[i] = np.random.uniform(0, 1)

    return channel_delay, channel_attenuation


# 初始化基站
def init_position(base_number, base_range):
    """
    :param base_number: 基站数目
    :param base_range: 基站初始化范围
    :return:
        base_position: 发射基站位置
        receiver_position: 接收机位置
    """
    # 定义发射基站位置
    base_position = np.random.randint(-base_range, base_range, size=(base_number, 3))

    # 随机生成接收器位置
    receiver_position = np.random.randint(-base_range, base_range, size=3)

    # 基站排序
    squared_sum = np.sum(base_position ** 2 - receiver_position ** 2, axis=1)
    sorted_indices = np.argsort(squared_sum)
    base_position = base_position[sorted_indices]

    return base_position, receiver_position