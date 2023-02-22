from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
import numpy as np
from math import log10
import output_manager

plt.style.use('ggplot')

def FFT_Manager(y_data, meta_data, options):
    fft_data = np.zeros(shape=(meta_data['channels'], options['frames'], options['bins']))

    for c in range(y_data.shape[1]):
        print(f"\nAnalysing channel {c + 1} of {y_data.shape[1]}")
        xf, channel_fft_data = Run_RFFT(y_data, meta_data, options)
        print(channel_fft_data.shape)


        fft_data[c] = channel_fft_data

    print(f"\nFFT produced an array of shape {fft_data.shape}\n")


    return fft_data, xf



def Run_RFFT(channel_data, meta_data, options):


        #y_data_channel = y_data[:, c]

        channel_fft_data = np.zeros(shape=(options['frames'], options['bins']))

        #print(f"Channel data shape = {channel_data.shape}")
        #print(f"Channel_fft_data shape = {channel_fft_data.shape}")

        printed = 0

        for i in range(options["frames"]):
            #print(f"{int(((i / frames) / channels) * 100)}% - frame {i}/{frames}, channel {c + 1}/{y_data.shape[1]}")
            if int(((i / options["frames"]) / meta_data["channels"]) * 100) % 10 == 0:
                if printed == 0:
                    print(f"{int(((i / options['frames']) / meta_data['channels']) * 100)}%...", end="")
                    printed = 1
            else:
                printed = 0

            sample_low = int(i * (meta_data['sample_count'] / options['frames']))
            sample_high = int(((i + 1) * (meta_data['sample_count'] / options['frames'])))

            samples_in_frame = (meta_data['sample_count'] / options['frames'])

            y_data_frame = channel_data[sample_low:sample_high]
            #print(f"y_data_frame shape = {y_data_frame.shape}")
            xf = rfftfreq(int(samples_in_frame), 1 / meta_data['rate'])

            yf = rfft(y_data_frame.reshape(-1))
            #print(f"yf shape = {yf.shape}")

            channel_fft_data[i] = np.abs(yf)[:options['bins']].flatten()
            for j in range(len(channel_fft_data[i])):
                channel_fft_data[i][j] = log10(channel_fft_data[i][j])

            xf = xf[:options['bins']]


            #plt.plot(xf, np.abs(channel_fft_data[i])[:int(xf.shape[0])])
            #plt.show()

        print(f"\nresult array = {channel_fft_data.shape}")

        return xf, channel_fft_data


def trim_data(data):
    if data.ndim != 1:
        for c in range(data.shape[0]):
            print(f"Trimming array from shape {data.shape}")
            trimmed_data = np.delete(data, 0, 1)
            print(f"Trimmed array shape {trimmed_data.shape}")


    else:
        print(f"Trimming array from shape {data.shape}")
        trimmed_data = np.delete(data, 0)
        print(f"Trimmed array shape {trimmed_data.shape}")

    return trimmed_data