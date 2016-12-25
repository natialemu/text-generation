import pyaudio
import speech_recognition as sr
import wave
def sourceInput():
    print("Which of the follwoing would you like to use as your source: ")
    print("A.Use a text File as a Source")
    print("B.Use sound recording as a Source")
    print("C.Use Speech as input for the text")
    response = input()
    if response == "A":
        filename=input("Please provide the file name:");
    elif response == 'B':
        wavfile = input("Provide the name of the .WAV recording file: ")
        with sr.WavFile(wavfile) as source:
            recognize = sr.Recognizer()
            recognize.energy_threshold = 600
            recognize.adjust_for_ambient_noise = 4000
            recognize.dynamic_energy_threshold = True
            recognize.dynamic_energy_adjustment_damping=0.15
            recognize.dynamic_energy_adjustment_ratio=1.5

            recognize.pause_threshold = 6
            binaryData = recognize.record(source)
        final_txt = recognize.recognize_ibm(binaryData,"b617bfe4-3700-4fe1-beb6-c9e2c1e440d5","8uacssEhEH0M")
    else:
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 15
        WAVE_OUTPUT_FILENAME = "john.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        '''with sr.WavFile(WAVE_OUTPUT_FILENAME) as source:
            recognize = sr.Recognizer()
            recognize.energy_threshold = 600
            recognize.adjust_for_ambient_noise = 4000
            recognize.dynamic_energy_threshold = True
            recognize.dynamic_energy_adjustment_damping=0.15
            recognize.dynamic_energy_adjustment_ratio=1.5

            recognize.pause_threshold = 6
            binaryData = recognize.record(source)
        final_txt = recognize.recognize_ibm(binaryData,"b617bfe4-3700-4fe1-beb6-c9e2c1e440d5","8uacssEhEH0M")'''
    #print(final_txt)
sourceInput()

