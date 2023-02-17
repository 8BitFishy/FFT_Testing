import csv

import matplotlib.pyplot as plt
import numpy as np
from os import path, makedirs, walk, remove

def output_files(fft_data, xf, file_name, options, meta_data):
    max_value = find_highest_value(fft_data)
    print(f"Printing frequency data")

    print_x_data(xf, file_name)
    for c in range(fft_data.shape[0]):
        print(f"Printing data for channel {c + 1} of {fft_data.shape[0]}")

        write_csv(fft_data[c], xf, file_name, c)
        printed = 0


        for i in range(fft_data.shape[1]):

            frame_id = round((i * options['frame_duration']), 2)
            #print(f"Printing frame {i} of {all_y_data.shape[0]} for channel {c + 1} of {channels}")

            if int(((i / fft_data.shape[1]) / meta_data['channels']) * 100) % 10 == 0:
                if printed == 0:
                    print(f"{int(((i / fft_data.shape[1]) / meta_data['channels']) * 100)}%...", end="")
                    printed = 1
            else:
                printed = 0

            if options['print_graphs'] == "y":
                print_plots(xf, fft_data[c][i], file_name, i, frame_id, c, max_value)

            #output_manager.print_data(all_y_data[i], file_name, i, frame_id, c)




def print_plots(xf, frame_fft_data, file_name, i, frame_id, channel="LC", max_value=None):
    if channel is not None:
        if channel == 0:
            channel_name = "LC"
        if channel == 1:
            channel_name = "RC"
    plt.plot(xf, np.abs(frame_fft_data)[:int(xf.shape[0])])
    if max_value is not None:
        plt.ylim([0, max_value])

    plt.savefig(f'graphs/{file_name}/{file_name} {channel_name} - {i} - {frame_id}.png')
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


def print_x_data(xf, file_name):
    with open(f"data/{file_name}/{file_name} x_data.txt", 'w') as f:
        for x in xf:
            f.write(str(f"{x}\n"))
        f.close()


def write_csv(channel_fft_data, xf, file_name, channel=None):
    if channel is not None:
        if channel == 0:
            channel_name = "LC"
        if channel == 1:
            channel_name = "RC"
    else:
        channel_name = "LC"

    print(f"\nPrinting csv for channel {channel_name}")

    # writing to csv file
    with open(f"data/{file_name}/{file_name} {channel_name}.csv", 'w', newline="") as csvfile:
        for x in xf:
            csvfile.write(str(f"{x},"))
        csvfile.write("\n")
        #print(channel_fft_data.shape[0])
        for i in range(channel_fft_data.shape[0]):
            for y in channel_fft_data[i]:
                csvfile.write(str(f"{y}, "))
            csvfile.write("\n")

def find_highest_value(data):
    highest_val = data.max()
    #print(f"Highest value in array = {highest_val}")
    return highest_val


def print_raw_data(y_data, file_name):
    # writing to csv file
    print(y_data.shape)
    with open(f"data/{file_name}/{file_name} raw data.csv", 'w', newline="") as csvfile:
        for i in range(y_data.shape[1]):
            for j in range(y_data.shape[0]):
                csvfile.write(str(f"{y_data[j][i]},"))
            csvfile.write("\n")

