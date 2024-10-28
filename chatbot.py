import re
from langchain_ollama import OllamaLLM
import speech_recognition as sr
from gtts import gTTS
import pygame
import os

# Ollama 모델 설정
llm = OllamaLLM(model="Depression-chatbot:latest")

messages = [
    {"role": "system", "content": "너는 일상적인 대화를 하는 한국어 챗봇이야."},
    {"role": "system", "content": "절대 혼자 질문하거나 추가적인 정보를 요청하지 마."},
    {"role": "system", "content": "답변은 항상 50자 이내로 짧고 명확하게 해줘."},
    {"role": "system", "content": "대화를 끝내지 말고 계속 이어가."},
]

# 우울증 설문 질문 리스트
depression_questions = [
    "유저의 말에 대한 답변을 하면서, 최근 2주 동안 며칠 정도 기분이 우울하거나 슬펐던 적이 있는지 질문해줘",
    "유저의 말에 대한 답변을 하면서, 최근 2주 동안 며칠 정도 평소 하던 일에 대한 흥미가 없어지거나 즐거움을 느끼지 못했는지 질문해줘",
    "유저의 말에 대한 답변을 하면서, 최근 2주 동안 며칠 정도 잠들기가 어렵거나 자주 깼거나 너무 많이 잤는지 질문해줘.",
    "유저의 말에 대한 답변을 하면서, 최근 2주 동안 며칠 정도 평소보다 식욕이 줄었거나 많이 먹었는지 질문해줘",
    "유저의 말에 대한 답변을 하면서, 최근 2주 동안 며칠 정도 다른 사람들이 눈치 챌 정도로 평소보다 말과 행동이 느려졌다거나 너무 안절부절 못해서 가만히 앉아 있을 수 없었는지 질문해줘",
    "유저의 말에 대한 답변을 하면서, 최근 2주 동안 며칠 정도 피곤하고 기운이 없었는지 질문해줘",
    "유저의 말에 대한 답변을 하면서, 최근 2주 동안 며칠 정도 내가 잘못 했거나, 실패했다는 생각이 들었는지 질문해줘.",
    "유저의 말에 대한 답변을 하면서, 최근 2주 동안 며칠 정도 신문을 읽거나 TV를 보는 것과 같은 일상적인 일에도 집중 할 수가 없었는지 질문해줘",
    "유저의 말에 대한 답변을 하면서, 최근 2주 동안 며칠 정도 차라리 죽는 것이 더 낫겠다고 생각했는지 질문해줘",
]

score_mapping = {
    # 0점 (0~1일)
    '0일': 0, '오늘': 0, '하루': 0, '1일': 0, '전혀': 0, '없었다': 0, '어제': 0, '그저께': 0, '어젯밤': 0,
    '한번도': 0, '단 하루도': 0, '아예': 0, '금방': 0, '방금': 0, '조금 전': 0, '지금 막': 0, '막': 0,

    # 1점 (2~6일)
    '2일': 1, '이틀': 1, '3일': 1, '사흘': 1, '4일': 1, '나흘': 1, '5일': 1, '6일': 1,
    '2~3일': 1, '3~4일': 1, '4~5일': 1, '5~6일': 1,
    '이번 주 초': 1, '얼마 안': 1, '며칠간': 1, '며칠 동안': 1, '며칠 전부터': 1, '며칠째': 1,
    '최근 며칠': 1, '얼마 전부터': 1, '이번 주 내내': 1, '요 며칠': 1, '한 주 내내': 1,
    '지난주에': 1, '최근에': 1, '이틀 전부터': 1, '나흘 전부터': 1, '5일 전부터': 1,

    # 2점 (7~12일)
    '7일': 2, '8일': 2, '9일': 2, '10일': 2, '11일': 2, '12일': 2, '일주일': 2, '1주': 2, '열흘': 2,
    '7~8일': 2, '8~9일': 2, '9~10일': 2, '10~11일': 2, '11~12일': 2,
    '일주일 넘게': 2, '일주일 이상': 2, '지난주부터': 2, '일주일 동안': 2, '지난 주말부터': 2,
    '지난 주 내내': 2, '열흘 넘게': 2, '열흘 동안': 2, '10일 넘게': 2, '2주 가까이': 2,
    '한참': 2, '꽤 오래': 2, '여러 날': 2, '많은 날들': 2, '최근 일주일': 2,
    '일주일 전부터': 2, '일주일째': 2, '지난 한 주 동안': 2, '며칠 이상': 2,

    # 3점 (13~14일 이상)
    '13일': 3, '14일': 3, '2주': 3, '2주일': 3, '2~3주': 3, '몇 주': 3, '보름': 3, '3주': 3,
    '매일': 3, '한 달': 3, '한달': 3, '몇 달': 3, '몇 년': 3, '작년': 3,
    '한참 전': 3, '오랫동안': 3, '오래': 3, '두 주': 3, '몇 달째': 3, '몇 년째': 3,
    '여러 달': 3, '몇 년 동안': 3, '항상': 3, '늘': 3, '지속적으로': 3, '끊임없이': 3,
    '예전부터': 3, '몇 달 전부터': 3, '몇 년 전부터': 3, '지난 달부터': 3, '언제부터인지': 3,
    '한참 동안': 3, '오랜 시간': 3, '오랜 기간': 3,
}

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

def extract_score(user_input):
    for keyword, score in score_mapping.items():
        if keyword in user_input:
            return score
    # 키워드가 없을 경우 추가 처리를 위해 정규표현식 사용
    day_pattern = r'(\d+)일'
    match = re.search(day_pattern, user_input)
    if match:
        days = int(match.group(1))
        if days < 2:
            return 0
        elif days <= 6:
            return 1
        elif days <= 12:
            return 2
        else:
            return 3
    # 해당하는 표현이 없을 경우 기본값 반환
    return 0
def format_chat(messages):
    # 메시지를 적절한 형식으로 변환
    formatted_text = ""
    for message in messages:
        if message["role"] == "system":
            formatted_text += f"{message['content']}\n"
        elif message["role"] == "user":
            formatted_text += f"사용자: {message['content']}\n"
        elif message["role"] == "assistant":
            formatted_text += f"챗봇: {message['content']}\n"
    formatted_text += "챗봇: "  # 모델이 이 부분에만 응답을 추가하도록 유도
    return formatted_text.strip()

num = 0
message_count = 0  # 메시지 카운터 초기화
depression_score = 0
recognizer = sr.Recognizer()


with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)
    try:
        while True:
            # 음성 인식
            print("You:", end=" ")
            audio = recognizer.listen(source)

            try:
                # 음성을 텍스트로 변환
                user_input = recognizer.recognize_google(audio, language='ko-KR')
                print(user_input)

                if user_input.lower() in ["exit", "quit", "종료"]:
                    print("Chatbot: 대화를 종료합니다.")
                    break

                message_count += 1  # 메시지 카운트 증가

                # 유저 메시지 추가
                messages.append({"role": "user", "content": user_input})

                # 매 3번째 대화마다 우울증 설문 프롬프트 추가
                if message_count % 3 == 0:
                    if num == 9:
                        break
                    depression_prompt = depression_questions[num]
                    messages.append({"role": "system", "content": depression_prompt})
                    num += 1

                if message_count % 3 == 1 and message_count > 1:
                    # 사용자 입력에서 날짜 관련 텍스트를 찾아서 점수 할당
                    score = extract_score(user_input)
                    depression_score += score

                # 입력 텍스트 포맷팅
                formatted_input = format_chat(messages)

                # Ollama 모델로 응답 생성
                outputs = llm.invoke(formatted_input)

                if message_count % 3 == 0:
                    messages.pop()

                # 불필요한 텍스트 제거
                decoded_response = outputs.replace("사용자:", "").replace("챗봇:", "").strip()

                if "\n" in decoded_response:
                    decoded_response = decoded_response.split("\n")[0].strip()

                print(f"Chatbot: {decoded_response}")

                # 챗봇 응답을 TTS로 출력
                speak(decoded_response)
                messages.append({"role": "assistant", "content": decoded_response})

            except sr.UnknownValueError:
                print("could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
    except KeyboardInterrupt:
        print("Exit")

print(f"End, Score is {depression_score}")