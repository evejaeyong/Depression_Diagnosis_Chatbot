## 프로젝트 개요

이 프로젝트는 음성 기반 대화 인터페이스를 통해 **우울증 자가 진단**을 수행하는 챗봇 시스템을 구현한 것이다.  
클라이언트-서버 구조로 구성되며, 서버에서는 한국어 LLM 기반 챗봇을 구동하고, 클라이언트에서는 **음성 입력(STT)** 및 **음성 출력(TTS)** 기능을 통해 사용자가 실제로 말로 대화할 수 있도록 설계되었다.  
우울증 진단은 **PHQ-9 설문지**의 질문 항목을 기반으로 하며, 챗봇이 일상 대화 중 주기적으로 관련 질문을 자연스럽게 삽입하여 사용자의 상태를 평가한다.

## 주요 기능

- 한국어 LLM 기반 챗봇
  - 모델: `teddylee777/EEVE-Korean-Instruct-10.8B-v1.0-gguf` (SOLAR 기반 파인튜닝 모델)
  - Hugging Face에서 다운로드하여 서버에 로드
  - 일상 대화를 진행하면서 **3번째 응답마다 PHQ-9 질문 삽입**
  - 사용자의 응답에서 **날짜 관련 표현(예: '이틀')**을 추출하여 점수로 변환

- PHQ-9 기반 우울증 진단
  - 9개의 표준 질문 항목 중 무작위로 1개를 선택해 주기적으로 질문
  - 사용자 답변 내 텍스트를 매핑하여 0~3점으로 스코어링
  - 누적 점수 기반 우울증 위험도 평가 가능

- 음성 기반 대화 인터페이스
  - **STT (Speech-to-Text)**:
    - 라이브러리: `speech_recognition`
    - 엔진: Google Web Speech API
    - 실제 사용자 테스트 결과 양호한 인식 성능 확인
  - **TTS (Text-to-Speech)**:
    - 라이브러리: `gTTS` (Google Text-to-Speech)
    - 텍스트 응답을 음성으로 자연스럽게 변환하여 출력

- 네트워크 구조
  - **Socket 통신 기반 클라이언트-서버 구조**
  - 클라이언트: STT 입력, TTS 출력 처리
  - 서버: LLM 응답 생성, PHQ-9 논리 포함

## 사용 기술

- 언어: Python
- 라이브러리:
  - `speech_recognition`, `gTTS`
  - `socket`, `re`, `datetime` 등
- 모델: Hugging Face LLM (`EEVE-Korean-Instruct-10.8B`)
- 구조: 클라이언트-서버 통신 기반 설계 (TCP 소켓)
- 플랫폼: Ubuntu / Windows 환경 모두 테스트함.
