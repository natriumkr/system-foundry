# ClaimClock

소규모 온라인 판매자가 교환·반품·환불 요청의 처리기한과 진행 상태를 놓치지 않도록 돕는 로컬 우선 업무 시스템입니다.

## 핵심 기능

1. 주문번호, 유형, 금액, 처리기한을 검증해 업무 건으로 등록
2. 기한 초과·48시간 이내·주의·안전 단계로 자동 분류하는 대시보드
3. 접수·대기·완료 상태 갱신과 미처리 금액 집계

## 설치 및 실행

Python 3.11 이상이 필요하며 외부 런타임 패키지는 없습니다.

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
cp .env.example .env
# .env의 두 값을 임의의 강한 값으로 바꾼 뒤:
set -a && . ./.env && set +a
python3 -m app.server
```

브라우저에서 `http://127.0.0.1:8080`을 열고 설정한 접속 코드를 입력합니다. 기본값이나 내장 관리자 계정은 없습니다.

## 테스트

```bash
python3 -m unittest discover -s tests -v
```

## Docker

```bash
docker build -t claimclock .
docker run --rm -p 127.0.0.1:8080:8080 \
  -e CLAIMCLOCK_HOST=0.0.0.0 \
  -e CLAIMCLOCK_ACCESS_KEY='replace-with-12-plus-chars' \
  -e CLAIMCLOCK_SESSION_SECRET='replace-with-24-plus-random-chars' \
  claimclock
```

공개 인터넷에 배포할 때는 TLS를 제공하는 리버스 프록시와 별도의 사용자 인증 체계를 추가하세요.

## 데이터와 보안

- SQLite 데이터는 기본적으로 `data/claimclock.db`에 저장되고 Git에서 제외됩니다.
- 접속 코드와 세션 서명키는 환경변수로만 받습니다.
- 모든 변경 요청은 서명된 세션 쿠키와 CSRF 토큰을 검사합니다.
- 입력 길이·유형·금액·날짜 범위를 검증하고 SQL 파라미터 바인딩을 사용합니다.
- 고객 실명 대신 별칭을 쓰는 것을 권장합니다.

## 가격 모델

- 셀프호스팅 1개 매장: 월 19,000원
- 초기 고객은 스마트스토어·자사몰을 운영하며 하루 5건 이상 고객 요청을 처리하는 소형 판매자입니다.

## 제한사항

단일 관리자 MVP입니다. 쇼핑몰 주문 자동 연동, 팀별 권한, 이메일 알림, 첨부파일은 후속 버전 범위입니다.
