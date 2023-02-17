from math import ceil



def data_processing(file_name):
    fft_data = {
    "frames" : None,
    "bins" : [],
    "data" : []
    }
    file_data = []
    with open(file_name, "r") as file:
        for line in file:
            file_data.append(line.strip().split(","))

    for i in range(len(file_data)):
        for j in range(len(file_data[i])):
            file_data[i][j] = float(file_data[i][j])


    fft_data["bins"] = file_data.pop(0)
    fft_data["frames"] = len(file_data)
    fft_data["data"] = file_data
    for key, value in fft_data.items():
        print(key, value)
    return fft_data



def data_clumping_inputs(fft_data):
    print(f"\nDatafile contains {fft_data['frames']} frames with {len(fft_data['bins'])} bins of {fft_data['bins'][1] - fft_data['bins'][0]}Hz spacing")
    while True:
        bins = int(input(f"How many bins would you like to reduce these to? "))
        ratio = len(fft_data['bins'])/bins
        print(f"Ratio = {ceil(ratio)}")
        print(f"This will result in {bins} new bins of {(fft_data['bins'][1] - fft_data['bins'][0]) * ratio}Hz spacing, each covering {float(len(fft_data['bins']) / bins)} old bins")
        if input("Would you like to continue? (y/n) ") == "y":
            break

    print(f"Continuing with {bins} data clumps")
    return ratio, bins

def data_clumping(data, ratio):
    print(f"data reduction ratio = 1:{int(ceil(ratio))}")
    new_data = []
    for i in range(0, len(data), int(ceil(ratio))):
        data_mean = []
        #print("Looping i")
        try:
            for j in range(int(ceil(ratio))):
                #print(f"i = {i}, j = {j}, i+j = {i+j}")
                data_mean.append(data[i+j])
                print(data_mean)
        except IndexError:
            pass

        new_data.append((sum(data_mean)/len(data_mean)))

    print(new_data)
    return new_data




if __name__ == '__main__':
    fft_data = data_processing("fft_data_sample.csv")

    ratio, bins = data_clumping_inputs(fft_data)


    print(f"\nClumping bins")
    fft_data_reduced = {"frames": fft_data["frames"], "bins": data_clumping(fft_data['bins'], ratio), "data": []}
    print("\nClumping data")
    for i in range(fft_data_reduced["frames"]):
        fft_data_reduced["data"].append(data_clumping(fft_data['data'][i], ratio))
    print(fft_data_reduced)


