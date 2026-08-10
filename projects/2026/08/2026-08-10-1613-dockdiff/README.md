# DockDiff

소형 매장이 주문 수량과 실수령 수량의 차이, 회수 대상액, 이의 제기 기한을 관리하는 로컬 우선 MVP입니다.

## 핵심 기능

- 납품·발주 정보 입력 검증
- 부족 수량·회수 금액·기한 위험도 계산
- 거래처 처리 완료 상태 추적

## 실행

Node.js 18 이상과 Python 3가 필요합니다.

```bash
npm install
npm test
npm start
```

브라우저에서 `http://localhost:4173`을 엽니다. 데이터는 해당 브라우저의 localStorage에만 저장됩니다.

Docker 실행: `docker build -t dockdiff . && docker run --rm -p 4173:4173 dockdiff`

## 제한사항

회계·법률 판단이나 거래처 연락 기능은 포함하지 않습니다. 실제 이의 제기 기한은 발주서와 거래처 약관을 확인하세요.
