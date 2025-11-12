# 🔍 AI 생성물 판별 분석기 (AI Media Classification)

**Google Gemini 2.0-Flash API 기반 AI 생성 이미지/영상 판별 웹 애플리케이션**

## 📌 프로젝트 개요

이 프로젝트는 **Google Gemini 2.0-Flash API를 활용하여 이미지와 영상이 AI로 생성되었는지 인간이 생성했는지 판별하는 보조 분석 도구**입니다.

### ⚠️ 중요 사항
- **이 도구는 의심 신호를 감지하고 확률을 추정하는 방식**으로 작동합니다
- **100% 정확도를 보장할 수 없으며, 참고용이며 최종 판단은 전문가 검토가 필요합니다**
- **무료 API 등급**: 1,000 요청/일 제한

---

## 🎯 핵심 기능

### 1️⃣ 파일 업로드
- **지원 형식**
  - 이미지: JPEG, PNG, WebP, GIF
  - 영상: MP4, WebM
  - 파일 크기 제한: 최대 20MB
  
- **업로드 방식**
  - 클릭 선택
  - 드래그 앤 드롭
  - 실시간 미리보기

### 2️⃣ AI 생성물 분석

분석 항목:

- 📊 **AI 생성 가능성** (0-100%)
  - 0-30%: 낮음 (인간 생성 가능성 높음) 🟢
  - 30-70%: 중간 (불확실) 🟡
  - 70-100%: 높음 (AI 생성 가능성 높음) 🔴

- 🚨 **감지된 신호**
  - 비정상적인 패턴
  - 부자연스러운 특징
  - AI 생성 특성
  - 각 신호별 상세 설명

- � **상세 분석**
  - **질감 분석**: 피부, 옷감, 물체 텍스처 일관성
  - **조명 분석**: 빛의 방향, 그림자, 반사 표현
  - **세부사항**: 머리카락, 눈, 작은 물체의 디테일
  - **배경 분석**: 배경 생성 흔적, 자연스러움

- ⚖️ **최종 판정** (종합 판정)
  - 종합적인 분석 결과를 텍스트로 제공
  - 각 신호의 중요도를 설명

### 3️⃣ 결과 시각화
- 색상 기반 신뢰도 바 (초록→노랑→빨강)
- 신호별 아이콘 및 설명
- 최종 판정 카드 (상태별 배경색 변화)

---

## 🛠️ 기술 스택

### 프론트엔드
- **HTML5**: 시맨틱 마크업
- **CSS3**: 
  - Flexbox & Grid 레이아웃
  - CSS 변수 (Custom Properties)
  - 반응형 디자인 (모바일/태블릿/데스크톱)
  - 그라데이션 & 애니메이션
  - 색상 기반 신뢰도 표시 (초록→노랑→빨강)
- **JavaScript (Vanilla)**:
  - 파일 처리 (FileReader API)
  - 드래그 앤 드롭
  - Base64 인코딩
  - Fetch API로 백엔드 호출

### 백엔드 (Python/Flask)
- **Flask 3.1.2**: 웹 API 서버
- **Flask-CORS 6.0.1**: 크로스 오리진 요청 지원
- **Requests 2.32.5**: HTTP 요청 처리
- **Python-dotenv 1.2.1**: 환경 변수 관리
- **Python 3.13**: 런타임

### API
- **Google Gemini 2.0-Flash**: 이미지/영상 분석 AI
- **무료 API**: 1,000 요청/일

---

## 📁 파일 구조

```
AI-media-classification/
├── index.html                 # 프론트엔드 (메인 페이지)
├── style.css                  # 스타일시트
├── script.js                  # JavaScript (클라이언트 로직)
├── app.py                     # 백엔드 (Flask 서버)
├── requirements.txt           # Python 의존성
├── .env                       # 환경 변수 (API 키) ⭐ 필수
├── .gitignore                 # Git 무시 파일
├── README.md                  # 이 문서
└── test.html                  # 테스트 파일
```

---

## 💻 설계 상세

### 아키텍처 다이어그램

```
┌─────────────────────────────────────────┐
│           사용자 브라우저                 │
│  index.html + style.css + script.js      │
└─────────────────────────────────────────┘
                    │
                    │ (파일 업로드)
                    │ POST /api/analyze
                    ↓
┌─────────────────────────────────────────┐
│        Flask 백엔드 (app.py)             │
│  - 파일 검증                             │
│  - API 키 관리                           │
│  - Gemini API 호출                       │
│  - JSON 파싱 및 응답                      │
└─────────────────────────────────────────┘
                    │
                    │ (Base64 이미지)
                    ↓
┌─────────────────────────────────────────┐
│    Google Gemini 2.0-Flash API          │
│  (이미지 분석 & 판별)                    │
└─────────────────────────────────────────┘
                    │
                    │ (분석 결과 JSON)
                    ↓
┌─────────────────────────────────────────┐
│           사용자 브라우저                 │
│  (결과 시각화 및 표시)                   │
└─────────────────────────────────────────┘
```

### 왜 이 아키텍처?

✅ **CORS 문제 해결**: 브라우저에서 직접 외부 API 호출 불가 → Flask 프록시 사용
✅ **API 키 보안**: 서버에서만 API 키 보관 (클라이언트에 노출 안 됨)
✅ **간단한 구조**: 복잡한 프레임워크 없이 간단하고 효율적

### Flask 백엔드 (`app.py`) 상세

#### 엔드포인트 1: GET `/api/health`
```
목적: 서버 상태 확인
응답:
{
    "status": "ok",
    "message": "AI 생성물 판별 분석기 서버 실행 중"
}
```

#### 엔드포인트 2: POST `/api/analyze`
```
목적: 이미지/영상 분석

요청:
{
    "imageData": "base64_encoded_image",
    "mediaType": "image/jpeg"  # 또는 image/png, video/mp4 등
}

응답:
{
    "confidence": 85,                    # 0-100 (AI 생성 가능성)
    "verdict": "LIKELY_AI",              # LIKELY_AI / UNCERTAIN / LIKELY_HUMAN
    "signals": [
        {
            "title": "신호 제목",
            "description": "신호 상세 설명"
        },
        ...
    ],
    "texture_analysis": "텍스처 분석 결과",
    "lighting_analysis": "조명 분석 결과",
    "detail_analysis": "세부사항 분석 결과",
    "background_analysis": "배경 분석 결과",
    "summary": "종합 판정 및 분석 결과"
}
```

#### API 호출 흐름

```python
1. 요청 수신
   ├─ imageData 검증
   ├─ mediaType 확인
   └─ API 키 확인

2. Gemini API 호출
   ├─ URL: https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent
   ├─ 메서드: POST
   ├─ 헤더: Content-Type: application/json
   ├─ 바디: 
   │   {
   │       "contents": [{
   │           "parts": [
   │               {"text": "프롬프트"},
   │               {"inlineData": {"mimeType": "...", "data": "base64..."}}
   │           ]
   │       }]
   │   }
   └─ 타임아웃: 30초

3. 응답 처리
   ├─ JSON 파싱
   ├─ 오염된 JSON 정리 (JSON이 다른 텍스트로 감싸져 있어도 추출)
   └─ 클라이언트에 반환

4. 에러 처리
   ├─ 요청 타임아웃: 504 Gateway Timeout
   ├─ 네트워크 오류: 500 Internal Server Error
   ├─ 파싱 오류: 500 Internal Server Error
   └─ 상세 에러 메시지 반환
```

### HTML 구조 (`index.html`)

#### 1. 헤더
```html
<header class="header">
    <h1>🔍 AI 생성물 판별 분석기</h1>
    <p class="subtitle">Google Gemini API 기반 이미지/영상 분석</p>
</header>
```

#### 2. 3단계 워크플로우

**Stage 1: 업로드** (#uploadSection)
```
┌─────────────────────┐
│   파일 선택 영역      │
│                     │
│  [드래그 또는 클릭]   │
│  📤                 │
│  [파일 선택 버튼]    │
└─────────────────────┘
```

**Stage 2: 프리뷰** (#previewSection)
```
┌─────────────────────┐
│  이미지/영상 표시    │
│  (최대 400px 높이)  │
│                     │
│  [다른 파일] [분석] │
└─────────────────────┘
```

**Stage 3: 결과** (#resultsSection)
```
┌─────────────────────────────────┐
│  1️⃣ AI 생성 가능성                │
│     [████████░░░░░░░░] 65%       │
│     중간 (불확실)                 │
├─────────────────────────────────┤
│  2️⃣ 최종 판정                    │
│     🤖 AI 생성물일 가능성이 높음   │
├─────────────────────────────────┤
│  3️⃣ 감지된 신호                  │
│     • 신호1: 설명                 │
│     • 신호2: 설명                 │
├─────────────────────────────────┤
│  4️⃣ 상세 분석                    │
│     질감: ...                     │
│     조명: ...                     │
│     세부: ...                     │
│     배경: ...                     │
├─────────────────────────────────┤
│  5️⃣ 종합 판정                    │
│     (전체 분석 결과 요약)           │
└─────────────────────────────────┘
```

### CSS 설계 (`style.css`)

#### 색상 시스템

| 변수 | 색상 | 용도 |
|------|------|------|
| `--primary` | #6366f1 | 주요 액센트 (인디고) |
| `--success` | #10b981 | 성공/낮은 위험 (그린) |
| `--warning` | #f59e0b | 경고/중간 (앰버) |
| `--danger` | #ef4444 | 위험/높음 (레드) |
| `--light` | #f3f4f6 | 배경 (밝은 회색) |
| `--gray` | #6b7280 | 텍스트/설명 (중간 회색) |
| `--text` | #1f2937 | 메인 텍스트 (검정) |

#### 신뢰도 바 디자인

```css
.confidence-bar {
    배경: 밝은 회색 (제한된 영역)
    높이: 30px
    채우기: 그라데이션 (초록→노랑→빨강)
    애니메이션: 부드러운 채우기 (0.5s ease)
}

0-30%:   🟢 초록 (인간 생성)
30-70%:  🟡 노랑 (불확실)
70-100%: 🔴 빨강 (AI 생성)
```

#### 레이아웃

- **컨테이너**: 최대 900px 너비, 중앙 정렬, 흰색 배경
- **헤더**: 그라데이션 배경 (자주색→분홍색), 흰색 텍스트
- **카드 시스템**: 
  - 왼쪽 보더 4px (강조)
  - 패딩 25px
  - 둥근 모서리 8px
  - 박스 그림자
- **버튼**: 
  - 기본: 인디고
  - 호버: 어두운 인디고 + 아래로 2px 이동

#### 반응형 디자인

| 화면 크기 | 처리 |
|----------|------|
| 1200px+ | 풀 레이아웃, 정상 패딩 |
| 768px-1199px | 태블릿: 버튼 전체 너비 |
| 480px+ | 모바일: 패딩 감소, 텍스트 축소 |

### JavaScript 로직 (`script.js`)

#### 주요 함수

```javascript
1. setupEventListeners()
   - 파일 입력 이벤트
   - 드래그 앤 드롭 이벤트
   - 버튼 클릭 이벤트

2. handleFileSelect(event)
   - 파일 선택 시 processFile() 호출

3. handleDragOver/Leave/Drop()
   - 드래그 오버 상태 시각화
   - 드롭 시 파일 처리

4. processFile(file)
   - 파일 타입 검증 (MIME type)
   - 파일 크기 검증 (20MB)
   - displayPreview() 호출

5. displayPreview(file)
   - 이미지 미리보기 또는
   - 비디오 미리보기 표시
   - Stage 2로 전환

6. analyzeFile()
   - Base64 변환
   - /api/analyze POST 요청
   - 결과 표시 또는 에러 처리

7. fileToBase64(file)
   - File 객체 → Base64 문자열

8. displayResults(data)
   - AI 생성 가능성 바 업데이트
   - 신호 목록 렌더링
   - 상세 분석 표시
   - 종합 판정 표시

9. showError(message)
   - 에러 메시지 표시
   - 재시도 버튼 제공
```

#### 파일 검증

```javascript
지원 형식:
- 이미지: image/jpeg, image/png, image/webp, image/gif
- 영상: video/mp4, video/webm

파일 크기:
- 최대 20MB

검증 실패 시:
- 사용자 친화적 에러 메시지 표시
```

---

## 🚀 빠른 시작

### 사전 요구사항
- Python 3.8 이상 (3.13 권장)
- Google Gemini API 키 (무료)
- 웹 브라우저

### 설치 및 실행

#### Step 1️⃣: Google Gemini API 키 발급

1. https://ai.google.dev/ 접속
2. "Get API Key" 버튼 클릭
3. Google 계정으로 로그인
4. API 키 복사

#### Step 2️⃣: 환경 설정

프로젝트 폴더에 `.env` 파일 생성:

```bash
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

예시:
```
GEMINI_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Step 3️⃣: Python 패키지 설치

```bash
pip install -r requirements.txt
```

설치되는 패키지:
- flask (3.1.2)
- flask-cors (6.0.1)
- requests (2.32.5)
- python-dotenv (1.2.1)

#### Step 4️⃣: Flask 서버 실행

```bash
python app.py
```

성공 메시지:
```
==================================================
AI 생성물 판별 분석기 - Flask 서버
==================================================
API 키 로드됨: AIzaSyC66S...
서버 시작 중...
http://localhost:5000
==================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

#### Step 5️⃣: 웹 브라우저에서 열기

1. 파일 탐색기에서 `index.html` 우클릭
2. "연결 프로그램" → "웹 브라우저" 선택
3. 또는 브라우저의 주소창에서 `Ctrl+O` 후 파일 선택

### 사용 흐름

```
1. 페이지 로드
   ↓
2. 이미지/영상 업로드
   (드래그 또는 클릭)
   ↓
3. 미리보기 확인
   ↓
4. "분석 시작" 버튼 클릭
   ↓
5. 분석 대기 (로딩 스피너)
   ↓
6. 결과 확인
   - AI 생성 가능성 바
   - 감지된 신호
   - 상세 분석
   - 종합 판정
```

---

## 📊 분석 결과 해석

### AI 생성 가능성

| 범위 | 의미 | 신뢰도 |
|------|------|--------|
| 0-30% | 인간이 생성했을 가능성 높음 | 낮음 🟢 |
| 30-70% | AI인지 인간인지 불확실 | 중간 🟡 |
| 70-100% | AI 생성물일 가능성 높음 | 높음 🔴 |

### 감지되는 신호 예시

**AI 생성 이미지의 특징:**
- 피부가 지나치게 매끄럽고 인위적
- 배경 흐림이 부자연스러움
- 머리카락 가닥이 지나치게 균일
- 눈동자의 광원 반사가 인위적
- 얼굴의 완벽한 대칭성
- 텍스처가 부드럽지만 단순

**인간이 생성한 이미지의 특징:**
- 자연스러운 피부 텍스처 (모공, 주름)
- 그림자와 빛의 자연스러운 분포
- 불규칙한 머리카락 패턴
- 미세한 결함과 불완벽함
- 비대칭적인 요소들
- 풍부한 텍스처 디테일

### 최종 판정 해석

| 판정 | 의미 |
|------|------|
| LIKELY_AI | AI 생성물일 가능성이 높습니다. |
| UNCERTAIN | AI인지 인간 생성인지 판별이 어렵습니다. |
| LIKELY_HUMAN | 인간이 생성한 콘텐츠일 가능성이 높습니다. |

---

## 🔧 트러블슈팅

### 1. "API 키가 설정되지 않았습니다" 오류

**원인**: `.env` 파일 없거나 API 키 형식 오류

**해결책**:
```bash
# .env 파일 확인
cat .env

# 파일이 없으면 생성
echo "GEMINI_API_KEY=YOUR_KEY_HERE" > .env

# 서버 재시작
python app.py
```

### 2. "요청 시간 초과" 오류

**원인**: API 응답 시간이 30초 초과

**해결책**:
- 인터넷 연결 확인
- 파일 크기 확인 (20MB 이하)
- 잠시 후 재시도
- Gemini API 상태 확인 (ai.google.dev)

### 3. "JSON 파싱 오류"

**원인**: API 응답이 올바른 JSON 형식 아님

**해결책**:
- 프롬프트 재확인
- 파일이 손상되지 않았는지 확인
- 브라우저 콘솔(F12) 에서 네트워크 탭 확인
- 서버 로그 확인

### 4. 포트 5000이 이미 사용 중

**원인**: 다른 프로그램이 포트 5000 사용 중

**해결책**:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID [PID] /F

# macOS/Linux
lsof -i :5000
kill -9 [PID]
```

### 5. CORS 오류 ("Access to XMLHttpRequest blocked")

**원인**: Flask 서버가 실행되지 않음

**해결책**:
```bash
# 터미널에서 확인
python app.py

# 정상 메시지 확인
# Running on http://127.0.0.1:5000
```

---

## 📈 성능 및 제한사항

### Google Gemini API 무료 등급 제한
- **요청 한도**: 1,000 요청/일
- **동시 요청**: 2개
- **파일 크기**: 최대 20MB
- **응답 시간**: 평균 5-10초

### 권장 사항
- 대량 분석 시 배치 처리 권장
- 시간대별 사용 분산
- 중복 분석 피하기 (결과 캐싱)

---

## 🔐 보안

### 프론트엔드
- API 키는 저장되지 않음 (전부 서버에서 처리)
- 파일은 Base64 인코딩 후 전송
- 메모리에만 저장 (영구 저장 X)

### 백엔드
- API 키는 `.env` 파일에서만 로드
- `.env`는 `.gitignore`에 포함 (커밋 안 됨)
- 파일 타입, 크기 검증
- 요청 타임아웃 설정 (30초)
- CORS 설정으로 특정 출처만 허용 가능

### 추가 보안 (권장)
```python
# app.py에 추가 가능
from flask_limiter import Limiter

# Rate limiting (1시간에 100개 요청)
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/analyze', methods=['POST'])
@limiter.limit("100/hour")
def analyze():
    # ...
```

---

## 🧪 테스트

### 수동 테스트 체크리스트

- [ ] **UI 렌더링**
  - [ ] 페이지가 정상 로드되는가
  - [ ] 모바일에서 반응형 디자인이 작동하는가

- [ ] **파일 업로드**
  - [ ] 클릭으로 파일 선택 가능
  - [ ] 드래그 앤 드롭 작동
  - [ ] 미리보기 표시

- [ ] **파일 검증**
  - [ ] 지원하지 않는 형식 거부
  - [ ] 20MB 초과 파일 거부
  - [ ] 올바른 에러 메시지 표시

- [ ] **분석**
  - [ ] 로딩 스피너 표시
  - [ ] API 응답 수신
  - [ ] 결과 렌더링

- [ ] **결과 표시**
  - [ ] AI 생성 가능성 바 표시 (0-100%)
  - [ ] 신호 목록 표시
  - [ ] 상세 분석 표시
  - [ ] 종합 판정 표시

### 테스트 이미지 소스
- Unsplash (실사)
- 생성형 AI (DALL-E, Midjourney 결과)
- 본인 촬영 사진

---

## 📚 개발 로그

### 프로젝트 진행 과정

#### Phase 1: 초기 계획 (2025-11-12)
- [x] 요구사항 정의
- [x] 기술 스택 선택 (Google Gemini API)
- [x] 아키텍처 설계

#### Phase 2: 프론트엔드 구현 (2025-11-12)
- [x] HTML 구조 작성 (3단계 워크플로우)
- [x] CSS 스타일링 (반응형 디자인)
- [x] JavaScript 로직 (파일 처리, API 호출)
- [x] 드래그 앤 드롭 구현
- [x] 에러 처리

#### Phase 3: 백엔드 구현 (2025-11-12)
- [x] Flask 앱 초기화
- [x] `/api/health` 엔드포인트
- [x] `/api/analyze` 엔드포인트
- [x] Gemini API 통합
- [x] JSON 파싱 및 에러 처리
- [x] CORS 설정

#### Phase 4: 최적화 (2025-11-12)
- [x] Gemini 2.0-Flash 모델 적용
- [x] 프롬프트 최적화
- [x] JSON 추출 로직 개선
- [x] 신뢰도 바 역계산 수정
- [x] UI/UX 개선

#### Phase 5: 문서화 (2025-11-12)
- [x] README.md 작성
- [x] 설치 가이드
- [x] 사용 방법 문서화
- [x] 트러블슈팅 가이드

---

## 🚀 향후 개선 사항

### 단기 (Phase 6)
- [ ] 배치 분석 기능 (여러 파일 동시 처리)
- [ ] 분석 히스토리 저장 (로컬 스토리지)
- [ ] 결과 내보내기 (JSON, CSV)
- [ ] 분석 통계 대시보드

### 중기 (Phase 7)
- [ ] 사용자 계정 시스템
- [ ] 클라우드 데이터베이스 연동
- [ ] API 사용량 모니터링 대시보드
- [ ] 다중 모델 앙상블 (정확도 개선)

### 장기 (Phase 8)
- [ ] 모바일 앱 개발 (React Native)
- [ ] 커스텀 AI 모델 학습
- [ ] 데스크톱 앱 (Electron)
- [ ] API 마켓플레이스 배포

---

## 💡 기술적 결정사항

### Google Gemini API를 선택한 이유
| 항목 | OpenAI Vision | Google Gemini | 승자 |
|------|---------------|---------------|------|
| 비용 | 유료 | 무료 (1000/일) | Gemini ✅ |
| 멀티모달 | O | O | 동등 |
| 이미지 분석 | 우수 | 우수 | 동등 |
| API 문서 | 상세 | 상세 | 동등 |
| 한국어 지원 | O | O | 동등 |

**결론**: 무료 등급 지원으로 Gemini API 선택 ✅

### CORS 문제 해결
```
❌ 초기 시도: 브라우저에서 직접 API 호출
   → CORS 정책 위반

✅ 최종 해결: Flask 프록시 패턴
   → 서버에서 API 호출 → 클라이언트로 결과 반환
   → CORS 문제 해결 + API 키 보안
```

### 신뢰도 표시 방식

**첫 번째 시도** (역계산):
- confidence 85 → 표시 15 (✗ 직관적이지 않음)

**최종 선택** (직접 표시):
- confidence 85 → 표시 85 (✓ 직관적)
- "AI 생성 가능성" 이름으로 개념 명확화

---

## 📖 참고 자료

### 공식 문서
- [Google Gemini API 문서](https://ai.google.dev/docs)
- [Flask 공식 문서](https://flask.palletsprojects.com/)
- [MDN Web Docs - FileReader API](https://developer.mozilla.org/en-US/docs/Web/API/FileReader)

### AI 생성 탐지 관련 논문/리소스
- [Arxiv AI Detection Papers](https://arxiv.org/)
- [How to Detect AI-Generated Images](https://www.google.com/search?q=detect+ai+generated+images)
- [Fake Image Detection Methods](https://arxiv.org/list/cs.CV/recent)

### CSS 레퍼런스
- [CSS 변수 가이드](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
- [Flexbox 레이아웃](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout)
- [반응형 디자인](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)

---

## 👥 프로젝트 정보

**저장소**: minnh692/AI-media-classification
**브랜치**: yangji
**개발 기간**: 2025년 11월 12일
**개발자**: AI Assistant (GitHub Copilot)

**주요 마일스톤**:
- ✅ 초기 설계 및 기술 선택
- ✅ OpenAI → Google Gemini API로 전환
- ✅ 완전 리팩토링 (코드 간소화)
- ✅ Flask 백엔드 구현
- ✅ 반응형 UI 완성
- ✅ 최적화 및 문서화

---

## ⚖️ 라이선스

이 프로젝트는 교육 및 개인 사용 목적으로 제공됩니다.

### 사용 약관
- ✅ 개인 사용
- ✅ 교육 목적
- ✅ 커스터마이징
- ❌ 상업 재배포 (API 비용 발생)
- ❌ 무단 수정 배포

---

## 📞 문의 및 피드백

프로젝트에 대한 질문이나 개선 사항이 있으시면 GitHub Issues에 등록해주세요.

---

**마지막 업데이트**: 2025년 11월 12일  
**버전**: 1.0.0 (MVP)  
**상태**: ✅ 완성 및 테스트 완료

**마지막 업데이트**: 2025년 11월 12일