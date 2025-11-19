import os
import base64
import json

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 환경 변수 읽기
load_dotenv()

app = Flask(__name__)

# OpenAI 클라이언트 (환경변수에서 키 읽음)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    # templates/index.html 을 렌더링
    return render_template("index.html")

@app.route("/api/check", methods=["POST"])
def check_image():
    # 이미지 파일이 제대로 전달됐는지 확인
    if "image" not in request.files:
        return jsonify({"error": "이미지 파일이 없습니다."}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "선택된 파일이 없습니다."}), 400

    # 파일 → base64 data URL
    img_bytes = file.read()
    mime_type = file.mimetype or "image/jpeg"
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    data_url = f"data:{mime_type};base64,{b64}"

    # 모델에게 줄 프롬프트
    system_prompt = """
    너는 'AI 생성 이미지일 가능성'을 추정하는 보조 도구야.

    해야 할 일:
    1) 업로드된 이미지를 보고, 이 이미지가
       - 사진/스캔 등 현실 세계를 찍은 것인지
       - 생성형 AI(예: DALL·E, Midjourney 등)로 만들었을 가능성이 큰지
       분석한다.
    2) 아래 JSON 형식으로만 답한다.

    {
      "is_ai_generated": true or false,
      "confidence": 0~100 사이 정수(추정 신뢰도, 퍼센트),
      "label": "AI로 생성된 것으로 보입니다" 같은 한글 한 줄 요약,
      "reasons": "이유를 한국어로 2~3문장 설명"
    }

    주의:
    - 100% 확신할 수 없다는 점을 인식하고, 과도한 확신은 피한다.
    - 단순한 느낌이 아니라, 조명, 질감, 디테일, 왜곡, 노이즈 패턴, 글자/손가락 등
      시각적 특징을 근거로 설명한다.
    """

    try:
        # 🔹 chat.completions API 사용 (이미지 + 텍스트)
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "이 이미지를 분석해서 요구한 JSON 형식으로만 결과를 반환해.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": data_url},
                        },
                    ],
                },
            ],
            # 응답을 JSON 객체 형식으로 강제
            response_format={"type": "json_object"},
        )

        # 모델이 준 JSON 문자열
        text = completion.choices[0].message.content

        # JSON 문자열 → dict
        result = json.loads(text)

        return jsonify(result)

    except Exception as e:
        print("OpenAI API error:", e)
        return jsonify({"error": "서버 또는 OpenAI API 오류가 발생했습니다."}), 500


if __name__ == "__main__":
    # 개발용 서버 실행
    app.run(debug=True)
