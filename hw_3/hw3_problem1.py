# -*- coding: utf-8 -*-
"""
Spyder Editor
Nick Cinko
AY250 HW3 Problem 1
Goal: Make a Siri-like program (call it Monty!) 
"""
import houndify  #for speech-to-text
import pyaudio  #for recording audio
import wave
import smtplib  #for sending e-mail
from urllib.request import urlopen  #for getting html file from webpage
from bs4 import BeautifulSoup  #for making html easy to read
import my_credentials as cred  #should contain houndify/gmail credentials

#file name for recording audio
WAVE_OUTPUT_FILENAME = "file.wav"
#dictionary for converting number 'strings' into floats
numbers = {'one': 1., 'two': 2., 'three': 3., 'four': 4., 'five': 5., 'six': 6., 'seven': 7., 'eight': 8., 'nine':9., 'ten': 10.}

#function will send an e-mail to the user
def sendEmail(text, user = cred.GMAIL_USERNAME, pw = cred.GMAIL_PASSWORD):
    subj_start = text.find('subject')
    body_start = text.find('body')
    if subj_start < body_start:
        subject = text[subj_start + len('subject '): body_start - len(' and ')]
        body = text[body_start + len('body '): len(text)]
    else:
        body = text[body_start + len('body '): subj_start - len(' and ')]
        subject = text[subj_start + len('subject '): len(text)]
    msg = 'Subject: ' + subject + '\n' + body  #\n character divides subject from body
    print('email sending...')
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()  #make the gmail server play nice
    server.starttls()
    server.login(user, pw)
    server.sendmail(user, user, msg)  #sender/recipient are both the user of this python script
    print('email sent!')
    server.quit()

#function will find and print a joke from randomjoke.com    
def getJoke():
    response = urlopen("http://www.randomjoke.com/topic/oneliners.php")
    html = response.read()  #read in html data
    response.close()
    soup = BeautifulSoup(html, 'html.parser')  #make it easy to view/search with bs4
    text = soup.get_text()
    #joke is always between the words 'appropriate' and 'Over' on this webpage
    start = text.find("appropriate")
    end = text.find("Over")
    lines = text[start + len("appropriate."):end]
    for line in lines.splitlines():
        if line != '':  #get rid of empty lines between start/end words
            print(line)  #print nonempty lines (hopefully a funny joke)

#function will interpret simple arithmetic expressions and evaluate/print them            
def calculate(text):
    words = text.split()  #split string into a list of words
    for i in range(len(words)):
        if words[i] == 'times':
            print(numbers[words[i-1]]*numbers[words[i+1]])
        if words[i] == 'divided':
            print(numbers[words[i-1]]/numbers[words[i+2]])  #implicit second number after the word 'by'
        if words[i] == 'over':
            print(numbers[words[i-1]]/numbers[words[i+1]])
        if words[i] == 'plus':
            print(numbers[words[i-1]]+numbers[words[i+1]])
        if words[i] == 'minus':
            print(numbers[words[i-1]]-numbers[words[i+1]])



#function will continuously record audio until a keyboard break            
def recordAudio():
    #formatting for audio file
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    
    #Keyboard input begins recording
    input("Press any key to begin recording; press Ctrl+C to end recording")
    print("recording...")
    frames = []
    try: 
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
    #Keyboard break stops recording
    except KeyboardInterrupt:   
        print("finished recording...")
        
    #stop recording audio
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    #write audio data to file
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

#function will send audio to Houndify to perform speech-to-text magic  
def getAudioText():
    BUFFER_SIZE = 512
    # Comment from Houndify:
    # Simplest HoundListener; just print out what we receive.
    # You can use these callbacks to interact with your UI.
    class MyListener(houndify.HoundListener):
      def onPartialTranscript(self, transcript):
          pass
      def onFinalResponse(self, response):
          pass
      def onError(self, err):
        print("Error: " + str(err))
    
    
    client = houndify.StreamingHoundClient(cred.HOUNDIFY_CLIENT_ID, cred.HOUNDIFY_CLIENT_KEY, "test_user")
    input_file = wave.open(WAVE_OUTPUT_FILENAME)

    client.setSampleRate(input_file.getframerate())
    client.start(MyListener())
    
    while True:
      samples = input_file.readframes(BUFFER_SIZE)
      if len(samples) == 0: break
      if client.fill(samples): break
           
    result = client.finish() # returns either final response or error
    return result['Disambiguation']['ChoiceData'][0]['Transcription']


    
#function will perform some low-level text interpretation and choose the appropriate function/response
def interpretText(text):
    if 'calculate' in text:
        calculate(text)
    elif 'email' in text:
        sendEmail(text)
    elif 'tell' in text and 'joke' in text:
        getJoke()
    elif 'favorite color' in text:
        print('Blue. No yel-- Auuuuuuuugh!')
    else:
        print("Monty's feeling a bit shy right now.")

#function will repeat record/interpret loop until the user says goodbye to Monty            
def main(): 
    running = True
    while running:
        recordAudio()
        text = getAudioText()
        print('Monty heard : ' + text)
        if ("goodbye" in text or "good bye"  in text) and "email" not in text:  #people like to use the word goodbye in email
            running = False
            print("Monty says goodbye")
        else:
            interpretText(text)
        
        

if __name__ == "__main__":
    main()

