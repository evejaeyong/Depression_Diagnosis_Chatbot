# Depression_Diagnosis_Chatbot

## Server (Chatbot)

### Python version

- Python 3.12

```
conda install pip
pip install transformers
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia

```

"exit" 입력 시 코드 종료 후, 우울증 진단 score 출력

대화 중 3번째 답변마다 우울증 관련 질문을 시작

## Client (STT, TTS)

### Python version

- Python 3.7

```
conda install pip
pip install SpeechRecognition
pip install gtts
pip install pygame

```

현재는 마이크에서 입력을 받은대로 음성을 생성하는 식으로 구현

## Ollama (Chatbot, STT, TTS)

### Python version

- Python 3.7

```
conda install pip
pip install huggingface-hub
pip install SpeechRecognition
pip install gtts
pip install pygame
pip install langchain-ollama

```

Ollama 사용으로 Chatbot을 로컬에서 작동이 가능해서 전체 코드를 합쳐서 구현

## Ollama 허깅페이스 연동

0. `pip install huggingface-hub`

1. ollama 다운로드
   https://ollama.com/download

2. 모델 다운로드 후 "Modelfile" 동레벨에 저장
   https://huggingface.co/teddylee777/EEVE-Korean-Instruct-10.8B-v1.0-gguf/blob/main/EEVE-Korean-Instruct-10.8B-v1.0-Q8_0.gguf

3. Modelfile이 있는 경로에서 `ollama create Depression-chatbot -f Modelfile` 코드 실행으로 모델 생성

4. `ollama list`로 생성된 모델 확인 가능

참고자료: https://www.youtube.com/watch?v=VkcaigvTrug&t=68s
