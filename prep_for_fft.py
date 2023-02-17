from numpy import zeros, split
from math import ceil

def select_options(duration, sample_count, channels, rate):
    print(
        f"\nAudio file is {duration} seconds long\nContains {sample_count * channels} total samples\n{channels} channel(s)\n{sample_count} samples per channel")

    print(
        f"For 20fps, you need {duration * 20} frames. This would create {ceil((sample_count / (duration * 20)) / 2)} bins at {rate / (sample_count / (duration * 20))}Hz separation\n"
        f"For 30fps, you need {duration * 30} frames. This would create {ceil((sample_count / (duration * 30)) / 2)} bins at {rate / (sample_count / (duration * 30))}Hz separation\n"
        f"For 60fps, you need {duration * 60} frames. This would create {ceil((sample_count / (duration * 60)) / 2)} bins at {rate / (sample_count / (duration * 60))}Hz separation\n")

    while True:
        frames = int(input(f"\nHow many frames would you like to produce? "))
        bins = ceil((sample_count / frames) / 2)
        print(
            f"\nThis makes each frame {round((duration / frames), 2)} seconds long ({frames / duration} fps) and contain {int(sample_count / frames)} samples")
        print(f"This would create {bins} bins at {rate/(sample_count / frames)}Hz separation\n")
        confirm = input(f"Would you like to continue? (y/n) ")

        if confirm == 'y':
            print_graphs = input(f"Would you like to print graphs? (y/n) ")
            print_data = input(f"Would you like to print data? (y/n) ")
            print_heightmap = input(f"Would you like to print heightmap? (y/n) ")

            return frames, print_graphs, bins, print_heightmap, print_data
        else:
            continue


def prep_data(data, channels):


    if channels == 2:
        print("Sample is stereo")

        y_data = zeros(shape=(data.data.shape[0], data.data.shape[1]))
        lc, rc = split(data.data, 2, 1)
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


def pre_fft_analysis(data):

    duration = int(len(data.data) / data.rate)

    # Number of samples in normalized_tone
    sample_count = data.rate * duration
    if data.data.shape[1] == 2:
        channels = 2
        for i in range(data.data.shape[0]):
            if data.data[i][0] != data.data[i][1]:
                print(f"Channels vary from {i} - {data.data[i][0]} != {data.data[i][1]}")
                break
            if i == range(data.data.shape[0])-1:
                print(f"Channels are identical")
    else:
        channels = 1

    frames, print_graphs, bins, print_heightmap, print_data = select_options(duration, sample_count, channels, data.rate)
    frame_duration = duration / frames

    rate = data.rate

    print(f"frames selected = {frames}")
    print(f"frame samples = {sample_count / frames}")
    print(f"frame duration = {round(frame_duration, 2)}")


    y_data = prep_data(data, channels)

    print(f"Analysing data array of shape {y_data.shape}")

    meta_data = {
        "duration": duration,
        "sample_count": sample_count,
        "rate": rate,
        "channels": channels
    }

    options = {
        "frames": frames,
        "bins":bins,
        "frame_duration":frame_duration,
        "print_graphs": print_graphs,
        "print_heightmap": print_heightmap,
        "print_data": print_data
    }

    return y_data, meta_data, options
