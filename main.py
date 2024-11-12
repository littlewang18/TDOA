# -*- coding: utf-8 -*-
# @Time    : 2024/10/21 17:10
# @Author  : littlewang
# @FileName: TDOA
# @Software: PyCharm
# @Desc    : Simulate TDOA
import time
from pathlib import Path

from Config import *
from tdoa import tdoa, euclidean
from Channel import add_awgn_noise, multipath, calculate_signal
from Export import signal_plot_export, tdoa_plot_export, data_export
from init import init_position, init_channel_delay, init_am_signal, init_fm_signal


# ToDo [√] 1. 加入多径效应, 噪音影响
# ToDo [√] 2. 三维定位
# ToDo [√] 3. 时延扰动
# ToDo [ ] 4. 信号分类
# ToDo [ ] 5. 信道估计与均衡
# ToDo [×] 6. 基站选择

# 主程序
if __name__ == '__main__':
    # 产生传输信号
    if signal_type == 'AM':
        modulating_signal, carrier_signal, signal_init = init_am_signal(fc, fm, beta, ac, fs, duration)
    else:
        modulating_signal, carrier_signal, signal_init = init_fm_signal(fm_fc, fm_fm, fm_am, fm_ac, fm_fs, duration)

    # 初始化基站
    base_position, receiver_position = init_position(base_number, base_range)

    # 初始化信道
    channel_delay, channel_attenuation = init_channel_delay(channel_number)

    # 增加零时延减小互相关边缘效应
    padded_signal_init = np.pad(signal_init, (zero_padding, zero_padding), mode='constant')

    # 不同位置基站到达接收器的信号
    signal_channel, true_time_delay = calculate_signal(base_position, receiver_position,
                                                       padded_signal_init, velocity, fs, time_factor)
    # 信号通过高斯白噪声信道
    signal_receiver = add_awgn_noise(signal_channel, snr[3])

    # 多径效应
    signal_receiver = multipath(signal_receiver, channel_number, channel_delay, channel_attenuation, fs)

    # toda 预测接收机位置
    signal_source_position, time_delay = tdoa(base_number, base_position, signal_receiver, fs, velocity)

    # 误差计算
    error = euclidean(signal_source_position, receiver_position)

    # 数据输出
    results_directory = "Data/" + time.strftime("%Y-%m-%d-%H-%M-%S") + "/"
    Path(results_directory).mkdir(parents=True, exist_ok=True)
    if export_plot:
        # signal_plot_export(duration, fs, padded_signal_init, signal_receiver, zero_padding, results_directory)
        tdoa_plot_export(base_position, receiver_position, signal_source_position, results_directory)
    if export_data:
        data_export(signal_source_position, receiver_position, results_directory, error)

