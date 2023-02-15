import matplotlib.pyplot as plt
import numpy as np
from os import path, makedirs, walk, remove


def print_plots(xf, yf, file_name, i, frame_id, channel=None, max_value=None):
    if channel is not None:
        if channel == 0:
            channel_name = "LC"
        if channel == 1:
            channel_name = "RC"

    plt.plot(xf, np.abs(yf)[:int(xf.shape[0])])
    if max_value is not None:
        plt.ylim([0, max_value])

    plt.savefig(f'graphs/{file_name}/{file_name} {channel_name} - {frame_id}.png')
    plt.cla()


def print_data(yf, file_name, i, frame_id, channel=None):
    if channel is not None:
        if channel == 0:
            channel_name = "LC"
        if channel == 1:
            channel_name = "RC"

    with open(f"data/{file_name}/{file_name} {channel_name} - {i} - {frame_id}.txt", 'w') as f:
        for x in yf:
            f.write(str(f"{x}\n"))
        f.close()


def clear_files(file_name):
    folders = ["graphs", "data"]

    for i in range(len(folders)):
        if not path.exists(f"{folders[i]}/{file_name}"):
            makedirs(f"{folders[i]}/{file_name}")

        for files in walk(f"{folders[i]}/{file_name}"):
            filelist = list(files[2])
            for file in filelist:
                if file_name in file:
                    remove(path.join(f"{folders[i]}/{file_name}", file))

