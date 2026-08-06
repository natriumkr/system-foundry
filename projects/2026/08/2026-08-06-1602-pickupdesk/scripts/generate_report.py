from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'report.pdf'
pdfmetrics.registerFont(TTFont('PickupSans',ROOT/'app/fonts/noto-sans-kr-regular.ttf'))
pdfmetrics.registerFont(TTFont('PickupSans-Bold',ROOT/'app/fonts/noto-sans-kr-bold.ttf'))
INK=colors.HexColor('#17211b'); GREEN=colors.HexColor('#275b45'); LIME=colors.HexColor('#dfff73'); PAPER=colors.HexColor('#f5f2e9'); ORANGE=colors.HexColor('#ff7b54'); MUTED=colors.HexColor('#667069')
styles=getSampleStyleSheet();
title=ParagraphStyle('title',fontName='PickupSans-Bold',fontSize=29,leading=36,textColor=INK,spaceAfter=12)
h1=ParagraphStyle('h1',fontName='PickupSans-Bold',fontSize=20,leading=25,textColor=INK,spaceBefore=5,spaceAfter=10)
h2=ParagraphStyle('h2',fontName='PickupSans-Bold',fontSize=12,leading=17,textColor=GREEN,spaceBefore=9,spaceAfter=5)
body=ParagraphStyle('body',fontName='PickupSans',fontSize=9.5,leading=15,textColor=INK,spaceAfter=7)
small=ParagraphStyle('small',fontName='PickupSans',fontSize=8,leading=12,textColor=MUTED)
center=ParagraphStyle('center',parent=body,alignment=TA_CENTER)
def P(text,style=body): return Paragraph(text,style)
def section(name,text): return KeepTogether([P(name,h2),P(text)])
def table(data,widths):
    t=Table(data,colWidths=widths,repeatRows=1)
    t.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'PickupSans',8),('FONT',(0,0),(-1,0),'PickupSans-Bold',8),('BACKGROUND',(0,0),(-1,0),GREEN),('TEXTCOLOR',(0,0),(-1,0),colors.white),('BACKGROUND',(0,1),(-1,-1),colors.white),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#cfd3cc')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));return t
def decorate(canvas,doc):
    canvas.saveState(); canvas.setFillColor(PAPER); canvas.rect(0,0,A4[0],A4[1],fill=1,stroke=0)
    canvas.setFillColor(GREEN); canvas.rect(0,A4[1]-9*mm,A4[0],9*mm,fill=1,stroke=0)
    canvas.setFont('PickupSans-Bold',8);canvas.setFillColor(colors.white);canvas.drawString(18*mm,A4[1]-6*mm,'SYSTEM FOUNDRY / PICKUPDESK')
    canvas.setFont('PickupSans',7);canvas.setFillColor(MUTED);canvas.drawRightString(A4[0]-18*mm,10*mm,f'{doc.page} / 6')
    canvas.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=20*mm,bottomMargin=17*mm,title='PickupDesk 프로젝트 보고서',author='System Foundry')
story=[]
story += [Spacer(1,8*mm),P('PickupDesk',title),P('수리 완료 물품을 제때 수령·결제까지 연결하는<br/>로컬 우선 업무 시스템',ParagraphStyle('sub',parent=h1,fontSize=16,leading=23,textColor=GREEN)),Spacer(1,7*mm)]
summary=Table([[P('BUSINESS MVP',small),P('월 ₩18,000',h1)],[P('상태',small),P('PASS · 테스트 8/8',h2)],[P('종합 평가',small),P('8.3 / 10',h1)]],colWidths=[50*mm,70*mm]);summary.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.white),('BOX',(0,0),(-1,-1),.8,INK),('INNERGRID',(0,0),(-1,-1),.35,colors.HexColor('#ccd1ca')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]));story += [summary,Spacer(1,7*mm)]
story += [section('1. 프로젝트 개요','PickupDesk는 수리 완료 물품의 수령 약속일, 미수금, 보관료와 상태를 한 화면에서 관리한다. 계정이나 외부 서버 없이 매장 PC 한 대에서 바로 쓸 수 있다.'),section('2. 대상 고객','소형 전자기기·자전거·생활용품 수리점 중 완료 물품을 종이 메모나 메신저로 관리하는 1~5인 사업장.'),section('3. 해결하는 문제','수리가 끝나도 고객 수령이 늦어지면 제한된 보관 공간이 줄고, 미수금 회수가 지연된다. 약속일과 금액이 흩어져 있으면 누구에게 먼저 연락할지도 불명확하다.'),PageBreak()]
story += [P('운영 흐름과 구조',title),section('4. 핵심 기능','① 검증된 수리 완료 등록 ② 약속 경과·오늘·임박 순 연락 큐 ③ 미수금·보관료·수령 완료 집계.'),section('5. 사용 방법','수리 완료 시 접수번호, 고객 별칭, 물품, 완료일, 수령 약속일과 미수금을 등록한다. 큐 상단 고객부터 연락하고 물품 인계·결제 후 수령 완료 처리한다.'),section('6. 시스템 구조','정적 UI → 입력 검증·비용 계산 엔진 → 브라우저 localStorage. 서버·데이터베이스·외부 API가 없는 단일 사용자 구조다.'),section('7. 사용 기술','HTML5, CSS, JavaScript, localStorage, Node.js 내장 테스트 러너, Python 정적 서버. PDF는 ReportLab으로 생성했다.'),Spacer(1,6*mm),table([[P('입력',small),P('처리',small),P('출력',small)],[P('별칭·물품·날짜·금액'),P('범위 검증 → 대기일·보관료·위험도 계산'),P('긴급도 큐·회수 예정액·완료 상태')]], [47*mm,70*mm,48*mm]),PageBreak()]
story += [P('8. 실행 화면',title),P('Chromium에서 실제 등록 흐름을 실행한 뒤 캡처한 1440×1400 화면이다. 샘플 3건에서 신규 1건을 추가해 수령 대기 4건, 회수 예정액 ₩345,500을 확인했다.',body),Spacer(1,4*mm)]
img=Image(str(ROOT/'screenshots/dashboard.png'),width=165*mm,height=160.4*mm);story += [img,Spacer(1,3*mm),P('그림 1. 연락 우선순위, 금액 집계, 등록 폼이 결합된 실제 실행 화면',center),PageBreak()]
story += [P('검증과 안전성',title),section('9. 테스트 결과','의존성 설치 성공. 자동 테스트 8/8 통과. HTTP 200과 제목을 확인했다. Chromium에서 초기 집계(3건·₩295,500), 신규 등록(4건·₩345,500), 수령 완료 후 집계(3건·₩242,500)를 검증했다.'),table([[P('검증 항목',small),P('결과',small)],[P('입력 정규화·필수값'),P('PASS')],[P('금액·날짜·상태 범위'),P('PASS')],[P('대기일·보관료·총 회수액'),P('PASS')],[P('긴급도 분류·정렬'),P('PASS')],[P('완료 상태와 대시보드'),P('PASS')],[P('HTTP·README·Chromium'),P('PASS')]], [115*mm,50*mm]),Spacer(1,7*mm),section('10. 보안 및 제한사항','연락처·주소 대신 고객 별칭만 저장하고, 입력 범위 검증과 HTML 이스케이프를 적용했다. .env와 자격 증명 패턴을 검사한다. 데이터는 브라우저 로컬에만 있어 기기 분실·브라우저 초기화 시 복구되지 않으며 다중 사용자 동기화와 자동 메시지는 없다. 보관료는 단순 추정치이므로 실제 청구 전 고지·동의와 관련 규정을 확인해야 한다.'),PageBreak()]
story += [P('시장 진입 계획',title),section('11. 가격과 수익 모델','사업장당 월 ₩18,000. 14일 체험 후 로컬 사용 라이선스로 전환한다. 초기에는 결제·문자 API 비용 없이 낮은 운영비를 유지한다.'),section('12. 첫 고객 확보 방법','동네 전자기기·자전거 수리점 10곳에 “완료 물품 보관 현황표” 무료 설치를 제안한다. 2주 동안 수령 지연 건수와 회수 금액을 기록해 전후 효과를 보여주고, 유료 전환 2곳을 첫 목표로 삼는다.'),section('13. 개선 계획','1단계 JSON 백업·복원, 2단계 CSV 내보내기와 직원별 권한, 3단계 명시적 동의를 받은 문자 템플릿 연동. 법적·운영 검토 전 보관료 자동 청구는 구현하지 않는다.'),Spacer(1,8*mm),table([[P('핵심 가설',small),P('초기 검증 지표',small)],[P('연락 큐가 방치 물품을 줄인다'),P('14일 이상 대기 건수 변화')],[P('금액 표시가 회수를 앞당긴다'),P('완료→결제 평균 일수')],[P('월 ₩18,000 지불 의사가 있다'),P('10개 매장 중 유료 전환 수')]], [82*mm,83*mm]),PageBreak()]
ratings=[('고객 문제의 강도',8,'공간 점유와 미수금은 소형 매장에 직접적인 운영 부담이다.'),('하루 내 완성도',9,'핵심 등록·정렬·집계·완료 흐름을 독립 실행형으로 완성했다.'),('판매 가능성',8,'회수 금액과 방치 건수라는 명확한 성과로 가치를 설명할 수 있다.'),('유지보수 난이도',9,'외부 API와 서버가 없어 초기 유지비와 장애 지점이 적다.'),('차별성',8,'범용 CRM보다 수리 완료 후 수령·보관 단계에만 집중한다.'),('확장 가능성',8,'백업, 직원 권한, 동의 기반 메시지로 자연스럽게 확장된다.')]
story += [P('14. 종합 평가',title),P('평균 8.3 / 10',ParagraphStyle('score',parent=title,fontSize=24,textColor=GREEN)),P('하루 MVP로서 문제·기능·가격이 선명하다. 실제 판매 전에는 수리점 인터뷰와 보관료 운영 규정 확인이 가장 중요하다.',body),Spacer(1,5*mm),table([[P('평가 항목',small),P('점수',small),P('근거',small)]]+[[P(a),P(f'{b}/10'),P(c)] for a,b,c in ratings],[42*mm,22*mm,101*mm]),Spacer(1,8*mm),P('최종 판단',h2),P('조건부 출시 권장. 연락처를 저장하지 않는 로컬 MVP로 파일럿을 시작하고, 수령 지연 감소 효과가 확인된 뒤 동기화·메시지 기능을 추가한다.'),Spacer(1,10*mm),P('Generated and verified on 2026-08-06 · No paid API used',center)]
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
print(OUT)
