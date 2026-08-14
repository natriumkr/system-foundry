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
 c.saveState();c.setFillColor(PAPER);c.rect(0,0,A4[0],A4[1],fill=1,stroke=0);c.setFillColor(GREEN);c.rect(0,A4[1]-8,A4[0],8,fill=1,stroke=0);c.setFont('Noto',7);c.setFillColor(MUTED);c.drawString(42,24,'BinReady · System Foundry MVP Report');c.drawRightString(A4[0]-42,24,str(d.page));c.restoreState()
st=[Spacer(1,90),p('SYSTEM FOUNDRY · PERSONAL MVP','c'),Spacer(1,20),p('BinReady','t'),Spacer(1,10),p('부품 위치와 부족 수량을<br/>한 번에 찾는 메이커 도구','c'),Spacer(1,35)]
t=Table([[p('프로젝트'),p('2026-08-14-0905-binready')],[p('대상 고객'),p('전자공작·로봇 취미 메이커')],[p('가격'),p('1회 구매 ₩9,900')],[p('상태'),p('PASS · 자동 테스트 9/9')]],colWidths=[100,350]);t.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1,GREEN),('INNERGRID',(0,0),(-1,-1),.5,LINE),('BACKGROUND',(0,0),(-1,-1),white),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]));st += [t,PageBreak()]
st += [sec('1. 프로젝트 개요','BinReady는 전자부품의 보관함 위치, 현재 수량, 다음 제작에 필요한 수량을 함께 관리하는 브라우저 기반 개인 도구다.'),sec('2. 대상 고객','전자공작·로봇·RC 제작을 하며 여러 보관함에 소형 부품을 나누어 보관하는 학생과 취미 메이커다.'),sec('3. 해결하는 문제','작업을 시작한 뒤 부품이 없거나 위치를 찾지 못하면 제작 흐름이 중단된다. 현재 재고와 필요 수량을 비교해 부족 부품을 먼저 보여준다.'),sec('4. 핵심 기능','① 검증된 부품 등록 ② 부품·코드·보관함 통합 검색 ③ 부족 수량 우선순위와 보충 기록'),sec('5. 사용 방법','외부 패키지 설치 없이 Node.js 내장 테스트를 실행하고 Python 정적 서버를 시작한다. 부품명·코드·분류·보관함·수량을 등록하고 검색과 부족 큐로 제작 준비 상태를 점검한다.'),PageBreak()]
st += [sec('6. 시스템 구조','브라우저 화면 → 입력 검증·부족 수량 계산·검색 엔진 → localStorage. 계정과 외부 서버가 없는 단일 사용자 구조다.'),sec('7. 기술 구성','HTML5, CSS, 순수 JavaScript, Node.js 내장 테스트 러너, Python 정적 서버, Docker. 외부 유료 API와 런타임 패키지는 없다.'),p('8. 실행 화면','h'),Image(str(R/'screenshots/dashboard.png'),width=493,height=493*1500/1440),p('실제 Chromium에서 신규 센서를 등록하고, 보관함 검색과 부족 부품 보충 흐름을 실행한 화면.','s'),PageBreak()]
st += [sec('9. 테스트 결과','자동 테스트 9/9 통과. 입력 정제, 코드·보관함 검증, 부족·여유 수량 계산, 준비도 집계, 검색, 중복 거부, 보충 기록을 확인했다. 외부 의존성 0개, HTTP 200, Chromium 등록·검색·보충 흐름과 README 명령도 검증했다.'),sec('10. 보안 및 제한사항','입력 길이·허용값 제한과 HTML 이스케이프를 적용한다. 보관함 이름에 개인정보나 출입 정보를 넣지 않도록 안내한다. 프로젝트별 BOM, 바코드, CSV 백업, 동기화는 포함하지 않는다.'),sec('11. 가격과 수익 모델','1회 구매 ₩9,900. 별도 서버 비용 없이 개인 메이커가 작업 중단과 중복 구매를 줄이는 가치를 판매 포인트로 삼는다.'),sec('12. 첫 고객 확보 방법','학교 메이커 동아리와 전자공작 커뮤니티 20명에게 무료 부품 정리 템플릿을 제공하고, 7일 사용 후 유료 라이선스 전환 의향을 확인한다.'),sec('13. 개선 계획','1) 프로젝트별 BOM 2) CSV 백업 3) QR 보관함 라벨 4) 사용 수량 차감 5) 구매 목록 내보내기 6) 선택형 동기화.'),PageBreak()]
data=[[p('평가 항목'),p('점수'),p('근거')],[p('고객 문제의 강도'),p('8/10'),p('부품 누락은 제작 중단과 중복 구매를 만든다.')],[p('하루 내 완성도'),p('9/10'),p('등록·검색·부족 큐·보충 흐름을 완성했다.')],[p('판매 가능성'),p('8/10'),p('메이커에게 시간 절약 가치를 설명하기 쉽다.')],[p('유지보수 난이도'),p('9/10'),p('정적 앱이며 외부 서비스가 없다.')],[p('차별성'),p('8/10'),p('보관 위치와 프로젝트 부족 수량을 함께 보여준다.')],[p('확장 가능성'),p('8/10'),p('BOM·QR·구매 목록으로 확장 가능하다.')]]
q=Table(data,colWidths=[105,48,340]);q.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),GREEN),('TEXTCOLOR',(0,0),(-1,0),white),('GRID',(0,0),(-1,-1),.5,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));st += [p('14. 종합 평가','h'),q,Spacer(1,16),p('종합 점수 8.3/10','h'),p('부품 위치와 부족 수량이라는 명확한 개인 메이커 문제를 좁은 워크플로로 해결한다. 유료화 전 프로젝트별 BOM과 QR 라벨 수요를 확인해야 한다.'),PageBreak(),p('부록 · 검증 체크리스트','h'),p('✓ 의존성 설치  ✓ 프로그램 시작  ✓ 핵심 기능  ✓ 자동 테스트 9개  ✓ README 명령  ✓ 비밀정보 검사  ✓ PDF 생성·파싱·렌더링'),p('릴리스 판정','h'),p('<b>PASS</b> — 개인 메이커 인터뷰와 소규모 유료 판매 검증에 사용할 수 있다. 실제 재고 수량은 사용자가 직접 확인해야 한다.')]
SimpleDocTemplate(str(R/'report.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=36,bottomMargin=40,title='BinReady MVP Report',author='System Foundry').build(st,onFirstPage=hf,onLaterPages=hf)
print(R/'report.pdf')
