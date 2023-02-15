from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
import numpy as np
import output_manager

plt.style.use('ggplot')


def Run_RFFT(file_name, data):
    duration = int(len(data.data) / data.rate)

    # Number of samples in normalized_tone
    N = data.rate * duration
    if data.data.shape[1] == 2:
        channels = 2
    else:
        channels = 1

    frames = frame_count(duration, N, channels)
    frame_duration = duration / frames

    print(f"frames selected = {frames}")
    print(f"frame samples = {N / frames}")
    print(f"frame duration = {round(frame_duration, 2)}")

    print_graphs = input(f"Would you like to print graphs? (y/n) ")

    y_data = prep_data(data, channels)

    print(f"Analysing data array of shape {y_data.shape}")

    for c in range(y_data.shape[1]):
        print(f"\nAnalysing channel {c + 1} of {y_data.shape[1]}")
        y_data_channel = y_data[:, c]
        for i in range(frames):
            print(f"{int(((i / frames) / channels) * 100)}% - frame {i}/{frames}, channel {c + 1}/{y_data.shape[1]}")

            sample_low = int(i * (N / frames))
            sample_high = int(((i + 1) * (N / frames)))

            N_frame = (N / frames)

            y_data_frame = y_data_channel[sample_low:sample_high]

            xf = rfftfreq(int(N_frame), 1 / data.rate)
            yf = rfft(y_data_frame)

            if i == 0:
                all_y_data = np.zeros(shape=(frames, int(xf.shape[0])))

            all_y_data[i] = np.abs(yf)[:int(xf.shape[0])]

        print(f"result array = {all_y_data.shape}")

        max_value = find_highest_value(all_y_data)

        for i in range(all_y_data.shape[0]):
            frame_id = round((i * frame_duration), 2)
            print(f"Printing frame {i} of {all_y_data.shape[0]} for channel {c + 1} of {channels}")
            if print_graphs == "y":
                output_manager.print_plots(xf, all_y_data[i], file_name, i, frame_id, c, max_value)
            output_manager.print_data(all_y_data[i], file_name, i, frame_id, c)


def frame_count(duration, N, channels):
    print(
        f"\nAudio file is {duration} seconds long and contains {N * channels} total samples across {channels} channel(s) ({N} samples per channel)")

    print(
        f"For 20fps, you need {duration * 20} frames\nFor 30fps, you need {duration * 30} frames\nFor 60fps, you need {duration * 60} frames")

    while True:
        frames = int(input(f"\nHow many frames would you like to produce? "))
        print(
            f"This would make each frames {round((duration / frames), 2)} seconds long (i.e. {frames / duration} fps) and contain {int(N / frames)} samples")
        confirm = input(f"Would you like to continue? (y/n) ")
        if confirm == 'y':
            return frames
        else:
            continue


def prep_data(data, channels):
    if channels == 2:
        print("Sample is stereo")

        y_data = np.zeros(shape=(data.data.shape[0], data.data.shape[1]))
        lc, rc = np.split(data.data, 2, 1)
        lc = lc.reshape(-1)
        rc = rc.reshape(-1)
        y_data[:, 0] = lc
        y_data[:, 1] = rc
        print(y_data.shape)


    else:
        print(f"Sample is mono")
        y_data = data.data
        # y_data = data.data.reshape(-1)

    return y_data


def find_highest_value(data):
    highest_val = data.max()
    print(highest_val)
    return highest_val
