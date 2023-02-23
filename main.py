import get_data, run_fft, output_manager, prep_for_fft, generate_height_map, data_scaling

def main():

    file_name, data = get_data.Get_Data()
    output_manager.generate_folders(file_name)
    print(f"\nFile meta-data = {data}")

    #output_manager.clear_files(file_name)
    y_data, meta_data, options = prep_for_fft.pre_fft_analysis(data)
    output_manager.print_inputs(file_name, meta_data, options)
    output_manager.print_raw_data(y_data, file_name)



    fft_data, xf = run_fft.FFT_Manager(y_data, meta_data, options)

    #fft_data = run_fft.trim_data(fft_data, fft_data.shape[1])
    #xf = run_fft.trim_data(xf)

    data_scaling.scale_data(fft_data, xf)

    if options["print_data"] == "y":
        output_manager.output_files(fft_data, xf, file_name, options, meta_data)

    if options["print_heightmap"] == "y":
        generate_height_map.generate_height_map(fft_data, file_name)

    #if options["print_amplitude_heightmap"] == "y":
    #    generate_height_map.generate_height_map((y_data, file_name))


if __name__ == '__main__':
    main()
