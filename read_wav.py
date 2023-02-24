import wavio
from os import walk
import matplotlib.pyplot as plt
from input_validation import validate_input
plt.style.use('ggplot')

def Read_Wav(file_path):
    data = wavio.read(file_path)
    return data

def Get_data_From_Wav():
    i = 0
    inputs = []
    print(f"Select file to open: ")
    for files in walk("wav_files"):
        filelist = list(files[2])
        for file in filelist:
            if ".wav" in file:
                print(f"{i} - {file}")
                inputs.append(i)
                i += 1

    file, _ = validate_input("Enter file number", inputs, input_count=1)

    #file = int(input("Enter file number: "))

    print(f"{filelist[file]} selected")

    data = Read_Wav(f"wav_files/{filelist[file]}")

    plot_waveform, _ = validate_input("Plot waveform?")

    if plot_waveform == "y":
        plt.plot(data.data)
        plt.show()

    return filelist[file], data
