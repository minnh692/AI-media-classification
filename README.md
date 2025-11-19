# 🔍 AI 생성물 판별 분석기

Google Gemini 2.0-Flash API를 활용한 **이미지/영상 AI 생성 여부 판별 도구**

## 📌 개요

- AI 생성 이미지/영상 감지 웹 애플리케이션
- Flask 백엔드 + 순수 JavaScript 프론트엔드
- Google Gemini API (무료 1,000 요청/일)
- 신뢰도 지표, 감지 신호, 상세 분석 제공

⚠️ **참고**: 100% 정확도를 보장하지 않으며, 분석 결과는 참고용입니다.

---

## 🎯 주요 기능

### 파일 업로드
- 지원 형식: JPEG, PNG, WebP, GIF, MP4, WebM
- 최대 크기: 20MB
- 방식: 클릭 선택 / 드래그 앤 드롭

### 분석 결과
- **신뢰도 지표** (0-100%): 색상 바로 시각화
- **판정 결과**: LIKELY_AI / UNCERTAIN / LIKELY_HUMAN
- **감지 신호**: 의심 항목 상세 설명
- **상세 분석**: 질감, 조명, 세부사항, 배경 분석

---

## 🛠️ 기술 스택

| 계층 | 기술 |
|------|------|
| **프론트엔드** | HTML5, CSS3 (Flexbox, Grid, 반응형), Vanilla JavaScript |
| **백엔드** | Python 3.13, Flask 3.1.2, Flask-CORS 6.0.1 |
| **API** | Google Gemini 2.0-Flash |
| **의존성** | requests 2.32.5, python-dotenv 1.2.1 |

---

---

## 📁 파일 구조

```
├── index.html          # 프론트엔드 (UI)
├── style.css           # 스타일시트
├── script.js           # 클라이언트 로직
├── app.py              # Flask 백엔드
├── requirements.txt    # Python 의존성
├── .env                # 환경 변수 (API 키) ⭐ 필수
├── .gitignore          # Git 무시 설정
└── README.md           # 이 문서
```

---

## � 시작하기

### 1. 환경 설정

```bash
# 저장소 클론
git clone <repository-url>
cd AI-media-classification

# Python 패키지 설치
pip install -r requirements.txt
```

### 2. API 키 설정

[Google AI Studio](https://ai.google.dev) 접속 → API 키 생성

`.env` 파일 생성:
```
GEMINI_API_KEY=your_api_key_here
```

### 3. 서버 실행

```bash
python app.py
```

서버는 `http://localhost:5000`에서 실행됩니다.

### 4. 웹 애플리케이션 사용

`index.html`을 브라우저에서 열기 (또는 Live Server 사용)

---

## � 분석 결과 해석

| 신뢰도 | 범위 | 판정 | 의미 |
|--------|------|------|------|
| 🟢 낮음 | 0-30% | LIKELY_HUMAN | 인간이 생성했을 가능성 높음 |
| 🟡 중간 | 30-70% | UNCERTAIN | 판단 곤란, 재검토 권장 |
| 🔴 높음 | 70-100% | LIKELY_AI | AI 생성물일 가능성 높음 |

---

## 🚀 설치 및 사용

### 1. 환경 설정

```bash
# 저장소 클론
git clone <repository-url>
cd AI-media-classification

# Python 패키지 설치
pip install -r requirements.txt
```

### 2. API 키 설정

[Google AI Studio](https://ai.google.dev)에서 API 키 발급 후 `.env` 파일 생성:

```
GEMINI_API_KEY=your_api_key_here
```

### 3. 서버 실행

```bash
python app.py
```

`http://localhost:5000`에서 실행됩니다.

### 4. 웹 사용

`index.html`을 브라우저에서 열기

---

## 📊 결과 해석

### AI 생성 가능성

| 신뢰도 | 범위 | 판정 |
|--------|------|------|
| 🟢 낮음 | 0-30% | LIKELY_HUMAN (인간 생성) |
| 🟡 중간 | 30-70% | UNCERTAIN (불확실) |
| 🔴 높음 | 70-100% | LIKELY_AI (AI 생성) |

---

## ⚙️ 기술 구성

### 아키텍처

```
[브라우저]
   ↓ (Base64 이미지)
[Flask 서버]
   ↓ (프롬프트 + 이미지)
[Google Gemini API]
   ↓ (분석 결과)
[브라우저 - 결과 표시]
```

### 주요 특징

- **CORS 처리**: Flask 프록시로 크로스 오리진 정책 우회
- **API 키 보안**: 클라이언트 노출 안 함
- **간단한 구조**: 경량 프레임워크 사용

---

## 🔧 트러블슈팅

### API 키 오류
```bash
# .env 파일 확인
cat .env

# 파일 없으면 생성
echo "GEMINI_API_KEY=YOUR_KEY" > .env
```

### 포트 5000 이미 사용 중 (Windows)
```bash
netstat -ano | findstr :5000
taskkill /PID [PID] /F
```

### CORS 오류
→ Flask 서버가 실행 중인지 확인 (`python app.py`)

---

## 📈 제한사항

| 항목 | 한도 |
|------|------|
| 일일 요청 | 1,000개 |
| 동시 요청 | 2개 |
| 파일 크기 | 20MB |
| 응답 시간 | 5-10초 |

---

## 🔐 보안

- ✅ API 키는 `.env`에서만 로드 (gitignore 처리)
- ✅ 파일은 Base64 인코딩 후 전송
- ✅ 메모리에만 저장 (영구 저장 안 함)
- ✅ 파일 타입/크기 검증

---

## 📞 참고 자료

- [Google Gemini API 문서](https://ai.google.dev/docs)
- [Flask 문서](https://flask.palletsprojects.com/)

**마지막 업데이트**: 2025년 11월 17일 | **버전**: 1.0.0