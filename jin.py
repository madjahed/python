
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime


# настройки
opts = {
    "alias": ('джин','джинни', 'джи', 'друг'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси', 'открой'),
    "cmds": {
        "internet": ('браузер','хром','интернет'),
        "ctime": ('текущее время','сейчас времени','который час'),
        "radio": ('включи музыку','воспроизведи радио','включи радио'),
        "stupid1": ('расскажи анекдот','рассмеши меня','ты знаешь анекдоты')
    }
}

# функции
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано: " + voice)
    
        if voice.startswith(opts["alias"]):
            #к помощнику
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()
            
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
            
            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    
    return RC

def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + " часа : " + str(now.minute) + " минут")
 
    elif cmd == 'radio':
        # воспроизвести радио
        os.system("D:\\Jarvis\\music\\cold_-_remedy-album-version.mp3")
        
    elif cmd == 'stupid1':
        # рассказать анекдот
        speak("Ты делаешь вопросно-ответную систему через if")
    elif cmd == 'internet':
        # открыть браузер
        os.system("D:\\Jarvis\\chrome.lnk")   
        #speak("Пожалуйста!")

    else:
        print('Команда не распознана, повторите!')

# запуск

r = sr.Recognizer()
m = sr.Microphone(device_index = 18)
with m as source:
    r.adjust_for_ambient_noise(source)
speak_engine = pyttsx3.init()
# Только если у вас установлены голоса для синтеза речи!
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[4].id)
speak("Привет, создатель")
speak("Джинни слушает")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop