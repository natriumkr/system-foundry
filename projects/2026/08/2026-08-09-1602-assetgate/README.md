# AssetGate

소형 웹·디자인·마케팅 제작사가 고객 자료 수신 상태와 프로젝트 착수 준비도를 관리하는 로컬 우선 MVP입니다.

## 핵심 기능

- 고객 자료 요청과 마감일 입력 검증
- 마감 위험도·프로젝트 준비도·잠재 지연일 집계
- 자료 수신 완료 상태 추적

## 실행

Node.js 18 이상과 Python 3가 필요합니다.

```bash
npm install
npm test
npm start
```

브라우저에서 `http://localhost:4173`을 엽니다. 데이터는 해당 브라우저의 localStorage에만 저장됩니다.

Docker 실행: `docker build -t assetgate . && docker run --rm -p 4173:4173 assetgate`

## 보안과 제한

비밀번호·API 키 같은 실제 자격 증명은 입력하지 마세요. 이 MVP는 파일 업로드, 이메일 발송, 팀 동기화를 포함하지 않습니다.
