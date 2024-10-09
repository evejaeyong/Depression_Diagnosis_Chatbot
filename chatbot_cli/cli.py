import speech_recognition as sr
from gtts import gTTS
import pygame
import os

# 음성 인식 객체 생성
recognizer = sr.Recognizer()
def speak(text):
    # TTS
    tts = gTTS(text=text, lang='ko')
    tts.save("audio.mp3")

    # pygame으로 오디오 재생
    pygame.mixer.init()
    pygame.mixer.music.load("audio.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():  # 음악이 재생 중일 때까지 대기
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    # 파일 삭제
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

            try:
                # 음성을 텍스트로 변환
                text = recognizer.recognize_google(audio, language='ko-KR')
                print(f"You said: {text}")

                # 서버에서 챗봇 응답 수신
                print(f"Chatbot: {text}")

                # 챗봇 응답을 TTS로 출력
                speak(text)

            except sr.UnknownValueError:
                print("Google Web Speech API could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Web Speech API; {e}")
    except KeyboardInterrupt:
        print("Exiting...")


