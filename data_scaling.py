from math import log10


def scale_data(fft_data, xf):

    #fft_data = log_fft_data(fft_data)


    return fft_data, xf





def log_fft_data(fft_data):
    for c in range(fft_data.shape[0]):
        for f in range(fft_data.shape[1]):
            for b in range(fft_data.shape[2]):
                if fft_data[c][f][b] > 0:
                    fft_data[c][f][b] = 20*log10(fft_data[c][f][b])
                else:
                    pass

    return fft_data
