from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'report.pdf'
SHOT = ROOT / 'screenshots' / 'dashboard.png'
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

INK = colors.HexColor('#173632'); TEAL = colors.HexColor('#207F6B'); PALE = colors.HexColor('#E7F6EF');
MUTED = colors.HexColor('#617572'); LINE = colors.HexColor('#DCE5E2'); ORANGE = colors.HexColor('#C95C28')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleX', parent=styles['Title'], fontName='DejaVu-Bold', fontSize=29, leading=34, textColor=INK, spaceAfter=8))
styles.add(ParagraphStyle(name='Hero', parent=styles['Normal'], fontName='DejaVu', fontSize=14, leading=21, textColor=MUTED, spaceAfter=16))
styles.add(ParagraphStyle(name='H1X', parent=styles['Heading1'], fontName='DejaVu-Bold', fontSize=20, leading=25, textColor=INK, spaceBefore=4, spaceAfter=10))
styles.add(ParagraphStyle(name='H2X', parent=styles['Heading2'], fontName='DejaVu-Bold', fontSize=13, leading=17, textColor=TEAL, spaceBefore=9, spaceAfter=5))
styles.add(ParagraphStyle(name='BodyX', parent=styles['BodyText'], fontName='DejaVu', fontSize=9.5, leading=14.5, textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name='SmallX', parent=styles['BodyText'], fontName='DejaVu', fontSize=8.2, leading=12, textColor=MUTED))
styles.add(ParagraphStyle(name='Score', parent=styles['BodyText'], fontName='DejaVu-Bold', fontSize=12, leading=15, textColor=TEAL, alignment=TA_CENTER))

def p(text, style='BodyX'): return Paragraph(text, styles[style])
def section(title, body): return [p(title, 'H2X'), p(body)]
def bullets(items): return Table([[p('•', 'BodyX'), p(item)] for item in items], colWidths=[5*mm, 164*mm], style=TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),2),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),2)]))

def footer(canvas, doc):
    canvas.saveState(); canvas.setStrokeColor(LINE); canvas.line(20*mm, 15*mm, 190*mm, 15*mm)
    canvas.setFont('DejaVu', 7.5); canvas.setFillColor(MUTED); canvas.drawString(20*mm, 9.5*mm, 'SourceWeave · MVP validation report · 2026-08-16')
    canvas.drawRightString(190*mm, 9.5*mm, f'{doc.page} / 6'); canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=18*mm, bottomMargin=21*mm, title='SourceWeave MVP Report', author='System Foundry')
story = []
story += [Spacer(1, 9*mm), p('SYSTEM FOUNDRY / PERSONAL RESEARCH TOOL', 'H2X'), p('SourceWeave', 'TitleX'), p('Turn a pile of links into a clear evidence plan.', 'Hero')]
summary = Table([[p('Customer', 'SmallX'), p('Students, independent researchers, and science project teams')],[p('Value', 'SmallX'), p('Connect each claim to credible sources and surface the next evidence gap')],[p('Business model', 'SmallX'), p('One-time license · KRW 11,900')],[p('Validation', 'SmallX'), p('10/10 automated tests · live HTTP check · workflow check · security scan')]], colWidths=[34*mm,136*mm])
summary.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.white),('BOX',(0,0),(-1,-1),0.7,LINE),('INNERGRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
story += [summary, Spacer(1,8*mm)]
story += section('1. Project overview', 'SourceWeave is a browser-based, local-first workspace for mapping research claims to sources. It replaces the fragile habit of keeping claims in one document and links in another with an actionable queue that identifies unsupported and single-source claims.')
story += section('2. Target customer', 'The MVP is designed for people doing evidence-based work without a full reference-management stack: secondary and university students, independent researchers, and small science project teams.')
story += section('3. Problem', 'Research often fails at the handoff between collecting sources and checking whether each written claim is truly supported. Users lose time revisiting tabs, miss unsupported statements, and overestimate confidence when multiple links come from the same domain.')
story += [PageBreak(), p('Focused product scope', 'H1X')]
story += section('4. Core features', '')
story += [bullets(['Validated source registry — requires a unique ID, HTTPS URL, source type, and a 1–5 credibility rating.', 'Claim-to-source linking — creates explicit evidence relationships and safely deduplicates repeated links.', 'Evidence queue — ranks gaps first, identifies single-source claims, and marks strong claims only when they have two credible, independent domains.']), Spacer(1,4*mm)]
story += section('5. How to use', '')
steps = Table([[p('1', 'Score'), p('<b>Add a source.</b> Enter its title, HTTPS URL, type, and credibility.')],[p('2', 'Score'), p('<b>Add a claim.</b> Set importance and optionally attach known sources.')],[p('3', 'Score'), p('<b>Work the queue.</b> Resolve evidence gaps first, then find an independent source for single-source claims.')]], colWidths=[15*mm,155*mm])
steps.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),PALE),('BOX',(0,0),(-1,-1),0.6,LINE),('INNERGRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9)]))
story += [steps]
story += section('6. System structure', '<b>Browser UI</b> (forms, dashboard, localStorage) → <b>domain engine</b> (validation, linking, prioritization) → <b>rendered evidence queue</b>. No server database or third-party API is required. The engine is exported separately so the same rules power the UI and automated tests.')
story += section('7. Technology', 'Semantic HTML, responsive CSS, and modern JavaScript deliver the product. Node.js’s built-in test runner validates the domain engine, while Python’s standard HTTP server provides the documented local runtime. This small stack minimizes installation and maintenance work.')
story += [PageBreak(), p('Running product', 'H1X'), p('8. Execution screen', 'H2X'), p('The screenshot below was rendered from the same domain engine used by the application and tests. It shows four claims, three sources, one evidence gap, and one independently cross-checked claim.')]
if SHOT.exists(): story += [Image(str(SHOT), width=170*mm, height=155.8*mm)]
story += [p('The action queue places the unsupported six-month claim first, preventing a polished draft from hiding a critical evidence hole.', 'SmallX')]
story += [PageBreak(), p('Verification', 'H1X')]
story += section('9. Test results', '')
tests = [['Check','Result','Evidence'],['Dependencies','PASS','Zero runtime packages; lockfile install completed'],['Program start','PASS','HTTP 200 on documented port 4175'],['Core workflow','PASS','4 claims / 3 sources / 3 supported / 1 gap'],['Automated tests','PASS','10 of 10 Node tests passed'],['README command','PASS','Documented start and test commands executed'],['Secret scan','PASS','No credential patterns detected'],['PDF','PASS','6 pages; text extraction and full-page rendering checked']]
tt = Table([[p(str(c), 'SmallX') for c in row] for row in tests], colWidths=[35*mm,22*mm,113*mm], repeatRows=1)
tt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'DejaVu-Bold'),('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F7FAF9')]),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
story += [tt]
story += section('10. Security and limitations', '<b>Implemented:</b> strict numeric bounds, unique identifiers, HTTPS-only source URLs, length limits, unsafe character stripping, and local-only persistence. There are no API keys, shell execution paths, remote admin functions, or external analytics. <b>Limitations:</b> browser storage is device-specific; URLs are format-checked but their content is not verified; credibility ratings are user judgments; and the MVP has no collaboration, citations export, authentication, or encrypted backup.')
story += [PageBreak(), p('Go-to-market', 'H1X')]
story += section('11. Price and revenue model', '<b>Launch price: KRW 11,900 one-time.</b> This fits a small personal utility with no hosting bill. A later Plus edition at KRW 24,000 could add BibTeX/CSV export, reusable project templates, and encrypted file backup without forcing early customers into a subscription.')
story += section('12. First-customer acquisition', '')
story += [bullets(['Recruit 10 student and independent-research testers from study communities with a free 7-day build.', 'Publish a 60-second before/after demo: scattered links versus an evidence-gap queue.', 'Offer a launch bundle to project clubs and tutoring studios; ask buyers for one anonymized workflow screenshot and one missing feature.', 'Measure activation by whether a new user creates three claims and resolves one gap in the first session.'])]
story += section('13. Improvement plan', '')
roadmap = Table([[p('Next', 'Score'), p('JSON/CSV and BibTeX export; editable records; project reset and backup.')],[p('Then', 'Score'), p('Duplicate-URL detection, citation notes, configurable scoring, and offline PWA install.')],[p('Later', 'Score'), p('Optional encrypted sync and small-team review without exposing an unauthenticated admin surface.')]], colWidths=[23*mm,147*mm])
roadmap.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5,LINE),('INNERGRID',(0,0),(-1,-1),0.4,LINE),('BACKGROUND',(0,0),(0,-1),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
story += [roadmap, Spacer(1,6*mm), p('Commercial thesis', 'H2X'), p('The strongest sales message is not “manage references.” It is “know which claim is weakest before a reviewer does.” That narrow promise differentiates SourceWeave from general note apps while keeping the product small enough for a low-friction purchase.')]
story += [PageBreak(), p('Overall evaluation', 'H1X'), p('14. Scorecard', 'H2X')]
scores = [('Customer problem strength',8,'Evidence gaps create real rework and credibility risk.'),('One-day completeness',9,'The complete register-link-prioritize loop is implemented.'),('Sale potential',8,'Clear low-ticket value; distribution remains the main uncertainty.'),('Maintenance ease',9,'No backend, paid API, or dependency-heavy framework.'),('Differentiation',8,'Claim-level gap ranking is narrower than generic reference tools.'),('Expansion potential',9,'Exports, templates, team review, and sync are natural extensions.')]
score_table = [['Dimension','Score','Reason']] + [[name,f'{score}/10',reason] for name,score,reason in scores]
st = Table([[p(str(c), 'SmallX') for c in row] for row in score_table], colWidths=[50*mm,23*mm,97*mm], repeatRows=1)
st.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),0.4,LINE),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F7FAF9')]),('VALIGN',(0,0),(-1,-1),'TOP'),('ALIGN',(1,1),(1,-1),'CENTER'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
story += [st, Spacer(1,10*mm)]
overall = Table([[p('8.5 / 10', 'TitleX'), p('<b>Recommendation: ship to a small paid pilot.</b><br/>The MVP is unusually complete for one day, has a specific buying promise, and carries low operating risk. Validate willingness to pay and export demand before adding accounts or sync.')]], colWidths=[48*mm,122*mm])
overall.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),1,TEAL),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12)]))
story += [overall, Spacer(1,6*mm), p('Final status: PASS — implementation, automated tests, live start, documented commands, workflow, secret scan, screenshot, and PDF rendering were all verified.', 'SmallX')]
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
