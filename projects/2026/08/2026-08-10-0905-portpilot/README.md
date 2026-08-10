# PortPilot

개인이 보유한 기기와 충전기의 포트·출력을 비교하고 여행용 최소 충전기 구성을 추천하는 로컬 우선 MVP입니다.

## 핵심 기능

- 기기와 충전기 정보 입력 검증
- 포트·정격 출력 기반 호환성 분석
- 여행 기기 선택과 최소 충전기 구성 추천

## 실행

Node.js 18 이상과 Python 3가 필요합니다.

```bash
npm install
npm test
npm start
```

브라우저에서 `http://localhost:4173`을 엽니다. 데이터는 해당 브라우저의 localStorage에만 저장됩니다.

Docker 실행: `docker build -t portpilot . && docker run --rm -p 4173:4173 portpilot`

## 제한사항

USB 전력 협상 규격과 케이블 정격을 자동 판별하지 않습니다. 실제 사용 전 제조사 사양과 안전 인증을 확인하세요.
