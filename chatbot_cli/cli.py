import speech_recognition as sr
from gtts import gTTS
import playsound
import os

# 음성 인식 객체 생성
recognizer = sr.Recognizer()

def speak(audio):
    #TTS
    tts = gTTS(text=audio, lang='ko')
    tts.save("audio.mp3")
    playsound.playsound("audio.mp3")
    os.remove("audio.mp3")

# 마이크를 음성 입력 소스로 사용
with sr.Microphone() as source:
    print("Adjusting for ambient noise, please wait...")
    recognizer.adjust_for_ambient_noise(source)
    print("Listening...")

    try:
        while True:
            # 음성 인식
            print("Say something!")
            audio = recognizer.listen(source)

            # Google Web Speech API를 사용하여 음성을 텍스트로 변환
            try:
                text = recognizer.recognize_google(audio, language='ko-KR')
                print(f"You said: {text}")
            except sr.UnknownValueError:
                print("Google Web Speech API could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Web Speech API; {e}")

    except KeyboardInterrupt:
        print("Exiting...")


