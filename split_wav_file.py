import wavio
from os import walk, path, makedirs


def Get_data_From_Wav():
    i = 0
    print(f"Select file to open: ")
    for files in walk("wav_files"):
        filelist = list(files[2])
        for file in filelist:
            if ".wav" in file:
                print(f"{i} - {file}")
                i += 1

    file = int(input("Enter file number: "))
    print(f"{filelist[file]} selected")

    data = Read_Wav(f"wav_files/{filelist[file]}")

    return filelist[file], data


def read_meta_data(data):
    duration = int(len(data.data) / data.rate)
    sample_count = data.rate * duration
    rate = data.rate
    channels = data.data.shape[1]
    sampwidth = data.sampwidth
    return duration, sample_count, channels, rate, sampwidth


def Read_Wav(file_path):
    data = wavio.read(file_path)
    return data


def split_wav(data, parts, rate, file_name, sample_count, sampwidth, channels):
    print(data.data.shape)
    part_samples = sample_count/parts
    print(f"Part samples = {part_samples}")

    if not path.exists(f"wav_files/{file_name.strip('.wav')}"):
        makedirs(f"wav_files/{file_name.strip('.wav')}")

    for i in range(parts):
        print(f"Part {i} samples = {part_samples*(i)} - {part_samples*(i+1)}")

        part_data = data.data[int(part_samples*(i)):int(part_samples*(i+1))]

        output_part(part_data, file_name, i, rate, sampwidth)


def output_part(part_data, file_name, i, rate, sampwidth):
    wavio.write(f"wav_files/{file_name.strip('.wav')}/{file_name} part {i}.wav", part_data, rate, sampwidth=sampwidth)

def main():

    file_name, data = Get_data_From_Wav()
    duration, sample_count, channels, rate, sampwidth = read_meta_data(data)
    print(
        f"\nAudio file is {duration} seconds long\nContains {sample_count * channels} total samples\n{channels} channel(s)\n{sample_count} samples per channel")
    parts = int(input("How many parts would you like to split it into? "))

    split_wav(data, parts, rate, file_name, sample_count, sampwidth, channels)


if __name__ == '__main__':
    main()