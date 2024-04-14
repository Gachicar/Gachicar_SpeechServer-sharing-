## 📌 About This Project
- 자연어처리를 한 의도 분류 모델이 있는 AI SpeechServer.
- 모델을 만드는 과정은 존재하지않고, 사용할 수 있는 모델만 모아서 test 해볼 수 있는 환경임 (상대경로로 구성됨).
- 작동 과정: 클라이언트→ 메인 벡인드서버 → AI SpeechServer: 클라이언트에게서 받은 메시지를 그대로 토큰 서버에 전달, AI SpeechServer → 메인 벡인드서버: 해당 메시지가 어떤 의도인지와 함께 클라이언트에게 다시 반환할 메시지 전달, 메인백엔드 서버 → 클라이언트 : 최종 메시지 출력
- 예시) 안녕 반가워 -> 해당 내용을 백엔드 서버로 전송함.
{"intention": "인사", "response": "안녕하세요. 무엇을 도와드릴까요?", "destination": "", "date": null, "hour": 
null, "minute": null}
- 해당 내용은 처음 배우는 딥러닝 챗봇, 조경래 저, 한빛미디어 책의 코드를 수정하여 사용하였으며, 데이터도 전면적으로 수정하여 사용함. 

## 📌 Main Features
### 1️⃣ 5가지로 의도를 분류 
- intention: 인사, 욕설, 목적지, 예약, 기타
- 집으로 설정해줘
{"intention": "주문", "response": "네 알겠습니다. 목적지로 출발하겠습니다.", "destination": "집", "date": null, "hour": null, "minute": null}
- 숙입으로 가고 싶어
{"intention": "주문", "response": "네 알겠습니다. 목적지로 출발하겠습니다.", "destination": "숙입", "date": null, "hour": null, "minute": null}

### 2️⃣ 차량 이용 예약
- 음성 비서를 사용하여 목적지, 사용 일시, 이용 시간을 입력하면, 인공지능 서버에서 자연어 처리를 통해 사용자의 의도에 맞는 응답을 백엔드 서버에 전달.
- 날짜는 아무거나 해도 상관없고, 한글은 오늘, 내일, 모레, 글피, 일주일후 까지 되게 해놓음.
- 병원으로 예약하고 싶어 -> 백엔드에서 "예약하실 날짜와 시간을 말씀해주세요"
{"intention": "예약", "response": "", "destination": "병원", "date": null, "hour": null, "minute": null}  
- 3월 25일 12시 30분으로 예약해줘 -> 백엔드에서 "네 알겠습니다. 몇시간 예약하시겠습니까?" or "해당 시간은 이미 예약되어있습니다. 다른 시간을 말씀해주세요." 
 {"intention": "예약", "response": "", "destination": "", "date": "2024.03.25", "hour": "12시", "minute": "30분"}
- 오늘 12시 30분으로 예약해줘
{"intention": "예약", "response": "", "destination": "", "date": "2024.03.24", "hour": "12시", "minute": "30분"}
- 일주일후 12시 30분으로 예약해줘
{"intention": "예약", "response": "", "destination": "", "date": "2024.03.31", "hour": "12시", "minute": "30분"}
- 2시간 예약해줘 -> 벡엔드에서 "예약이 정상적으로 완료 되었습니다."
{"intention": "예약", "response": "", "destination": "", "date": null, "hour": "2시", "minute": null}

## 📌 작동방법
- 백엔드 서버를 작동하지 않고 AI SpeechServer만 작동하고 싶은 경우: 해당 레포지토리를 클론 한 후, self_test_without_backend.py를 작동하여 received_text를 바꿔가면서 테스트 하면 됨.
- 유의 사항: 아나콘다 가상환경을 따로 설정하여 테스트하는 것을 권고 (해당 레포지토리에는 pytorch와 tensorflow가 같이 다운로드 받아져 있으면 안됨, tensorflow 버전은 2.10.0 으로 사용해야함.)
- 백엔드 서버와 AI SpeechServer를 작동하고 싶은 경우: 해당 레포지토리를 클론 한 후, socket_with_backend.py 를 먼저 작동시키면 '연결을 기다리는 중' 이라는 메세지가 뜸. 그러고 백엔드 서버를 키고 안드로이드 앱을 작동하여 음성인식을 시작하면 소켓 연결이 성공할 경우 '연결이 되었습니다' 라는 메세지가 뜸.
- 유의 사항: ip 주소 와 port 설정을 자신의 구동하는 환경에 맞게 다 바꿔줘야 작동함. 
