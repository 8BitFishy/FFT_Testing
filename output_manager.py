import csv

import matplotlib.pyplot as plt
import numpy as np
from os import path, makedirs, walk, remove

def output_files(fft_data, xf, file_name, options, folder):
    max_value = find_highest_value(fft_data)
    print(f"Printing frequency bin data")
    print_x_data(xf, file_name, folder)
    if options["print_data"] == "y":
        string_update = "csvs"
        if options['print_graphs'] == "y":
            string_update += " and graphs"
    elif options['print_graphs'] == "y":
        string_update = "graphs"
    else:
        string_update = ""

    for c in range(fft_data.shape[0]):
        print(f"Printing {string_update} for channel {c + 1} of {fft_data.shape[0]}")
        if options["print_data"] == "y":
            write_csv(fft_data[c], file_name, folder + "/fft_data", xf, c)
        printed = 0


        for i in range(fft_data.shape[1]):
            frame_id = round((i * options['frame_duration']), 2)

            if int((i / fft_data.shape[1]) * 100) % 10 == 0:
                if printed == 0:
                    print(f"{int((i / fft_data.shape[1]) * 100)}%...", end="")
                    printed = 1
            else:
                printed = 0

            if options['print_graphs'] == "y":
                print_plots(xf, fft_data[c][i], file_name, i, frame_id, folder, c, max_value)



def print_plots(xf, frame_fft_data, file_name, i, frame_id, folder, channel=0, max_value=None):
    if channel is None or channel == 0:
        channel_name = "LC"
    else:
        channel_name = "RC"

    plt.plot(xf, np.abs(frame_fft_data)[:int(xf.shape[0])])
    if max_value is not None:
        plt.ylim([0, max_value])

    plt.savefig(f'{folder}/graphs/{file_name} {channel_name} - {i} - {frame_id}.png')
    plt.cla()


def print_data(yf, file_name, i, frame_id, channel=None):
    if channel is None or channel == 0:
        channel_name = "LC"
    else:
        channel_name = "RC"

    with open(f"data/{file_name}/{file_name} {channel_name} - {i} - {frame_id}.txt", 'w') as f:
        for x in yf:
            f.write(str(f"{x}\n"))
        f.close()


def clear_files(file_name):
    folders = ["graphs", "data"]
    for i in range(len(folders)):
        for files in walk(f"{folders[i]}/{file_name}"):
            filelist = list(files[2])
            for file in filelist:
                if file_name in file:
                    remove(path.join(f"{folders[i]}/{file_name}", file))


def print_x_data(xf, file_name, folder):
    with open(f"{folder}/fft_data/{file_name} x_data.txt", 'w') as f:
        for x in xf:
            f.write(str(f"{x}\n"))
        f.close()


def write_csv(channel_fft_data, file_name, folder, xf=None, channel=None):
    if channel is None or channel == 0:
        channel_name = "LC"
    else:
        channel_name = "RC"

    # writing to csv file

    with open(f"{folder}/{file_name} {channel_name}.csv", 'w', newline="") as csvfile:
        if xf is not None:
            for x in xf:
                csvfile.write(str(f"{x},"))
            csvfile.write("\n")

        for i in range(channel_fft_data.shape[0]):
            for y in channel_fft_data[i]:
                csvfile.write(str(f"{y}, "))
            csvfile.write("\n")


def find_highest_value(data):
    if isinstance(data, list):
        highest_val = max(data)
    else:
        highest_val = data.max()
    #print(f"Highest value in array = {highest_val}")
    return highest_val


def print_raw_data(y_data, file_name, folder):
    # writing to csv file
    print(f"Printing raw wav data")
    with open(f"{folder}/wav_data/{file_name} raw data.csv", 'w', newline="") as csvfile:
        for i in range(y_data.shape[1]):
            for j in range(y_data.shape[0]):
                csvfile.write(str(f"{y_data[j][i]},"))
                csvfile.write("\n")
    csvfile.close()


def generate_folders(file_name, options):
    folder_prefix = ""
    print("\nGenerating folders")
    for value in options.values():
        if isinstance(value, float):
            value = round(value, 2)
        if isinstance(value, str):
            continue
        folder_prefix += (str(value) + "_")
    folders = ["output_data"]
    folders_2 = ["graphs", "heightmaps", "wav_data", "fft_data"]
    for i in range(len(folders)):
        for j in range(len(folders_2)):
            generate_directory(f"{folders[i]}/{file_name}_{folder_prefix.rstrip('_')}/{folders_2[j]}")
    return f"{folders[0]}/{file_name}_{folder_prefix.rstrip('_')}"

def generate_directory(directory):
    if not path.exists(directory):
        makedirs(directory)


def print_inputs(file_name, meta_data, options, folder):
    inputs = [meta_data, options]
    print("Printing input file")
    with open(f"{folder}/{file_name} inputs.txt", 'w') as f:
        for i in range(len(inputs)):
            for key, value in inputs[i].items():
                f.write(str(f"{key}:{value}\n"))
    f.close()
