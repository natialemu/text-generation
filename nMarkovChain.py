#Nathnael Alemu
import os.path
import random
import pyaudio
import speech_recognition as sr
import wave
import math
def sourceInput():
    print("Which of the follwoing would you like to use as your source: ")
    print("A.Use a text File as a Source")
    print("B.Use sound recording as a Source")
    print("C.Use Speech as input for the text")
    response = input()
    if response.lower() == "a":
        filename = input("Please provide file name you want to read from including extention: ")
        while not(os.path.exists(filename)):
            filename = input("Please provide a correct file name you want to read from including extention: ")
        with open(filename) as myfile:
            final_txt = myfile.read()
    elif response.lower() == 'b':
        wavfile = input("Provide the name of the .WAV recording file: ")
        while not(os.path.exists(wavfile)):
            wavfile = input("Please provide a correct file name of the .WAV: ")
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
        seconds = int(input("For how long would you like to record the sound: "))
        RECORD_SECONDS = seconds
        WAVE_OUTPUT_FILENAME = "output.wav"

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
        with sr.WavFile(WAVE_OUTPUT_FILENAME) as source:
            recognize = sr.Recognizer()
            recognize.energy_threshold = 600
            recognize.adjust_for_ambient_noise = 4000
            recognize.dynamic_energy_threshold = True
            recognize.dynamic_energy_adjustment_damping=0.15
            recognize.dynamic_energy_adjustment_ratio=1.5

            recognize.pause_threshold = 6
            binaryData = recognize.record(source)
        final_txt = recognize.recognize_ibm(binaryData,"b617bfe4-3700-4fe1-beb6-c9e2c1e440d5","8uacssEhEH0M")
    return final_txt

def outputToFile(order,firstFile,new_list,num_lines,num_words_line):
    index_of_ws = [i*19 for i in range(300)]
    new_listA = new_list[:]
    secondFile = ""
    for i in range(len(new_listA[:])):
        if i in index_of_ws:
            new_listA.insert(i,'\n')
    new_listA.insert(-17,'\n')
    response = input("Would you like to save the text to a file or to print it the screen? ")
    res = ["yes","save","write","file","do"]
    
    if (res[0] in response.lower() or res[1] in response.lower() or res[2] in response.lower() or res[3] in response.lower() or res[4] in response.lower()):
        filename = input("Please provide file name you want to write to including extention: ")
        with open(filename, 'w') as myfile:
            for items in new_listA:
                myfile.write(items + " ")
            print("Text has been written to %s! "%filename)
        with open(filename) as file:
            secondFile=file.read()
        vector1 = unitVector(firstFile)
        vector2 = unitVector(secondFile)
        dot_product = dotProduct(vector1,vector2)
        print()
        print("There is a %f%% correlation between the output and input files using markov model of order %d."%(dot_product*100/1,order))
    else:
        for items in new_listA:
            print(items+" ",end="")
            secondFile += items+" " 
        vector1 = unitVector(firstFile)
        vector2 = unitVector(secondFile)
        dot_product = dotProduct(vector1,vector2)
        print("\n\n")
        print("There is a %f%% correlation between the output and input files using markov model of order %d."%(dot_product*100/1,order))
def newWords(n,all_words,markov):
    new_words = []
    for order in range(n):
        new_words.append(all_words[order])
    lastKey = all_words[-n]
    for last in range(-n+1,0,1):
        lastKey += " " + all_words[last]
    list_of_keys = list(markov.keys())
    list_of_values = list(markov.values())
    for value in list_of_values:
        if ("." in value):
            markov[lastKey] = value
    i = 0
    while i < len(new_words):
        key  = new_words[i]
        for h in range(1,n):
            key += " " + new_words[i+h] 
        desired_value = ""
        if key not in list_of_keys:
            break
        if len(markov[key]) > 1:
            current_list = markov[key]
            desired_value = random.choice(current_list)
            new_words.append(desired_value)
        else:
            desired_value = markov[key][0]
            new_words.append(desired_value)
        if (len(new_words) > len(all_words)):
            break
        i += 1
    return new_words
def nMarkovChain(n,all_words):
    markov = {}
    for i in range(n,len(all_words)):
        key = all_words[i-n]
        for order in range(n-1,0,-1):
            key += " "+all_words[i-order] 
            
        value = []
        to_continue = False
        for keys,values in markov.items():
            if key == keys:
                values.append(all_words[i])
                to_continue = True
        if(to_continue):
            continue
        value.append(all_words[i])
        markov[key] = value
    return markov
def allWords(content):
    content_lines = content.split('\n')
    number_of_lines = len(content_lines)
    number_of_words_per_line = 0
    all_words = []
    for i in range(number_of_lines):
        content_words = content_lines[i].split()
        number_of_words_per_line = len(content_words)
        for j in range(len(content_words)):
            all_words.append(content_words[j])
    return [all_words,number_of_lines,number_of_words_per_line]
def unitVector(astr):
    astr = astr.lower()
    listA = [0 for k in range(26)]
    for c in astr:
        if c >= 'a' and c <= 'z':
            index = ord(c) - ord('a')
            listA[index] += 1
    sum_of_squares = 0
    for i in range(len(listA)):
        sum_of_squares += listA[i]**2
    square_root = math.sqrt(sum_of_squares)
    unit_vector = listA[:]
    for i in range(len(unit_vector)):
        unit_vector[i] = unit_vector[i]/square_root
    return unit_vector
def dotProduct(u1,u2):
    if len(u1) != len(u2):
        return
    dot_product = 0
    for i in range(len(u1)):
        dot_product += u1[i]*u2[i]
    return dot_product
def main():
    entireText=sourceInput()
    order = int(input("Please specify the order of the markov model: "))
    words_of_file=allWords(entireText)
    while(order > len(words_of_file[0])-1):
        order = int(input("Please provide an order for the markov model that is with in the word limit: "))
    all_words = words_of_file[0]
    num_lines = words_of_file[1]
    num_words_line = words_of_file[2]
    markov = nMarkovChain(order,all_words)
    print("Generating new words...")
    new_words = newWords(order,all_words,markov)
    outputToFile(order,entireText,new_words,num_lines,num_words_line)
main()
