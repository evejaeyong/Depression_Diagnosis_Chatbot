# Depression_Diagnosis_Chatbot

## Server (Chatbot)
### Python version
* Python 3.12
  
```
conda install pip
pip install transformers
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia

```

"exit" 입력 시 코드 종료 후, 우울증 진단 score 출력
대화 중 3번째 답변마다 우울증 관련 질문을 시작


## Client (STT, TTS)
### Python version
* Python 3.7

```
conda install pip
pip install SpeechRecognition
pip install gtts
pip install pygame

```

현재는 마이크에서 입력을 받은대로 음성을 생성하는 식으로 구현