# PackWise

여행 짐 체크리스트와 수하물 중량 계산기를 결합한 로컬 우선 웹 도구입니다. 물건별 수량과 무게를 기록하면 허용 중량까지 남은 여유와 포장 진행률을 즉시 확인할 수 있습니다.

## 핵심 기능

1. 포장 체크리스트와 진행률
2. 물건별 수량·무게 기반 수하물 초과 경고
3. 브라우저 자동 저장 및 JSON 백업

## 요구사항

- Python 3.10 이상(정적 파일 서버)
- Node.js 20 이상(테스트)

## 실행

```bash
python3 -m http.server 8080 -d app
```

브라우저에서 <http://localhost:8080>을 엽니다.

Docker 실행:

```bash
docker build -t packwise .
docker run --rm -p 8080:8080 packwise
```

## 테스트

외부 패키지가 필요하지 않습니다.

```bash
npm test
```

## 데이터와 보안

- 입력 데이터는 브라우저 `localStorage`에만 저장됩니다.
- 서버, 계정, 분석 도구, 외부 API가 없습니다.
- 이름·수량·무게·허용 중량을 범위 검사합니다.
- 실제 항공사의 휴대·위탁 수하물 및 제한품 규정은 출발 전에 별도로 확인해야 합니다.

## 프로젝트 구조

```text
app/          정적 웹 애플리케이션
tests/        Node.js 자동 테스트
screenshots/  검증된 실행 화면
scripts/      PDF 보고서 생성기
logs/         생성 및 검증 로그
report.pdf    프로젝트 보고서
```

## 라이선스

애플리케이션 코드는 MIT이며 포함된 Noto Sans KR 서브셋은 OFL-1.1입니다.
