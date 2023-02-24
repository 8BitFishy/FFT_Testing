import get_data, run_fft, output_manager, prep_for_fft, generate_heightmap, data_scaling

def main():

    output_manager.generate_directory("wav_files")

    file_name, data = get_data.Get_Data()


    print(f"\nFile meta-data = {data}")

    #output_manager.clear_files(file_name)
    y_data, meta_data, options = prep_for_fft.pre_fft_analysis(data)
    folder = output_manager.generate_folders(file_name, options)
    output_manager.print_inputs(file_name, meta_data, options, folder)
    output_manager.print_raw_data(y_data, file_name, folder)



    fft_data, xf = run_fft.FFT_Manager(y_data, meta_data, options)

    #fft_data = run_fft.trim_data(fft_data, fft_data.shape[1])
    #xf = run_fft.trim_data(xf)

    data_scaling.scale_data(fft_data, xf)


    if options["print_data"] == "y" or options["print_graphs"] == "y":
        output_manager.output_files(fft_data, xf, file_name, options, folder)

    if options["print_heightmap"] == "y":
        generate_heightmap.generate_frequency_heightmap(fft_data, file_name, folder)

    if options["print_wav_heightmap"] == "y":
        generate_heightmap.generate_wav_heightmap_stream(y_data, file_name, folder, fft_data.shape, "wav heightmap data")

if __name__ == '__main__':
    main()
