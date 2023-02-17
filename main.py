import get_data, run_fft, output_manager, prep_for_fft



if __name__ == '__main__':

    file_name, data = get_data.Get_Data()

    print(f"\nFile meta-data = {data}")

    output_manager.clear_files(file_name)
    y_data, meta_data, options = prep_for_fft.pre_fft_analysis(data)

    output_manager.print_raw_data(y_data, file_name)

    fft_data, xf = run_fft.FFT_Manager(y_data, meta_data, options)

    output_manager.output_files(fft_data, xf, file_name, options, meta_data)



