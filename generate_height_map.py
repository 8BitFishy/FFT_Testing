from PIL import Image
import numpy as np
import output_manager

def generate_height_map(fft_data, file_name):
    #width = len(fft_data.shape[1])
    #height = len(fft_data.shape[2])
    max_value = output_manager.find_highest_value(fft_data)


    for c in range(fft_data.shape[0]):
        mapped_data = np.zeros(shape=(fft_data.shape[1], fft_data.shape[2]))

        if c == 1:
            channel_name = "RC"
        else:
            channel_name = "LC"


        # gradient between 0 and 1 for 256*256
        #fft_data[c] = np.linspace(0, max_value, 256 * 256)

        # reshape to 2d
        #mat = np.reshape(fft_data[c], (256, 256))

        print(f"\nGenerating {channel_name} heightmap")
        print(f"Mapping array of shape {fft_data.shape}")

        for f in range(fft_data.shape[1]):
            for v in range(fft_data.shape[2]):
                mapped_data[f][v] = int((fft_data[c][f][v] / max_value) * 255)
                '''if fft_data[c][f][v] > max_value-1000:
                    print("HERE_____________________________________")
                print(f"Value {fft_data[c][f][v]} mapped to {mapped_data[f][v]}")
                '''
        #scaled_array = np.uint8(fft_data[c] * 255)

        print(f"Scaled array of shape {mapped_data.shape}")

        output_manager.write_csv(mapped_data, mapped_data[0], file_name)
        # Creates PIL image
        img = Image.fromarray(mapped_data, 'L')
        #img.show()




        #img = Image.fromarray(fft_data[c], 'BW')
        img.save(f"data/{file_name}/{file_name} {channel_name} heightmap.png")