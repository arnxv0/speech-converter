# pyinstaller.exe --onefile -w --hidden-import=pyaudio --hidden-import=google-cloud-speech --hidden-import=google-api-python-client App.py
# pyinstaller.exe App.py
# pyinstaller.exe --icon=icon.ico -w RobotVoice.py
# pyinstaller.exe -w RobotVoice.py

# Python program to translate
# speech to text and text to speech
# https://pypi.org/project/pynput/
# https://www.reddit.com/r/Python/comments/bdcz7m/the_exe_module_aint_doing_fine/

# https://vb-audio.com/Voicemeeter/index.htm
# https://rogueamoeba.com/loopback/
# https://www.planetradiocity.com/how-to-play-desktop-audio-through-mic
# https://vb-audio.com/Cable/index.htm

import speech_recognition as sr
import pyttsx3 

# install pyaudio
# pip install sounddevice
# pip install google-cloud-speech
# pip install google-api-python-client


# Initialize the recognizer 
r = sr.Recognizer() 
  
# Function to convert text to
# speech
def SpeakText(command):
    
    # Initialize the engine
    engine = pyttsx3.init()
    voiceId = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\IVONA 2 Voice Justin22"
    engine.setProperty('voice', voiceId)
    engine. setProperty("rate", 178)
    engine.say(command)
    # voices = engine.getProperty('voices')
    # for voice in voices:
    #     engine.setProperty('voice', voice.id) # changes the voice
    #     print(voice.id)  
    #     engine.say(command)
    engine.runAndWait()

      
# Loop infinitely for user to
# speak

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
  
while(1):
    # Exception handling to handle
    # exceptions at the runtime
    print("======Start======")
    try:
          
        # use the microphone as source for input.
        # with sr.Microphone(device_index=15) as source2:
        with sr.Microphone() as source2:
            
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level 
            r.adjust_for_ambient_noise(source2, duration=3)
              
            #listens for the user's input 
            audio2 = r.listen(source2)
            print("======Stop======")
            
            # Using ggogle to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
  
            print(MyText)
            SpeakText(MyText)
              
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
          
    except sr.UnknownValueError:
        print("unknown error occured")
    
    except Exception as e:
        print(e)




# import pyttsx3

# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# engine.setProperty('rate', 80)
# for voice in voices:
#    engine.setProperty('voice', voice.id)
#    engine.say('<pitch middle="10">Hello there! I am Friday</pitch>')
# engine.runAndWait()