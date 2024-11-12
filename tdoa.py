# -*- coding: utf-8 -*-
# @Time    : 2024/10/21 17:10
# @Author  : littlewang
# @FileName: Positioning
# @Software: PyCharm
# @Desc    : Positioning by TDOA
import numpy as np
from scipy.optimize import least_squares


# 距离计算
def euclidean(pos1, pos2):
    """
    :param pos1: 位置1
    :param pos2: 位置2
    :return:
        np.linalg.norm(pos1 - pos2): 返回二范数
    """
    return np.linalg.norm(pos1 - pos2)


# 利用广义相关来计算不同信号之间的时延
def calculate_time_delay(base_number, signal_receiver, fs):
    """
    :param base_number: 基站数目
    :param signal_receiver: 接收到的信号
    :param fs: 采样频率
    :return:
        time_delay: 信号之间的时间延迟
    """
    time_delay = np.zeros(base_number)

    for i in range(len(signal_receiver)):

        # 计算信号的互相关，最近基站接收信号为参考信号
        correlation = np.correlate(signal_receiver[i], signal_receiver[0], mode='full')

        # 找到最大相关值的位置
        max_corr_index = np.argmax(correlation)

        # 计算信号之间的样本偏移量
        lags = np.arange(-len(signal_receiver[0]) + 1, len(signal_receiver[0]))
        sample_delay = lags[max_corr_index]

        # 根据采样率将样本偏移量转换为时间
        time_delay[i] = sample_delay / fs

    return time_delay


# 最小二乘法计算方程
def three_equations(predicting_position, base_position, velocity, time_delay):
    """
    :param predicting_position: 预测的位置
    :param base_position: 基站位置
    :param velocity: 信号传播速度
    :param time_delay: 时间延迟
    :return:
        residuals: 最小二乘法方程组
    """
    residuals = []
    distance = time_delay * velocity
    for i in range(1, len(distance)):
        dist_to_ref = np.linalg.norm(base_position[i] - predicting_position)
        dist_to_rec = np.linalg.norm(base_position[0] - predicting_position)
        residuals.append(dist_to_ref - dist_to_rec - distance[i])

    return residuals


# 多维TDOA定位
def tdoa(base_number, base_position, signal_receiver, fs, velocity):
    """
    :param base_number: 基站数目
    :param base_position: 基站位置
    :param signal_receiver: 接收到信号
    :param fs: 采样频率
    :param velocity: 信号传播速度
    :return:
        result.x: 最小二乘法计算的位置
        time_delay: 计算的时延
    """
    # 计算不同信号之间的时延
    time_delay = calculate_time_delay(base_number, signal_receiver, fs)

    # 求解方程组
    initial_guess = np.array([1.0, 1.0, 1.0])

    result = least_squares(
        three_equations,
        initial_guess,
        args=(base_position, velocity, time_delay),
        ftol=1e-12,
        xtol=1e-12,
        gtol=1e-12,
        method="trf"
    )

    return result.x, time_delay