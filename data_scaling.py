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


def log_frequency_data(xf):
    new_bins = []
    for i in range(len(bins)):
        if i != 0:
            new_bin = log10(bins[i])

        else:
            new_bin = 0
        new_bins.append(new_bin)

    print(f"new bins - {new_bins}")
    print(f"New bins length = {len(new_bins)}")

    cut_down_bins = []
    bin_indices = []
    for i in range(len(new_bins)):
        if i != 0:
            if new_bins[i] - cut_down_bins[-1] > 0.2:
                cut_down_bins.append(new_bins[i])
                bin_indices.append(i)
            else:
                pass
        else:
            cut_down_bins.append(0)
            bin_indices.append(0)

    bin_indices.append(bin_count)
    print()
    new_data = []
    for f in range(1):
        current_bin = []
        bin_means = []
        for b in range(len(bin_indices) - 1):
            current_bin = []
            for i in range(bin_indices[b], bin_indices[b + 1]):
                current_bin.append(sample_data[f][i])
            bin_mean = sum(current_bin) / len(current_bin)
            bin_means.append(bin_mean)

        new_data.append(bin_means)

    print(new_data)
