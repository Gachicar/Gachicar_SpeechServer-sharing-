from socket import *
from utils.Preprocess import Preprocess
from models.intent.IntentModel import IntentModel
from models.ner.NerModel import NerModel
import json
from datetime import datetime, timedelta

# 현재 년도 받아오기
current_year = datetime.now()
# Preprocess 객체 초기화
p = Preprocess(word2index_dic='chatbot_dict.bin',
               userdic='user_dic3.tsv')
# IntentModel 초기화
intent = IntentModel(model_name='intent_model.h5', proprocess=p)

# NerModel 초기화 
ner = NerModel(model_name='ner_model.h5', proprocess=p)

# 데이터 입력 (테스트를 위해 직접 입력)
received_text = "오늘 12시 35분으로 예약해줘"

response_data = {}

if not received_text.strip():  # 받은 메시지가 빈 문자열인 경우
    response = "잘 이해하지 못했습니다. 다시한번 말씀해주세요."
    response_data = {
        "intention": "불명확",
        "response": response,
        "destination": "",
        "date": None,  
        "hour": None,
        "minute": None
    }
else:
    # 예약 받기 위한 과정 
    pos = p.pos(received_text)
    ret = p.get_keywords(pos, without_tag=False)

    # 태그에 해당하는 단어 추출
    predicts = ner.predict(received_text)
    tags = ner.predict_tags(received_text)

    # 예외 처리: predicts 또는 tags가 None일 경우
    if predicts is None or tags is None:
        response = ""
        destination = ""
        time = ""
    else:
        # 장소 정보에 해당하는 단어를 추출 
        destination_words = [word[0] for word, tag in zip(predicts, tags) if tag == 'B_FOOD']
        destination = ' '.join(destination_words)

    # 의도 예측
    predict = intent.predict_class(received_text)
    predict_label = intent.labels[predict]

    date = None
    hour = None
    minute = None

    # 의도에 따른 응답 생성
    if predict_label == '인사':
        response = "안녕하세요. 무엇을 도와드릴까요?"
    elif predict_label == '욕설':
        response = "죄송하지만 욕설은 사용할 수 없습니다."
    elif predict_label == '주문':
        response = "네 알겠습니다. 목적지로 출발하겠습니다."
    elif predict_label == '예약':
        response = ""
        for keyword, pos in ret:
            if pos == 'NNP':
                date_str = keyword.replace(" ", "")
                if date_str == "오늘":
                    date = datetime.now().strftime('%Y.%m.%d')
                elif date_str == "내일":
                    date = (datetime.now() + timedelta(days=1)).strftime('%Y.%m.%d')
                elif date_str == "모레":
                    date = (datetime.now() + timedelta(days=2)).strftime('%Y.%m.%d')
                elif date_str == "글피":
                    date = (datetime.now() + timedelta(days=3)).strftime('%Y.%m.%d')
                elif date_str == "일주일후":
                    date = (datetime.now() + timedelta(weeks=1)).strftime('%Y.%m.%d')
                else:
                    date_obj = datetime.strptime(date_str, '%m월%d일')
                    date = date_obj.replace(year=current_year).strftime('%Y.%m.%d')
            elif pos == 'NR':
                if hour is None:
                   hour = keyword
                else:
                    minute = keyword
    else:
        response = "잘 이해하지 못했습니다. 다시한번 말씀해주세요."

    response_data = {
        "intention": predict_label,
        "response": response,
        "destination": destination,
        "date": date,  
        "hour": hour,
        "minute": minute
    }

# JSON 형식으로 출력
response_json = json.dumps(response_data, ensure_ascii=False)
print(response_json)
