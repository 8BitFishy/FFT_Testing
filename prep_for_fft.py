from numpy import zeros, split
from math import ceil
from input_validation import validate_input

def select_options(duration, sample_count, channels, rate):
    print(
        f"\nAudio file is {duration} seconds long\nContains {sample_count * channels} total samples\n{channels} channel(s)\n{sample_count} samples per channel")

    print(
        f"For 20fps, you need {duration * 20} frames. This would create {ceil((sample_count / (duration * 20)) / 2)} bins at {rate / (sample_count / (duration * 20))}Hz separation\n"
        f"For 30fps, you need {duration * 30} frames. This would create {ceil((sample_count / (duration * 30)) / 2)} bins at {rate / (sample_count / (duration * 30))}Hz separation\n"
        f"For 60fps, you need {duration * 60} frames. This would create {ceil((sample_count / (duration * 60)) / 2)} bins at {rate / (sample_count / (duration * 60))}Hz separation\n")

    while True:
        frame_rate = int(input(f"What frame rate would you like? "))
        frames = frame_rate * duration
        bins = ceil((sample_count / frames) / 2)
        print(
            f"\nThis  will make {frames} frames, each {round((duration / frames), 2)} seconds long and contain {int(sample_count / frames)} samples")
        print(f"This would create {bins} bins at {rate/(sample_count / frames)}Hz separation\n")
        confirm, _ = validate_input(f"Would you like to continue?")

        if confirm == 'y':
            if channels == 2:
                analyse_both_channels, _ = validate_input("Would you like to analyse both channels?")
            else:
                analyse_both_channels = "n"
            print_graphs, _ = validate_input(f"Would you like to print graphs?")
            print_data, _ = validate_input(f"Would you like to print data?")
            print_heightmap, _ = validate_input(f"Would you like to print heightmap?")
            print_wav_heightmap, _ = validate_input(f"Would you like to print wav heightmap?")

            return frames, print_graphs, bins, print_heightmap, print_data, print_wav_heightmap, analyse_both_channels
        else:
            continue


def prep_data(data, channels, analyse_both_channels):


    if channels == 2:
        print("Sample is stereo")

        lc, rc = split(data.data, 2, 1)
        lc = lc.reshape(-1)

        if analyse_both_channels != "y":
            print("Only analysing left channel")
            print(f"Converting {data.data.shape} array to ", end="")
            y_data = lc
            print(f"{y_data.shape} array for analysis.")
            channels = 1

        else:
            print("Analysing both channels, giving array of shape ", end="")
            y_data = zeros(shape=(data.data.shape[0], data.data.shape[1]))
            channels = 2
            rc = rc.reshape(-1)
            y_data[:, 0] = lc
            y_data[:, 1] = rc
            print(f"{y_data.shape}")


    else:
        print(f"Sample is mono")
        y_data = data.data
        channels = 1
        # y_data = data.data.reshape(-1)

    return y_data, channels


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
            if i == data.data.shape[0]-1:
                print(f"Channels are identical")
    else:
        channels = 1

    frames, print_graphs, bins, print_heightmap, print_data, print_wav_heightmap, analyse_both_channels = select_options(duration, sample_count, channels, data.rate)
    frame_duration = duration / frames

    rate = data.rate
    print(f"\nFrames selected = {frames}")
    print(f"Frame samples = {sample_count / frames}")
    print(f"Frame duration = {round(frame_duration, 2)}\n")

    y_data, channels = prep_data(data, channels, analyse_both_channels)

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
        "print_data": print_data,
        "print_wav_heightmap": print_wav_heightmap
    }

    return y_data, meta_data, options
