import get_data, run_fft



if __name__ == '__main__':

    file_name, data = get_data.Get_Data()
    print(data)



    run_fft.Run_RFFT(file_name, data)



