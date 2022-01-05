import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from random import randint
from pynput import keyboard

import pyaudio
import sounddevice

################################### Speech Stuff ###############################################

import pyttsx3
import speech_recognition as sr

r = sr.Recognizer()

# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

engine = pyttsx3.init()

voices = engine.getProperty('voices')
voices_list = []
for idx, voice in enumerate(voices):
    voices_list.append((f"Voice {idx + 1}", voice.id))


##################################### talkting stuff #########################################
root = ttk.Window(themename="cyborg")
root.title("Voice Bot")

lbl_heading = ttk.Label(root, text="Voice Changer", font=('Lato',15), bootstyle="info")
lbl_heading.grid(row=0, column=0, padx=20, columnspan=2, pady=(30,20))

# voices_list = ["Justin", "Jarvis", "Friday"]
modified_voices_list = [ele[0] for ele in voices_list]
current_voice = ttk.StringVar(value=modified_voices_list[0])
cbo_voice = ttk.Combobox(root, textvariable=current_voice, values=modified_voices_list, width=20, bootstyle="info")
cbo_voice.grid(row=1, column=0, columnspan=2, padx=(25,60), pady=(10,30))

mtr_speed = ttk.Meter(metersize=230, padding=5, amountused=90, metertype="semi", subtext="Speed", interactive=True, bootstyle="primary")
mtr_pitch = ttk.Meter(metersize=230, padding=5, amountused=75, metertype="semi", subtext="Pitch", interactive=True, bootstyle="warning")

mtr_speed.grid(row=2, column=0, padx=(60,25))
mtr_pitch.grid(row=2, column=1, padx=(25,60))

lbl_volume = ttk.Label(root, text="Volume", font=('Lato',10), bootstyle="info")
lbl_volume.grid(row=3, column=0, padx=50, columnspan=2)

volume = ttk.IntVar(value=100)
scl_volume = ttk.Scale(root, orient=HORIZONTAL, variable=volume, length=800, from_=0, to=100, bootstyle="info")
scl_volume.grid(row=4, column=0, columnspan=2, pady=(10,20), padx=(50,50))

mtr_voice = ttk.Meter(metersize=150, padding=5, amountused=0, metertype="full", subtext="Standby", interactive=False, bootstyle="success")
mtr_voice.grid(row=5, column=0, padx=(20,20), pady=(0,20))

ent_text = ttk.Text(root, width=35, height=6)
ent_text.grid(row=5, column=1, padx=(0,100), pady=(0,0))


def getSpeedLevel():
    return mtr_speed.amountusedvar.get()

def getPitchLevel():
    return mtr_pitch.amountusedvar.get()

def getVoiceLevel():
    return mtr_voice.amountusedvar.get()

def setVoiceLevel(speed):
    mtr_voice.configure(amountused = speed)

def getVoiceName():
    return current_voice.get()

def getVolumeLevel():
    return volume.get()

def getText():
    return ent_text.get('1.0', END)

def clearText():
    ent_text.delete('1.0', END)

# def setRandomVoiceLevel():
#     voice_level = getVoiceLevel() + randint(-5,5)
#     if voice_level < 0:
#         voice_level = 0
#     elif voice_level > 100:
#         voice_level = 100
#     setVoiceLevel(voice_level)


def SpeakText(command, voiceIdx, pitch, speed, volume):
    engine.setProperty("voice", voices_list[voiceIdx][1])
    engine. setProperty("rate", speed)
    engine. setProperty("volume", volume)
    engine.say(command)
    ent_text.replace('1.0', END, command)
    engine.runAndWait()

def speakBtnCommand(text):
    voiceIdx = int(getVoiceName().split(" ")[1]) - 1
    speed = getSpeedLevel()
    vol = int(getVolumeLevel()) / 100
    SpeakText(text, voiceIdx, 0, speed, vol)

def readText():
    mtr_voice.configure(subtext="Outputing...", amountused=100)
    speakBtnCommand(getText())
    mtr_voice.configure(subtext="Standby", amountused=0)

def startBtnCommand():
    noiseDuration = 3
    # print("======Start======")

    mtr_voice.configure(subtext="Loading...", amountused=0)
    mtr_voice.step(10)
    mtr_voice.step(10)
    mtr_voice.step(10)

    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=noiseDuration)
            mtr_voice.configure(subtext="Speak", amountused=100)

            audio2 = r.listen(source2)

            mtr_voice.configure(subtext="Analysing...", amountused=100)
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            # print(MyText)
            mtr_voice.configure(subtext="Outputing...", amountused=100)
            speakBtnCommand(MyText)
            mtr_voice.configure(subtext="Standby", amountused=0)
            
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        mtr_voice.configure(subtext="Try again", amountused=0)
        
    except sr.UnknownValueError as e:
        print(f"unknown error occured: {e}")
        mtr_voice.configure(subtext="Try again", amountused=0)
    
    except Exception as e:
        print(e)
        mtr_voice.configure(subtext="Try again", amountused=0)


BTN_WIDTH = 30
# btn_listen = ttk.Button(root, text="Start", command=startBtnCommand, width=BTN_WIDTH, bootstyle="primary")
# btn_listen.grid(row=6, column=0, pady=(0,100), ipady=10)


btn_speak = ttk.Button(root, text="Read", command=readText, width=BTN_WIDTH, bootstyle="warning")
btn_speak.grid(row=6, column=1, padx=(0,100), pady=(0,100), ipady=10)


# def task():
#     # print(getSpeedLevel())
#     # print(getPitchLevel())
#     # print(getVolumeLevel())
#     # print(getText())
#     # print(getVoiceName())
#     setRandomVoiceLevel()

#     root.after(200, task)  # run task function every 200 miliscecs


# root.after(200, task)

################################### Keyboard stuff ###############################################

# voices_list = ["Justin", "Jarvis", "Friday"]
shotcutList = ["Key.f1", "Key.f2", "Key.f3", "Key.f4"]
currentShotcut = ttk.StringVar(value=shotcutList[0])
shotCutKeyDropDown = ttk.Combobox(root, textvariable=currentShotcut, values=shotcutList, width=30, bootstyle="info")
shotCutKeyDropDown.grid(row=6, column=0, pady=(0,0))

def on_press(key):
    try:
        # print('alphanumeric key {0} pressed'.format(key.char))
        # print(str(key.char))
        if(currentShotcut.get() == key.char):
            startBtnCommand()
    except AttributeError:
        # print('special key {0} pressed'.format(key))
        # print(key)
        # print(currentShotcut.get())
        if(currentShotcut.get() == str(key)):
            startBtnCommand()

def on_release(key):
    pass
    # print('{0} released'.format(key))
    # if key == keyboard.Key.esc:
    #     # Stop listener
    #     return False

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

root.mainloop()