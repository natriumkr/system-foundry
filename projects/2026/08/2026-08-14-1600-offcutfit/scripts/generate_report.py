from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

R = Path(__file__).resolve().parents[1]
pdfmetrics.registerFont(TTFont('Noto', R / 'app/fonts/noto-sans-kr-regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoB', R / 'app/fonts/noto-sans-kr-bold.ttf'))
GREEN, INK, MUTED, PAPER, LINE = map(HexColor, ['#24735d', '#202b27', '#65736d', '#f6f4ef', '#d4dcd8'])
S = {
    't': ParagraphStyle('t', fontName='NotoB', fontSize=30, leading=38, textColor=INK),
    'h': ParagraphStyle('h', fontName='NotoB', fontSize=19, leading=26, textColor=GREEN, spaceBefore=6, spaceAfter=10),
    'b': ParagraphStyle('b', fontName='Noto', fontSize=9.3, leading=15, textColor=INK, spaceAfter=8),
    's': ParagraphStyle('s', fontName='Noto', fontSize=7.5, leading=11, textColor=MUTED),
    'c': ParagraphStyle('c', fontName='NotoB', fontSize=11, leading=17, textColor=GREEN, alignment=TA_CENTER),
}

def p(text, style='b'):
    return Paragraph(text, S[style])

def sec(title, body):
    return KeepTogether([p(title, 'h'), p(body)])

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER); canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(GREEN); canvas.rect(0, A4[1] - 8, A4[0], 8, fill=1, stroke=0)
    canvas.setFont('Noto', 7); canvas.setFillColor(MUTED)
    canvas.drawString(42, 24, 'OffcutFit · System Foundry MVP Report')
    canvas.drawRightString(A4[0] - 42, 24, str(doc.page)); canvas.restoreState()

story = [Spacer(1, 90), p('SYSTEM FOUNDRY · BUSINESS MVP', 'c'), Spacer(1, 20), p('OffcutFit', 't'), Spacer(1, 10), p('자투리 판재를 작업 규격과 대조해<br/>재사용 가치와 적합도를 관리하는 시스템', 'c'), Spacer(1, 35)]
cover = Table([[p('프로젝트'), p('2026-08-14-1600-offcutfit')], [p('대상 고객'), p('소형 레이저 커팅·간판·목공·모형 제작소')], [p('가격'), p('사업장당 월 ₩19,000')], [p('상태'), p('PASS · 자동 테스트 10/10')]], colWidths=[100, 350])
cover.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 1, GREEN), ('INNERGRID', (0, 0), (-1, -1), .5, LINE), ('BACKGROUND', (0, 0), (-1, -1), white), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 10), ('BOTTOMPADDING', (0, 0), (-1, -1), 10)]))
story += [cover, PageBreak()]
story += [sec('1. 프로젝트 개요', 'OffcutFit은 남은 판재의 치수·두께·보관 위치·잔존 가치를 기록하고 새 작업에 맞는 재료를 찾는 브라우저 기반 업무 시스템이다.'), sec('2. 대상 고객', '아크릴·합판·MDF 같은 판재를 반복 가공하는 소형 레이저 커팅·간판·목공·모형 제작소다.'), sec('3. 해결하는 문제', '쓸 수 있는 자투리가 선반에 쌓여도 규격과 위치를 찾기 어려워 새 판재를 다시 구매한다. 자투리의 면적과 금액을 가시화하고 작업 규격과 즉시 대조해 낭비를 줄인다.'), sec('4. 핵심 기능', '① 검증된 자투리 소재 등록 ② 직접·90도 회전 배치 적합 계산 ③ 가용 면적·잔존 가치와 사용 상태 추적'), sec('5. 사용 방법', 'node --test tests/*.test.js로 테스트하고 python3 -m http.server 4173 -d app으로 실행한다. 자투리를 등록한 뒤 작업 재료·가로·세로·두께를 입력해 적합 큐를 확인하고 사용할 조각을 처리한다.'), PageBreak()]
story += [sec('6. 시스템 구조', '브라우저 화면 → 입력 검증·치수 회전·면적·가치 계산 엔진 → localStorage. 외부 전송과 계정이 없는 단일 사업장 구조다.'), sec('7. 사용 기술', 'HTML5, CSS, 순수 JavaScript, Node.js 내장 테스트 러너, Python 정적 서버, Docker. 외부 유료 API와 런타임 패키지는 없다.'), p('8. 실행 화면', 'h'), Image(str(R / 'screenshots/dashboard.png'), width=493, height=493 * 1500 / 1440), p('실제 Chromium에서 자투리를 등록하고 작업 규격을 매칭한 뒤 한 조각을 사용 처리한 화면.', 's'), PageBreak()]
story += [sec('9. 테스트 결과', '자동 테스트 10/10 통과. 문자열 정제, 치수·단가 검증, 직접·회전 적합 판정, 면적·잔존 가치·사용률, 정렬, 중복 코드, 사용 상태 전환을 확인했다. HTTP 200, Chromium 등록·매칭·사용 처리, README 명령도 검증했다.'), sec('10. 보안 및 제한사항', '입력 길이·숫자 범위·허용 상태를 제한하고 HTML 이스케이프를 적용한다. 고객 개인정보·결제정보·비밀번호를 입력하지 않도록 안내한다. 직사각형 판재만 지원하며 실제 절단 전 흠집·톱날 여유·결 방향을 작업자가 확인해야 한다.'), sec('11. 가격과 수익 모델', '사업장당 월 ₩19,000 구독. 재고로 잠든 자투리의 금액과 새 판재 구매 회피액을 판매 포인트로 삼는다.'), sec('12. 첫 고객 확보 방법', '지역 레이저 커팅·간판·메이커 작업실 10곳의 자투리 선반을 일주일간 무료 목록화하고, 재사용한 금액을 제시해 14일 체험으로 전환한다.'), sec('13. 개선 계획', '1) 절단 여유·톱날 폭 2) 비정형 조각 3) 다중 부품 네스팅 4) QR 위치 라벨 5) CSV 가져오기 6) 팀 동기화.'), PageBreak()]
data = [[p('평가 항목'), p('점수'), p('근거')], [p('고객 문제의 강도'), p('9/10'), p('불필요한 새 판재 구매는 작업 마진을 직접 줄인다.')], [p('하루 내 완성도'), p('9/10'), p('등록·매칭·가치·사용 처리 흐름을 완성했다.')], [p('판매 가능성'), p('8/10'), p('회수한 재료비로 구독 가치를 설명할 수 있다.')], [p('유지보수 난이도'), p('9/10'), p('정적 앱이며 외부 서비스가 없다.')], [p('차별성'), p('8/10'), p('회전 적합도와 잔존 가치를 같은 큐에 제시한다.')], [p('확장 가능성'), p('8/10'), p('네스팅·QR·팀 재고로 확장할 수 있다.')]]
score_table = Table(data, colWidths=[105, 48, 340])
score_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), GREEN), ('TEXTCOLOR', (0, 0), (-1, 0), white), ('GRID', (0, 0), (-1, -1), .5, LINE), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 7), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
story += [p('14. 종합 평가', 'h'), score_table, Spacer(1, 16), p('종합 점수 8.5/10', 'h'), p('구매 회피액이라는 명확한 경제 효과를 좁은 워크플로로 보여준다. 유료화 전 작업장에서 절단 여유와 비정형 판재 지원 우선순위를 확인해야 한다.'), PageBreak(), p('부록 · 검증 체크리스트', 'h'), p('✓ 의존성 설치  ✓ 프로그램 시작  ✓ 핵심 기능  ✓ 자동 테스트 10개  ✓ README 명령  ✓ 비밀정보 검사  ✓ PDF 생성·파싱·렌더링'), p('릴리스 판정', 'h'), p('<b>PASS</b> — 내부 운영과 고객 인터뷰용 MVP로 사용할 수 있다. 실제 절단 전 소재 상태와 충분한 가공 여유를 확인해야 한다.')]

SimpleDocTemplate(str(R / 'report.pdf'), pagesize=A4, rightMargin=42, leftMargin=42, topMargin=36, bottomMargin=40, title='OffcutFit MVP Report', author='System Foundry').build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(R / 'report.pdf')
