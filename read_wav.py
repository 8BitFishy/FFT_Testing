import wavio
from os import walk
import matplotlib.pyplot as plt
plt.style.use('ggplot')

def Read_Wav(file_path):
    data = wavio.read(file_path)
    return data

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

    if input("Plot waveform? (y/n) ") == "y":
        plt.plot(data.data)
        plt.show()

    return filelist[file], data
