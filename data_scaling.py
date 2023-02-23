from math import log10


def scale_data(fft_data, xf):


    fft_data = log_fft_data(fft_data)



    return fft_data, xf





def log_fft_data(fft_data):
    print(fft_data.shape)
    for c in range(fft_data.shape[0]):
        for f in range(fft_data.shape[1]):
            for b in range(fft_data.shape[2]):
                fft_data[c][f][b] = 10 * (log10(fft_data[c][f][b])**2)


    return fft_data
