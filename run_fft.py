from scipy.fft import fft, fftfreq, rfft, rfftfreq
import matplotlib.pyplot as plt
import numpy as np
from os import walk, path, remove

plt.style.use('ggplot')


def Run_FFT(filename, data):

    # Number of samples in normalized_tone
    N = int(data.rate * (len(data.data)/data.rate))
    print(data.data.reshape(-1))
    yf = fft(data.data.reshape(-1))

    xf = fftfreq(N, 1 / data.rate)
    plt.plot(xf, np.abs(yf))
    plt.show()


def Run_RFFT(file_name, data):
    duration = int(len(data.data)/data.rate)
    print(f"duration = {duration}")
    batches = duration * 30
    print(f"Batches = {batches}")
    # Number of samples in normalized_tone
    N = data.rate * duration
    print(f"Batch samples = {N/batches}")

    clear_graph_files(file_name)

    if data.data.shape[1] == 2:
        lc, rc = np.split(data.data, 2, 1)
        y_data = lc
        print(y_data)
        y_data = y_data.reshape(-1)
        print(y_data)


    else:
        y_data = data.data.reshape(-1)


    for i in range(batches):
        sample_low = int(i * (N/batches))
        sample_high = int(((i+1) * (N/batches)))
        print(f"{i}/{batches} - samples {sample_low} - {sample_high} of {N}")

        N_batch = (N/batches)
        y_data_batch = y_data[sample_low:sample_high]
        '''
        print("Batch data: ")
        print(y_data_batch.shape)
        print(N_batch)
        '''
        xf = rfftfreq(int(N_batch), 1 / data.rate)
        yf = rfft(y_data_batch)
        '''
        print("FFT data shape")
        print(yf.shape)
        print(xf.shape)
        '''

        plt.plot(xf, np.abs(yf)[:int(xf.shape[0])])
        plt.savefig(f'graphs/{file_name} - {i}.png')
        plt.cla()
        #plt.show()


def clear_graph_files(file_name):
    for files in walk("graphs"):
        filelist = list(files[2])
        for file in filelist:
            if file_name in file:
                dir = path.join(f"graphs/", file)
                remove(dir)