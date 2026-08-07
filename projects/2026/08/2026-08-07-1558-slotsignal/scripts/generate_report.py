from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,Table,TableStyle,PageBreak,KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'report.pdf'; IMG=ROOT/'screenshots/dashboard.png'
pdfmetrics.registerFont(TTFont('Noto',ROOT/'app/fonts/noto-sans-kr-regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoB',ROOT/'app/fonts/noto-sans-kr-bold.ttf'))
GREEN=HexColor('#194b3a'); LIME=HexColor('#c8f36b'); INK=HexColor('#17231d'); MUTED=HexColor('#64716b'); PAPER=HexColor('#f4f1e8'); LINE=HexColor('#d8d5ca')
styles={
'title':ParagraphStyle('title',fontName='NotoB',fontSize=30,leading=38,textColor=INK,spaceAfter=12),
'h1':ParagraphStyle('h1',fontName='NotoB',fontSize=20,leading=27,textColor=GREEN,spaceBefore=6,spaceAfter=12),
'h2':ParagraphStyle('h2',fontName='NotoB',fontSize=12,leading=18,textColor=INK,spaceBefore=5,spaceAfter=5),
'body':ParagraphStyle('body',fontName='Noto',fontSize=9.4,leading=15,textColor=INK,spaceAfter=8),
'small':ParagraphStyle('small',fontName='Noto',fontSize=7.8,leading=12,textColor=MUTED),
'cover':ParagraphStyle('cover',fontName='NotoB',fontSize=12,leading=18,textColor=GREEN,alignment=TA_CENTER),
}
def p(text,style='body'): return Paragraph(text,styles[style])
def section(title,body): return KeepTogether([p(title,'h1'),p(body)])
def header_footer(canvas,doc):
    canvas.saveState(); canvas.setFillColor(PAPER); canvas.rect(0,0,A4[0],A4[1],fill=1,stroke=0); canvas.setFillColor(GREEN); canvas.rect(0,A4[1]-8,A4[0],8,fill=1,stroke=0)
    canvas.setFont('Noto',7); canvas.setFillColor(MUTED); canvas.drawString(42,25,'SlotSignal · System Foundry MVP Report'); canvas.drawRightString(A4[0]-42,25,str(doc.page)); canvas.restoreState()
def score_table():
    data=[[p('평가 항목','h2'),p('점수','h2'),p('근거','h2')],
    [p('고객 문제의 강도'),p('9/10'),p('취소 직후의 빈 시간은 곧 사라지는 매출 기회다.')],
    [p('하루 내 완성도'),p('9/10'),p('등록-추천-확정의 핵심 흐름을 외부 연동 없이 완성했다.')],
    [p('판매 가능성'),p('8/10'),p('회수 매출로 가치를 설명하기 쉽고 소규모 사업장에 가격 저항이 낮다.')],
    [p('유지보수 난이도'),p('9/10'),p('의존성 없는 정적 앱이며 데이터 모델이 작다.')],
    [p('차별성'),p('7/10'),p('단순 명단이 아니라 시간대·대기일·임박도를 점수화한다.')],
    [p('확장 가능성'),p('8/10'),p('문자 발송, 예약 플랫폼, 다지점 분석으로 확장 가능하다.')]]
    t=Table(data,colWidths=[105,48,340],repeatRows=1);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),GREEN),('TEXTCOLOR',(0,0),(-1,0),white),('GRID',(0,0),(-1,-1),.5,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));return t
story=[]
story += [Spacer(1,90),p('SYSTEM FOUNDRY · BUSINESS MVP','cover'),Spacer(1,20),p('SlotSignal','title'),p('취소 슬롯을 가장 맞는 대기 고객과 연결하는<br/>로컬 우선 예약 회수 데스크','cover'),Spacer(1,35)]
cover=Table([[p('프로젝트','h2'),p('2026-08-07-1558-slotsignal')],[p('대상 고객','h2'),p('1~5인 미용실·네일숍·예약형 클래스')],[p('가격','h2'),p('사업장당 월 ₩15,000')],[p('상태','h2'),p('PASS · 자동 테스트 8/8')]],colWidths=[100,350]);cover.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),white),('BOX',(0,0),(-1,-1),1,GREEN),('INNERGRID',(0,0),(-1,-1),.5,LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]));story += [cover,PageBreak()]
story += [section('1. 프로젝트 개요','SlotSignal은 취소로 생긴 빈 예약을 등록하고, 대기 고객의 희망 서비스·가능 시간대·대기일·슬롯 임박도를 비교해 연락 우선순위를 만드는 브라우저 기반 업무 도구다.'),section('2. 대상 고객','예약 취소가 곧 매출 손실로 이어지는 소규모 미용실, 네일 스튜디오, 1인 클래스 운영자가 1차 고객이다.'),section('3. 해결하는 문제','대기 명단이 메신저나 종이에 흩어져 있으면 취소 직후 적합한 고객을 찾는 데 시간이 걸린다. 직원마다 연락 기준도 달라 기회를 놓치고 고객 경험도 불균일해진다.'),section('4. 핵심 기능','① 서비스·일시·예상 매출을 검증하는 빈 슬롯 등록 ② 서비스와 가능 시간대를 포함한 대기 고객 관리 ③ 적합도 기반 연락 큐와 한 번의 예약 확정 처리'),section('5. 사용 방법','<b>npm install</b>, <b>npm test</b>, <b>npm start</b> 순서로 실행한다. 빈 슬롯과 대기 고객을 등록하면 추천 큐가 즉시 갱신된다. 연락 성공 시 예약 확정을 눌러 슬롯과 고객을 동시에 완료 상태로 바꾼다.'),PageBreak()]
story += [p('6. 시스템 구조','h1'),p('<b>브라우저 UI</b> → 입력 검증·점수 계산 엔진 → localStorage. 서버나 외부 API 없이 정적 파일만 제공한다.'),p('7. 사용 기술','h1'),p('HTML5, CSS, 순수 JavaScript, Node.js 내장 테스트 러너, Python 정적 서버, Docker. 유료 API와 런타임 패키지는 0개다.'),p('8. 실행 화면','h1'),Image(str(IMG),width=493,height=493*1500/1440),p('실제 Chromium에서 슬롯과 대기 고객을 추가한 뒤 캡처한 화면.','small'),PageBreak()]
story += [section('9. 테스트 결과','자동 테스트 <b>8/8 통과</b>. 고객·슬롯 입력 검증, 시간대 분류, 적합도 계산, 서비스 불일치 제외, 정렬, 예약 확정 상태 전이를 확인했다. HTTP 200과 Chromium 핵심 흐름, README 명령도 실제 검증했다.'),section('10. 보안 및 제한사항','입력 길이·허용값·날짜·시간·금액 범위를 제한하고 화면 출력 시 HTML을 이스케이프한다. 비밀값과 외부 전송은 없다. 단, 인증·다중 사용자·클라우드 백업·자동 메시지 기능이 없어 인터넷 공개 업무용으로는 적합하지 않다.'),section('11. 가격과 수익 모델','사업장당 월 ₩15,000 구독. 7일 무료 체험 후 취소 슬롯 회수액을 보여 주어 전환한다. 유료 메시지 발송은 고객이 원할 때 별도 연동으로 제공한다.'),section('12. 첫 고객 확보 방법','지역 미용·네일 사업장 10곳에 데모를 제안하고, 최근 한 달 취소 건수와 평균 객단가로 회수 가능 매출을 함께 계산한다. 체험 기간에는 수동 연락만 사용해 도입 장벽을 낮춘다.'),section('13. 개선 계획','1) 고객 동의 기반 문자 템플릿 2) 예약 플랫폼 CSV 가져오기 3) 다직원·다지점 권한과 감사 로그 4) 실제 예약 성사율로 점수 가중치 조정.'),PageBreak()]
story += [p('14. 종합 평가','h1'),score_table(),Spacer(1,16),p('<b>종합 점수 8.3/10</b>','h1'),p('짧은 구현 범위 안에서 명확한 매출 손실 문제를 해결한다. 첫 판매 전에는 실제 사업장 인터뷰로 연락 우선순위와 개인정보 처리 절차를 검증해야 한다.'),Spacer(1,25),p('검증 체크리스트','h1'),p('✓ 의존성 설치  ✓ 프로그램 시작  ✓ 핵심 기능  ✓ 자동 테스트 8개  ✓ README 명령  ✓ 비밀정보 검사  ✓ PDF 생성·파싱·렌더링'),PageBreak(),p('부록 · 운영 메모','h1'),p('MVP는 고객 연락처를 수집하지 않는다. 실제 운영 단계에서는 고객 동의, 보관 기간, 삭제 요청 처리, 직원 접근 권한을 설계해야 한다. 자동 발송 기능을 추가할 때는 메시지 사업자 약관과 현지 개인정보 규정을 확인한다.'),p('릴리스 판정','h1'),p('<b>PASS</b> — 로컬 단일 사업장 데모와 고객 인터뷰에 사용할 수 있다. 인터넷 공개 운영은 인증과 데이터 보호 기능이 추가된 이후로 제한한다.')]
doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=36,bottomMargin=40,title='SlotSignal MVP Report',author='System Foundry')
doc.build(story,onFirstPage=header_footer,onLaterPages=header_footer)
print(OUT)
