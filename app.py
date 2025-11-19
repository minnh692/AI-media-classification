"""
AI 생성물 판별 분석기 - Flask 백엔드
Google Gemini API를 사용하여 이미지/영상 분석
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
import sys
from dotenv import load_dotenv

# Windows 한글 인코딩 문제 해결
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)
CORS(app)

# Google Gemini API 키
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


@app.route('/api/health', methods=['GET'])
def health():
    """서버 헬스 체크"""
    return jsonify({
        'status': 'ok',
        'message': 'AI 생성물 판별 분석기 서버 실행 중'
    }), 200


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    이미지 또는 영상 분석
    요청: {imageData: "base64string", mediaType: "image/jpeg"}
    응답: {confidence: 75, verdict: "LIKELY_AI", signals: [...], ...}
    """
    try:
        # 요청 데이터 확인
        if not request.json:
            return jsonify({'error': '요청 데이터가 없습니다.'}), 400

        image_data = request.json.get('imageData')
        media_type = request.json.get('mediaType', 'image/jpeg')

        if not image_data:
            return jsonify({'error': '이미지 데이터가 없습니다.'}), 400

        # API 키 확인
        if not GEMINI_API_KEY:
            return jsonify({'error': 'API 키가 설정되지 않았습니다.'}), 500

        # Gemini API 호출을 위한 프롬프트
        prompt = """이 이미지/영상이 AI로 생성되었을 가능성을 분석해주세요.

다음 형식으로 정확히 응답해주세요 (JSON만 응답):
{
    "confidence": <0-100 숫자, AI로 생성되었을 확률. 0=확실히 인간 생성, 100=확실히 AI 생성>,
    "verdict": "<LIKELY_AI 또는 LIKELY_HUMAN 또는 UNCERTAIN>",
    "signals": [
        {"title": "신호1", "description": "설명1"},
        {"title": "신호2", "description": "설명2"}
    ],
    "texture_analysis": "텍스처 분석 내용",
    "lighting_analysis": "조명 분석 내용",
    "detail_analysis": "세부사항 분석 내용",
    "background_analysis": "배경 분석 내용",
    "summary": "전체 종합 판정 내용"
}

중요 규칙:
- confidence는 반드시 "AI 생성 확률"을 나타내야 합니다.
- verdict가 LIKELY_HUMAN이면 confidence는 30 미만이어야 합니다.
- verdict가 LIKELY_AI이면 confidence는 70 이상이어야 합니다.
- verdict가 UNCERTAIN이면 confidence는 30-70 사이여야 합니다.

주의: JSON만 응답하고 다른 텍스트는 추가하지 마세요."""

        # Gemini API 요청 (gemini-2.0-flash 최신 모델)
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        },
                        {
                            "inlineData": {
                                "mimeType": media_type,
                                "data": image_data
                            }
                        }
                    ]
                }
            ]
        }

        response = requests.post(url, json=payload, timeout=30)

        if response.status_code != 200:
            error_info = response.json() if response.text else {}
            error_msg = error_info.get('error', {}).get('message', f'API 오류: {response.status_code}')
            return jsonify({'error': error_msg}), response.status_code

        result = response.json()

        # 응답 처리
        if 'candidates' not in result or not result['candidates']:
            return jsonify({'error': 'API 응답이 유효하지 않습니다.'}), 500

        content = result['candidates'][0].get('content', {})
        parts = content.get('parts', [])

        if not parts:
            return jsonify({'error': 'API 응답에 데이터가 없습니다.'}), 500

        text = parts[0].get('text', '')

        # JSON 파싱 (오염된 JSON 제거)
        try:
            # 만약 JSON이 다른 텍스트로 감싸져 있다면 추출
            if '{' in text and '}' in text:
                start_idx = text.find('{')
                end_idx = text.rfind('}') + 1
                json_str = text[start_idx:end_idx]
                analysis = json.loads(json_str)
            else:
                analysis = json.loads(text)
        except json.JSONDecodeError as e:
            # JSON 파싱 실패 시 에러 반환
            return jsonify({'error': f'API 응답 파싱 오류: {str(e)}'}), 500

        return jsonify(analysis), 200

    except requests.exceptions.Timeout:
        return jsonify({'error': '요청 시간 초과. 다시 시도해주세요.'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'네트워크 오류: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'서버 오류: {str(e)}'}), 500


if __name__ == '__main__':
    print('=' * 50)
    print('AI 생성물 판별 분석기 - Flask 서버')
    print('=' * 50)
    
    if not GEMINI_API_KEY:
        print('경고: GEMINI_API_KEY가 설정되지 않았습니다!')
        print('   .env 파일을 확인하고 API 키를 입력해주세요.')
    else:
        print(f'API 키 로드됨: {GEMINI_API_KEY[:20]}...')
    
    print('서버 시작 중...')
    print('http://localhost:5000')
    print('=' * 50)
    
    app.run(debug=True, port=5000, host='0.0.0.0')
