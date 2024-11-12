# -*- coding: utf-8 -*-
# @Time    : 2024/10/28 08:57
# @Author  : littlewang
# @FileName: Export
# @Software: PyCharm
# @Desc    : Export the Data to csv
import csv
import numpy as np
import matplotlib.pyplot as plt


# 数据输出
def data_export(signal_source_position_list, receiver_position, results_directory, error):
    flag = False
    export_to_file = results_directory + "result.csv"
    with open(export_to_file, "w", newline='\n') as out:
        writer = csv.writer(out, delimiter=',')
        if not flag:
            header = np.array([
                "Predicted PositionX",
                "Predicted PositionY",
                "Predicted PositionZ",
                "Receiver PositionX",
                "Receiver PositionY",
                "Receiver PositionZ",
                "Error",
            ])
            writer.writerow(header)
            flag = True
            print(flag)

        data = np.array([
            signal_source_position_list[0],
            signal_source_position_list[1],
            signal_source_position_list[2],
            receiver_position[0],
            receiver_position[1],
            receiver_position[2],
            error,
        ])
        writer.writerow(data)
    out.close()


# 信号输出
def signal_plot_export(duration, fs, padded_signal_init, signal_receiver, zero_padding, results_directory):
    duration = duration + (zero_padding / fs) * 2
    t = np.arange(0, duration, 1 / fs)
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, padded_signal_init)
    plt.title('Original AM Signal')
    plt.subplot(2, 1, 2)
    for index in range(len(signal_receiver)):
        plt.plot(t, signal_receiver[0], label=f'signal{index}')
    plt.title('Received Signal at Receiver')
    plt.tight_layout()
    plt.legend()

    # 保存图像
    fig_name = results_directory + "/signal_plot.png"
    plt.savefig(fig_name)
    plt.clf()


# tdoa输出
def tdoa_plot_export(base_position, receiver_position, signal_source_position, results_directory):
    # 基站位置
    x = base_position[:, 0]
    y = base_position[:, 1]
    z = base_position[:, 2]

    ax = plt.axes(projection="3d")

    plt.ion()
    ax.scatter3D(x, y, z, color="black")
    ax.scatter3D(receiver_position[0], receiver_position[1], receiver_position[2], marker='o', color="red")
    ax.scatter3D(signal_source_position[0], signal_source_position[1], signal_source_position[2], marker='^', color="blue")
    plt.title("simple 3D scatter plot")

    plt.ioff()
    plt.show()
    fig_name = results_directory + "/tdoa_plot.png"
    plt.savefig(fig_name)
    plt.clf()
