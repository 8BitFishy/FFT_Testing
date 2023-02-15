import get_data, run_fft, output_manager



if __name__ == '__main__':

    file_name, data = get_data.Get_Data()

    print(f"\nFile meta-data = {data}")

    output_manager.clear_files(file_name)

    run_fft.Run_RFFT(file_name, data)



