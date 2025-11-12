# ...existing code...
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS  # CORS 문제 방지용 (선택)
import logging
import os

app = Flask(__name__)
CORS(app)

# 로그 파일 경로 (프로젝트 폴더에 생성)
LOG_PATH = os.path.join(os.path.dirname(__file__), "requests.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),  # 콘솔 출력
        logging.FileHandler(LOG_PATH, encoding="utf-8")  # 파일 출력
    ],
)

@app.before_request
def log_request_info():
    # 본문은 JSON이 아닐 수 있으니 안전하게 추출
    try:
        body = request.get_json(silent=True)
        if body is None:
            body = request.get_data(as_text=True)
    except Exception:
        body = "<unreadable>"
    logging.info("REQ %s %s from %s args=%s body=%s",
                 request.method, request.path, request.remote_addr, request.args.to_dict(), body)

# HTML 파일을 같은 서버에서 제공 (브라우저에서 http://localhost:5000/ 로 접근)
@app.route("/", methods=["GET"])
def index():
    return send_from_directory(os.path.dirname(__file__), "asdf.html")

@app.route("/<path:filename>", methods=["GET"])
def serve_file(filename):
    return send_from_directory(os.path.dirname(__file__), filename)

@app.route("/api/hello", methods=["GET"])
def hello():
    return jsonify({"message": "백엔드에서 온 데이터입니다!"})

@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    return jsonify({"result": f"서버가 받은 내용: {text}"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
# ...existing code...