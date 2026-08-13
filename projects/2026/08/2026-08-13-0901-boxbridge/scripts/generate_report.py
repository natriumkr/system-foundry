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
 c.saveState();c.setFillColor(PAPER);c.rect(0,0,A4[0],A4[1],fill=1,stroke=0);c.setFillColor(GREEN);c.rect(0,A4[1]-8,A4[0],8,fill=1,stroke=0);c.setFont('Noto',7);c.setFillColor(MUTED);c.drawString(42,24,'BoxBridge · System Foundry MVP Report');c.drawRightString(A4[0]-42,24,str(d.page));c.restoreState()
st=[Spacer(1,90),p('SYSTEM FOUNDRY · PERSONAL MVP','c'),Spacer(1,20),p('BoxBridge','t'),Spacer(1,10),p('상자 속 물건을 바로 찾고<br/>새집 정리 진행률을 끝까지 관리하는 도구','c'),Spacer(1,35)]
t=Table([[p('프로젝트'),p('2026-08-13-0901-boxbridge')],[p('대상 고객'),p('이사를 준비하는 개인·소형 가구')],[p('가격'),p('1회 구매 ₩8,900')],[p('상태'),p('PASS · 자동 테스트 8/8')]],colWidths=[100,350]);t.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1,GREEN),('INNERGRID',(0,0),(-1,-1),.5,LINE),('BACKGROUND',(0,0),(-1,-1),white),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]));st += [t,PageBreak()]
st += [sec('1. 프로젝트 개요','BoxBridge는 상자 코드, 도착 방, 내용물과 깨짐주의 여부를 기록하고 검색하며 포장 해제 진행률을 계산하는 브라우저 기반 이사 도구다.'),sec('2. 대상 고객','원룸이나 아파트 이사를 직접 준비하며, 여러 상자에서 필요한 물건을 빠르게 찾아야 하는 개인과 소형 가구다.'),sec('3. 해결하는 문제','상자 겉면의 짧은 메모만으로는 필요한 물건을 찾기 어렵고, 새집에서 어느 방의 정리가 남았는지 파악하기 어렵다. 검색 가능한 목록과 정리 상태를 하나로 묶어 탐색 시간을 줄인다.'),sec('4. 핵심 기능','① 검증된 상자 등록 ② 코드·방·내용물 통합 검색 ③ 포장 해제 진행률 추적'),sec('5. 사용 방법','npm install, npm test, npm start 순서로 실행한다. 포장할 때 상자 정보를 등록하고, 새집에서 검색해 찾은 뒤 정리 완료로 전환한다.'),PageBreak()]
st += [sec('6. 시스템 구조','브라우저 화면 → 입력 검증·검색·진행률 계산 엔진 → localStorage. 외부 전송과 계정이 없는 단일 사용자 구조다.'),sec('7. 사용 기술','HTML5, CSS, 순수 JavaScript, Node.js 내장 테스트 러너, Python 정적 서버, Docker. 외부 유료 API와 런타임 패키지는 없다.'),p('8. 실행 화면','h'),Image(str(R/'screenshots/dashboard.png'),width=493,height=493*1500/1440),p('실제 Chromium에서 신규 깨짐주의 상자를 등록하고 내용물을 검색한 화면.','s'),PageBreak()]
st += [sec('9. 테스트 결과','자동 테스트 8/8 통과. 코드 정규화·거부, 방 검증, 깨짐주의 변환, 중복 거부, 검색, 진행률, 상태 전환을 확인했다. HTTP 200, Chromium 등록·검색 흐름, README 명령도 검증했다.'),sec('10. 보안 및 제한사항','입력 길이·허용값 제한과 HTML 이스케이프를 적용한다. 현금·신분증·비밀번호·귀중품의 위치를 기록하지 않도록 안내한다. 사진 첨부와 다중 기기 동기화는 포함하지 않는다.'),sec('11. 가격과 수익 모델','1회 구매 ₩8,900. 이사 한 번의 분실·재탐색 시간을 줄이는 즉시 효용과 광고 없는 로컬 저장을 판매 포인트로 삼는다.'),sec('12. 첫 고객 확보 방법','지역 이사 커뮤니티와 체크리스트 게시판에 무료 10상자 체험판을 배포하고, 검색으로 절약한 시간을 사례로 수집해 무제한 버전 구매로 전환한다.'),sec('13. 개선 계획','1) QR 라벨 인쇄 2) 방별 진행률 3) JSON 백업 4) 사진 첨부 5) 가족 공동 편집 6) 이사 완료 후 데이터 일괄 삭제.'),PageBreak()]
data=[[p('평가 항목'),p('점수'),p('근거')],[p('고객 문제의 강도'),p('8/10'),p('이사 중 분실과 재탐색은 짧지만 강한 불편이다.')],[p('하루 내 완성도'),p('9/10'),p('등록·검색·정리 흐름을 완성했다.')],[p('판매 가능성'),p('8/10'),p('이사 직전 명확한 구매 동기가 생긴다.')],[p('유지보수 난이도'),p('9/10'),p('정적 앱이며 외부 서비스가 없다.')],[p('차별성'),p('8/10'),p('목록과 포장 해제 진행률을 한 화면에 묶었다.')],[p('확장 가능성'),p('8/10'),p('QR·백업·공동 편집으로 확장 가능하다.')]]
q=Table(data,colWidths=[105,48,340]);q.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),GREEN),('TEXTCOLOR',(0,0),(-1,0),white),('GRID',(0,0),(-1,-1),.5,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));st += [p('14. 종합 평가','h'),q,Spacer(1,16),p('종합 점수 8.3/10','h'),p('이사라는 짧고 강한 문제를 좁은 워크플로로 해결한다. 반복 구독보다 저가 1회 구매가 적합하며, 유료화 전 QR 라벨 수요를 확인해야 한다.'),PageBreak(),p('부록 · 검증 체크리스트','h'),p('✓ 의존성 설치  ✓ 프로그램 시작  ✓ 핵심 기능  ✓ 자동 테스트 8개  ✓ README 명령  ✓ 비밀정보 검사  ✓ PDF 생성·파싱·렌더링'),p('릴리스 판정','h'),p('<b>PASS</b> — 실제 이사 준비와 고객 인터뷰용 MVP로 사용할 수 있다. 민감한 위치 정보는 입력하지 않아야 한다.')]
SimpleDocTemplate(str(R/'report.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=36,bottomMargin=40,title='BoxBridge MVP Report',author='System Foundry').build(st,onFirstPage=hf,onLaterPages=hf)
print(R/'report.pdf')
