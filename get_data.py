import generate_sound, read_wav


def Get_Data():
    if input("Generate sound? (y/n) ") == "y":
        file, data = generate_sound.Generate_Sound()
        print(data)

    else:
        file, data = read_wav.Get_data_From_Wav()

    return file, data