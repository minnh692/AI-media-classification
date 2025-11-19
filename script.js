// AI 생성물 판별 분석기 - 클라이언트 로직

let currentFile = null;

// DOM 요소들
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const uploadSection = document.getElementById('uploadSection');
const previewSection = document.getElementById('previewSection');
const imagePreview = document.getElementById('imagePreview');
const videoPreview = document.getElementById('videoPreview');
const changeFileBtn = document.getElementById('changeFileBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const loadingState = document.getElementById('loadingState');
const resultsContent = document.getElementById('resultsContent');
const errorState = document.getElementById('errorState');
const errorMessage = document.getElementById('errorMessage');
const retryBtn = document.getElementById('retryBtn');

// 초기화
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

// 이벤트 리스너 설정
function setupEventListeners() {
    uploadBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    changeFileBtn.addEventListener('click', resetForm);
    analyzeBtn.addEventListener('click', analyzeFile);
    retryBtn.addEventListener('click', () => analyzeFile());
}

// 파일 선택 처리
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) processFile(file);
}

// 드래그 오버
function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

// 드래그 떠남
function handleDragLeave() {
    uploadArea.classList.remove('dragover');
}

// 드롭
function handleDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const file = event.dataTransfer.files[0];
    if (file) processFile(file);
}

// 파일 처리
function processFile(file) {
    // 지원 형식 확인
    const validTypes = [
        'image/jpeg', 'image/png', 'image/webp', 'image/gif',
        'video/mp4', 'video/webm'
    ];
    
    if (!validTypes.includes(file.type)) {
        showError('지원하지 않는 파일 형식입니다.\n지원: JPG, PNG, WebP, GIF, MP4, WebM');
        return;
    }
    
    // 파일 크기 확인 (20MB)
    if (file.size > 20 * 1024 * 1024) {
        showError('파일 크기가 20MB를 초과합니다.');
        return;
    }
    
    currentFile = file;
    displayPreview(file);
}

// 미리보기 표시
function displayPreview(file) {
    uploadSection.style.display = 'none';
    previewSection.style.display = 'block';
    resultsSection.style.display = 'none';
    
    const isImage = file.type.startsWith('image/');
    
    if (isImage) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
            videoPreview.style.display = 'none';
        };
        reader.readAsDataURL(file);
    } else {
        const reader = new FileReader();
        reader.onload = (e) => {
            videoPreview.src = e.target.result;
            videoPreview.style.display = 'block';
            imagePreview.style.display = 'none';
        };
        reader.readAsDataURL(file);
    }
}

// 폼 초기화
function resetForm() {
    currentFile = null;
    fileInput.value = '';
    uploadSection.style.display = 'block';
    previewSection.style.display = 'none';
    resultsSection.style.display = 'none';
}

// 분석 시작
async function analyzeFile() {
    if (!currentFile) {
        showError('파일을 선택해주세요.');
        return;
    }
    
    previewSection.style.display = 'none';
    resultsSection.style.display = 'block';
    loadingState.style.display = 'block';
    resultsContent.style.display = 'none';
    errorState.style.display = 'none';
    
    try {
        // Base64 변환
        const base64Data = await fileToBase64(currentFile);
        
        // API 호출
        const response = await fetch('http://localhost:5000/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                imageData: base64Data,
                mediaType: currentFile.type
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'API 호출 실패');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        console.error('분석 중 오류:', error);
        showError(error.message || '분석 중 오류가 발생했습니다. 다시 시도해주세요.');
    }
}

// Base64 변환
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
            const base64 = reader.result.split(',')[1];
            resolve(base64);
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// 결과 표시
function displayResults(data) {
    loadingState.style.display = 'none';
    resultsContent.style.display = 'block';
    
    const confidence = Math.round(data.confidence || 0);
    const verdict = data.verdict || 'UNCERTAIN';
    
    // confidence는 항상 AI 생성 가능성을 나타냄 (0-100)
    // 바가 많이 채워질수록 AI 가능성 높음
    const confidenceFill = document.getElementById('confidenceFill');
    const confidenceValue = document.getElementById('confidenceValue');
    const confidenceLabel = document.getElementById('confidenceLabel');
    
    confidenceFill.style.width = confidence + '%';
    confidenceValue.textContent = confidence + '%';
    
    // 퍼센테이지에 맞는 라벨 표시
    confidenceLabel.className = '';
    if (confidence < 30) {
        confidenceLabel.textContent = '낮음 (인간 생성)';
        confidenceLabel.classList.add('confidence-label-low');
    } else if (confidence < 70) {
        confidenceLabel.textContent = '중간 (불확실)';
        confidenceLabel.classList.add('confidence-label-medium');
    } else {
        confidenceLabel.textContent = '높음 (AI 생성)';
        confidenceLabel.classList.add('confidence-label-high');
    }
    
    // 판정 (verdict는 참고용, confidence가 주요 지표)
    const verdictCard = document.getElementById('verdictCard');
    const verdictText = document.getElementById('verdictText');
    
    verdictCard.className = 'card verdict';
    if (verdict === 'LIKELY_AI' || confidence >= 70) {
        verdictText.innerHTML = '🤖 <strong>AI 생성물일 가능성이 높습니다.</strong>';
    } else if (verdict === 'LIKELY_HUMAN' || confidence < 30) {
        verdictText.innerHTML = '👤 <strong>인간이 생성한 콘텐츠일 가능성이 높습니다.</strong>';
    } else {
        verdictText.innerHTML = '❓ <strong>판별이 불확실합니다.</strong>';
    }
    
    // 신호
    const signalsList = document.getElementById('signalsList');
    signalsList.innerHTML = '';
    
    if (data.signals && data.signals.length > 0) {
        data.signals.forEach(signal => {
            const item = document.createElement('div');
            item.className = 'signal-item';
            item.innerHTML = `<strong>${signal.title}</strong><p>${signal.description}</p>`;
            signalsList.appendChild(item);
        });
    } else {
        signalsList.innerHTML = '<p style="color: var(--gray);">특이한 신호가 감지되지 않았습니다.</p>';
    }
    
    // 상세 분석
    document.getElementById('textureAnalysis').textContent = data.texture_analysis || '분석 중';
    document.getElementById('lightingAnalysis').textContent = data.lighting_analysis || '분석 중';
    document.getElementById('detailAnalysis').textContent = data.detail_analysis || '분석 중';
    document.getElementById('backgroundAnalysis').textContent = data.background_analysis || '분석 중';
    
    // 요약
    document.getElementById('summaryText').textContent = data.summary || '분석 완료';
}

// 에러 표시
function showError(message) {
    loadingState.style.display = 'none';
    resultsContent.style.display = 'none';
    errorState.style.display = 'block';
    errorMessage.textContent = message;
}

