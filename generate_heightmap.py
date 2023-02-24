from PIL import Image
import numpy as np
import output_manager


def generate_frequency_heightmap(data, file_name, folder):
    modifier = "frequency heightmap data"
    max_value = output_manager.find_highest_value(data)
    for c in range(data.shape[0]):
        if c == 1:
            channel_name = "RC"
        else:
            channel_name = "LC"

        print(f"\nGenerating {channel_name} {modifier}")
        mapped_data = generate_heightmap(data[c], file_name, folder, modifier, max_value, channel_name)
        print(f"Printing {channel_name} heightmap csv file")
        output_manager.write_csv(mapped_data, file_name + modifier, folder + "/heightmaps", channel=c)

        print(f"Printing {channel_name} heightmap stream")

        for f in range(data.shape[1]):
            frame_data = np.zeros(shape=(data.shape[2], data.shape[2]))
            for b in range(data.shape[2]):
                for h in range(data.shape[2]):
                    frame_data[h][b] = data[c][f][b]

            generate_heightmap(frame_data, file_name, folder, modifier + f" {f}", max_value,
                                                 channel_name, sub_folder="frequency_sequence/")


def generate_heightmap(data, file_name, folder, modifier, max_value, channel_name, sub_folder=""):

    mapped_data = np.zeros(shape=(data.shape[0], data.shape[1]))

    for f in range(data.shape[0]):
        for v in range(data.shape[1]):
            mapped_data[f][v] = int((data[f][v] / max_value) * 255)


    mapped_data = np.uint8(mapped_data)

    img = Image.fromarray(mapped_data, 'L')
    
    #img.show()
    
    output_manager.generate_directory(f"{folder}/heightmaps/{sub_folder}")
    img.save(f"{folder}/heightmaps/{sub_folder}{file_name} {modifier} {channel_name}.png")

    return mapped_data



def generate_wav_heightmap_stream(y_data, file_name, folder, data_shape, modifier, width=10, height=10):


    wav_data = np.zeros(shape=(data_shape[0], data_shape[1], 1))

    frame_range = int(y_data.shape[0] / data_shape[1])
    mean_amps = []
    for i in range(data_shape[1]):
        mean_amp = sum(y_data[(i*frame_range):((i+1)*frame_range)])/frame_range
        mean_amps.append(mean_amp)

    max_value = output_manager.find_highest_value(mean_amps)

    for c in range(data_shape[0]):
        if c == 1:
            channel_name = "RC"
        else:
            channel_name = "LC"

        print(f"Printing {channel_name} wav heightmap image sequence")

        for f in range(data_shape[1]):
            frame_data = np.zeros(shape=(height, width))
            for b in range(width):
                for h in range(height):
                    frame_data[b][h] = mean_amps[f]

            mapped_data = generate_heightmap(frame_data, file_name, folder, modifier + f" {f}", max_value, channel_name, sub_folder="wav_sequence/")

            wav_data[c][f] = int(mapped_data[0][0])

        print(f"Printing {channel_name} wav heightmap data")
        output_manager.write_csv(wav_data[c], file_name + modifier, folder + "/heightmaps", channel=c)

    return
