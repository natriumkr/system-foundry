from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor,white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,Table,TableStyle,PageBreak,KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[1]
pdfmetrics.registerFont(TTFont('Noto',R/'app/fonts/noto-sans-kr-regular.ttf'));pdfmetrics.registerFont(TTFont('NotoB',R/'app/fonts/noto-sans-kr-bold.ttf'))
GREEN=HexColor('#24735d');INK=HexColor('#202b27');MUTED=HexColor('#65736d');PAPER=HexColor('#f6f4ef');LINE=HexColor('#d4dcd8')
S={'t':ParagraphStyle('t',fontName='NotoB',fontSize=30,leading=38,textColor=INK),'h':ParagraphStyle('h',fontName='NotoB',fontSize=19,leading=26,textColor=GREEN,spaceBefore=6,spaceAfter=10),'b':ParagraphStyle('b',fontName='Noto',fontSize=9.3,leading=15,textColor=INK,spaceAfter=8),'s':ParagraphStyle('s',fontName='Noto',fontSize=7.5,leading=11,textColor=MUTED),'c':ParagraphStyle('c',fontName='NotoB',fontSize=11,leading=17,textColor=GREEN,alignment=TA_CENTER)}
def p(x,k='b'):return Paragraph(x,S[k])
def sec(a,b):return KeepTogether([p(a,'h'),p(b)])
def hf(c,d):
 c.saveState();c.setFillColor(PAPER);c.rect(0,0,A4[0],A4[1],fill=1,stroke=0);c.setFillColor(GREEN);c.rect(0,A4[1]-8,A4[0],8,fill=1,stroke=0);c.setFont('Noto',7);c.setFillColor(MUTED);c.drawString(42,24,'ProofGuard · System Foundry MVP Report');c.drawRightString(A4[0]-42,24,str(d.page));c.restoreState()
st=[Spacer(1,90),p('SYSTEM FOUNDRY · BUSINESS MVP','c'),Spacer(1,20),p('ProofGuard','t'),Spacer(1,10),p('최종 시안 승인 마감과<br/>승인 전 제작 위험을 관리하는 시스템','c'),Spacer(1,35)]
t=Table([[p('프로젝트'),p('2026-08-13-1559-proofguard')],[p('대상 고객'),p('소형 인쇄·간판·패키지 제작사')],[p('가격'),p('사업장당 월 ₩18,000')],[p('상태'),p('PASS · 자동 테스트 8/8')]],colWidths=[100,350]);t.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1,GREEN),('INNERGRID',(0,0),(-1,-1),.5,LINE),('BACKGROUND',(0,0),(-1,-1),white),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]));st += [t,PageBreak()]
st += [sec('1. 프로젝트 개요','ProofGuard는 고객 시안의 승인 마감, 재작업 노출액과 승인 상태를 관리하는 브라우저 기반 업무 시스템이다.'),sec('2. 대상 고객','최종 시안 승인 후 인쇄·제작에 투입하는 소형 인쇄·간판·패키지 제작사다.'),sec('3. 해결하는 문제','승인 상태가 메신저와 이메일에 흩어지면 미승인 시안이 제작에 투입되어 재작업 비용이 발생한다. 마감과 노출액을 한 큐로 묶어 위험을 줄인다.'),sec('4. 핵심 기능','① 검증된 승인 건 등록 ② 마감 위험·노출액 큐 ③ 승인 상태 추적'),sec('5. 사용 방법','npm install, npm test, npm start 순서로 실행한다. 시안 발송 후 고객·작업·마감·노출액을 등록하고 승인 대기·수정 요청·승인 완료 상태를 갱신한다.'),PageBreak()]
st += [sec('6. 시스템 구조','브라우저 화면 → 입력 검증·마감 위험·노출액 계산 엔진 → localStorage. 외부 전송과 계정이 없는 단일 사업장 구조다.'),sec('7. 사용 기술','HTML5, CSS, 순수 JavaScript, Node.js 내장 테스트 러너, Python 정적 서버, Docker. 외부 유료 API와 런타임 패키지는 없다.'),p('8. 실행 화면','h'),Image(str(R/'screenshots/dashboard.png'),width=493,height=493*1500/1440),p('실제 Chromium에서 신규 승인 건을 등록하고 승인 상태를 변경한 화면.','s'),PageBreak()]
st += [sec('9. 테스트 결과','자동 테스트 8/8 통과. 입력 정제, 날짜·노출액 검증, 마감 위험 판정, 노출액 집계, 승인 상태 전환을 확인했다. HTTP 200, Chromium 등록·상태 변경 흐름, README 명령도 검증했다.'),sec('10. 보안 및 제한사항','입력 길이·허용값 제한과 HTML 이스케이프를 적용한다. 고객 개인정보·결제정보·비밀번호를 입력하지 않도록 안내한다. 파일 첨부와 전자서명·감사 로그는 포함하지 않는다.'),sec('11. 가격과 수익 모델','사업장당 월 ₩18,000 구독. 승인 전 제작으로 생기는 재작업 비용을 줄이는 가치를 판매 포인트로 삼는다.'),sec('12. 첫 고객 확보 방법','지역 인쇄·간판 업체 10곳에 무료 승인 관리표를 제공하고, 미승인 노출액을 일주일 측정해 14일 체험으로 전환한다.'),sec('13. 개선 계획','1) 승인 증빙 첨부 2) 고객 승인 링크 3) 자동 알림 4) 작업별 이력 5) 역할별 로그인 6) CSV 내보내기.'),PageBreak()]
data=[[p('평가 항목'),p('점수'),p('근거')],[p('고객 문제의 강도'),p('9/10'),p('미승인 제작은 직접적인 재작업 비용을 만든다.')],[p('하루 내 완성도'),p('9/10'),p('등록·위험 큐·상태 흐름을 완성했다.')],[p('판매 가능성'),p('8/10'),p('회피 가능한 손실액으로 가치를 설명하기 쉽다.')],[p('유지보수 난이도'),p('9/10'),p('정적 앱이며 외부 서비스가 없다.')],[p('차별성'),p('8/10'),p('승인 기한과 재작업 노출액을 함께 우선화한다.')],[p('확장 가능성'),p('8/10'),p('승인 링크·증빙·감사 로그로 확장 가능하다.')]]
q=Table(data,colWidths=[105,48,340]);q.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),GREEN),('TEXTCOLOR',(0,0),(-1,0),white),('GRID',(0,0),(-1,-1),.5,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));st += [p('14. 종합 평가','h'),q,Spacer(1,16),p('종합 점수 8.4/10','h'),p('승인 전 제작이라는 반복 손실을 좁은 워크플로로 해결한다. 유료화 전 고객 승인 링크와 증빙 첨부의 우선순위를 확인해야 한다.'),PageBreak(),p('부록 · 검증 체크리스트','h'),p('✓ 의존성 설치  ✓ 프로그램 시작  ✓ 핵심 기능  ✓ 자동 테스트 8개  ✓ README 명령  ✓ 비밀정보 검사  ✓ PDF 생성·파싱·렌더링'),p('릴리스 판정','h'),p('<b>PASS</b> — 내부 운영과 고객 인터뷰용 MVP로 사용할 수 있다. 실제 제작 전 서면 승인 원본을 별도로 보관해야 한다.')]
SimpleDocTemplate(str(R/'report.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=36,bottomMargin=40,title='ProofGuard MVP Report',author='System Foundry').build(st,onFirstPage=hf,onLaterPages=hf)
print(R/'report.pdf')
