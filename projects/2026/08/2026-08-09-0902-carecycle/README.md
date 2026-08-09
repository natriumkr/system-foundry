# CareCycle

가정용 필터·청소·가전·취미 장비의 관리 주기와 예상 비용을 브라우저 안에서 관리하는 로컬 우선 MVP입니다.

## 핵심 기능

- 관리 항목과 반복 주기 입력 검증
- 지연·7일·30일 기준 우선순위 큐와 연간 예상 비용
- 오늘 완료 처리 시 다음 관리일 자동 계산

## 실행

Node.js 18 이상과 Python 3가 필요합니다.

```bash
npm install
npm test
npm start
```

브라우저에서 `http://localhost:4173`을 엽니다. 데이터는 해당 브라우저의 localStorage에만 저장됩니다.

Docker 실행: `docker build -t carecycle . && docker run --rm -p 4173:4173 carecycle`

## 제한사항

알림과 기기 간 동기화는 포함하지 않습니다. 안전 관련 설비는 앱의 계산보다 제조사 지침과 전문가 점검을 우선하세요.
