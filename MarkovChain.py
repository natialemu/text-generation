import os.path
import random
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
        filename = input("Please provide file name you want to read from including extention: ")
        while not(os.path.exists(filename)):
            filename = input("Please provide a correct file name you want to read from including extention: ")
        with open(filename) as myfile:
            final_txt = myfile.read()
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
        RECORD_SECONDS = 10
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

def outputToFile(firstFile,new_list,num_lines,num_words_line):
    #print("The length of new_list is",len(new_list))
    index_of_ws = [i*19 for i in range(300)]
    new_listA = new_list[:]
    secondFile = ""
    for i in range(len(new_listA[:])):
        if i in index_of_ws:
            new_listA.insert(i,'\n')

    print(len(new_listA))
    response = input("Would you like to save the text to a file or to print it the screen? ")
    res = ["yes","save","write","file","do"]
    
    if (res[0] in response.lower() or res[1] in response.lower() or res[2] in response.lower() or res[3] in response.lower() or res[4] in response.lower()):
        filename = input("Please provide file name you want to write to from including extention: ")
        with open(filename, 'w') as myfile:
            for items in new_listA:
                myfile.write(items + " ")
            
            '''i = 0
            num_words_line = 19
            for number_lines in range(num_lines):
                while i < num_words_line and i < len(new_list):# try having a max of 19 characters
                    myfile.write(new_list[i] + " ")
                    i += 1
                myfile.write("\n")
                i += 19
                num_words_line += 19
                #print(i)'''
            print("Text has been written to %s! "%filename)
        with open(filename) as file:
            secondFile=file.read()
        vector1 = unitVector(firstFile)
        vector2 = unitVector(secondFile)
        dot_product = dotProduct(vector1,vector2)
        print("There is a %f%% correlation between the output and input files."%(dot_product*100/1))
            
    else:
        for items in new_listA:
            print(items+" ",end="")
            secondFile += items+" " 
        vector1 = unitVector(firstFile)
        vector2 = unitVector(secondFile)
        dot_product = dotProduct(vector1,vector2)
        print("There is a %f%% correlation between the output and input files."%(dot_product*100/1))

        '''for number_lines in range(num_lines):
            i = 0
            while i < num_words_line and i < len(new_list):
                print(new_list[i] + " ",end="")
                i += 1
            print()
            i += num_words_line
            num_words_line += num_words_line'''
            
def newWords(all_words,markov):
    new_words = []
    new_words.append(all_words[0])
    new_words.append(all_words[1])
    lastKey = all_words[-2] + " " + all_words[-1]
    list_of_keys = list(markov.keys())
    list_of_values = list(markov.values())
    i = 0
    while i < len(new_words):
        key = new_words[i] + " " + new_words[i+1]#try to solve the problem of not finding a key! by, for eg, not accessing the last word or accesing it rarely.
        desired_value = ""
        if (key == lastKey):
            continue
        if key not in list_of_keys:
            #print("About to break!")
            break
        if len(markov[key]) > 1:
            current_list = markov[key]
            desired_value = random.choice(current_list)
            new_words.append(desired_value)
            #print("THERE ARE SOME!!!")
        else:
            '''if list_of_values.count(markov[key]) > 1:# if you have multiple values the goal is to use their key
              
                desired_value = markov[key][0]
                new_words.append(desired_value)
                identical_keys = []
                for keys,values in markov.items():
                    if markov[key] == values:
                        identical_keys.append(keys)
                second_word_of_keys = []
                for each_key in identical_keys:
                    second_word = each_key.split()
                    second_word_of_keys.append(second_word[1])
                key1 = random.choice(second_word_of_keys)
                key_tobe_used = key1 + " " + desired_value
                desired_value = markov[key_tobe_used][0]
                new_words.append(desired_value)
                ## get the index of all of all of the values(which are lists)
                ## concatenate the lists to get a new list of all the values
                ##randomly select from that list and assign that to desired_value and append it to new_words'''
             
            desired_value = markov[key][0]
            new_words.append(desired_value)
            ## get the value from the list
            ## append it to desired_value and append that to new_words
        if (len(new_words) > 1000):
            #print("Exceeded word limit")
            break
        i += 1
    return new_words
    ##return the new list
            
            
        
def markovChain(all_words):
    markov = {}
    for i in range(2,len(all_words)):
        key = all_words[i-2] + " " + all_words[i-1]
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
def dataMining():
    file1 = 'moby.txt'
    file2 = 'PrideAndPredjudiceChap1-3.txt'
    vector1 = unitVector(file1)
    vector2 = unitVector(file2)
    dot_product = dotProduct(vector1,vector2)
    print("There is a %f%% correlation between %s and %s"%(dot_product*100/1,file1,file2))
    # a correlation of 1 or 100% means the two files are very simillar while a correlation of
    # 0 means they have no simillarity
    print("-------------------------------------------------------------------------")
def main():
    entireText=sourceInput()#depending on what source the user chose add a new line character at several points
    words_of_file=allWords(entireText)
    all_words = words_of_file[0]
    num_lines = words_of_file[1]
    num_words_line = words_of_file[2]
    markov = markovChain(all_words)
    new_words = newWords(all_words,markov)
    print(all_words)
    print()
    print(markov)
    print()
    print(new_words)
    outputToFile(entireText,new_words,num_lines,num_words_line)
main()
