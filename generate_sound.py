import numpy as np
import matplotlib.pyplot as plt
import wavio

plt.style.use('ggplot')


def Generate_Sound():
    # sampling information
    Sample_Rate = 44100  # sample rate
    T = 1 / Sample_Rate  # sampling period
    Duration = int(input("Duration: "))  # duration (s)
    N = Sample_Rate * Duration  # total points in signal

    t_vec = np.arange(N) * T  # time vector for plotting
    y_data = 0
    file_name = ""
    channels = int(input("Channel count? (1/2) "))

    for i in range(int(input("Number of waves: "))):
        # signal information
        freq = int(input(f"Signal {i} freq: "))  # in hertz, the desired natural frequency
        volume = float(input(f"Signal {i} volume (0-1): "))
        '''
        for j in range(channels):
            
        omega = 2 * np.pi * freq  # angular frequency for sine waves
        y = y + np.sin(omega * t_vec)
        '''
        file_name += str(f"{freq}+")

        _, y = generate_sine_wave(freq, Sample_Rate, Duration)
        y_data = y_data + (y*volume)

    normalized_tone = np.int16((y_data / y_data.max()) * 32767)
    Save_Wav(normalized_tone, file_name, Sample_Rate)

    if input("Plot data? (y/n) ") == "y":
        Plot_Sound(normalized_tone)

    array = wavio._wav2array(channels, 2, normalized_tone)
    w = wavio.Wav(data=array, rate=Sample_Rate, sampwidth=2)

    return file_name, w

def Plot_Sound(y):
    plt.plot(y[:1000])
    plt.show()
    return

def Save_Wav(y, file_name, Sample_Rate):
    wavio.write(f"wav_files/{file_name}Hz.wav", y, Sample_Rate, sampwidth=2)


def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    # 2pi because np.sin takes radians
    y = np.sin((2 * np.pi) * frequencies)
    return x, y