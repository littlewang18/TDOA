# -*- coding: utf-8 -*-
# @Time    : 2024/10/21 17:10
# @Author  : littlewang
# @FileName: Channel
# @Software: PyCharm
# @Desc    : Generate a Gaussian white noise channel which the signal is passed through
import numpy as np

from tdoa import euclidean


# 高斯白噪声信道
def add_awgn_noise(signal_channel, snr):
    """
    :param signal_channel: 初始信号
    :param snr: 信噪比
    :return:
        signal_channel: 通过高斯白噪声信号
    """
    # 计算噪声功率
    signal_power = np.mean(signal_channel[0] ** 2)
    snr_linear = 10**(snr / 10.0)
    noise_power = signal_power / snr_linear

    # 增加噪声
    for i in range(len(signal_channel)):
        noise = np.random.normal(0, np.sqrt(noise_power), len(signal_channel[0]))
        signal_channel[i] += noise
    return signal_channel


# 多径效应
def multipath(signal_receiver, channel_number, channel_delay, channel_attenuation, fs):
    """
    :param signal_receiver: 接收到的信号
    :param channel_number: 信道数目
    :param channel_delay: 信道延迟
    :param channel_attenuation: 信道衰减因子
    :param fs: 采样频率
    :return:
        signal_receiver:增加信道延迟和衰减的信号
    """
    # 信号增加信道延迟和衰减
    for index in range(channel_number):
        delay = int(channel_delay[index] * fs)
        signal_attenuation = channel_attenuation[index] * np.roll(signal_receiver, delay)
        signal_receiver += signal_attenuation

    return signal_receiver


# 计算不同基站到达接收器的信号
def calculate_signal(base_position, receiver_position, signal_init, velocity, fs, time_factor):
    """
    :param base_position: 基站位置
    :param receiver_position: 接收器位置
    :param signal_init: 初始信号
    :param velocity: 信号传播速度
    :param fs: 采样频率
    :param time_factor: 时间扰动因子
    :return:
        signal: 接收信号
        time_diff: 真实信号延迟
    """
    # 计算距离差
    distances = np.array([euclidean(station, receiver_position) for station in base_position])

    # 计算到达所需时间
    arrival_times = distances / velocity

    # 以最近基站作为参考基站
    reference_time = arrival_times[0]

    # 计算时间差
    time_diff = arrival_times - reference_time

    # 计算时延对应采样点数
    time_delay = (time_diff * fs).astype(int)

    # 信号加上距离时延
    signal_channel = np.zeros((len(base_position), len(signal_init)))
    for i in range(len(base_position)):
        signal_channel[i] = np.roll(signal_init, time_delay[i])

        # 加上时间扰动
        signal_channel[i] = np.roll(signal_channel[i], np.random.random_sample() * time_factor)


    return signal_channel, time_diff
