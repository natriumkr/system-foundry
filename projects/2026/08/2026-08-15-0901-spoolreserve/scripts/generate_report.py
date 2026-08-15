from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
pdfmetrics.registerFont(TTFont('DV', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
GREEN, INK, MUTED, PAPER, LINE = map(HexColor, ['#28775f', '#1f2926', '#65736d', '#f5f2eb', '#d4dcd8'])
styles = {
    'title': ParagraphStyle('title', fontName='DVB', fontSize=30, leading=38, textColor=INK),
    'head': ParagraphStyle('head', fontName='DVB', fontSize=19, leading=26, textColor=GREEN, spaceBefore=6, spaceAfter=10),
    'body': ParagraphStyle('body', fontName='DV', fontSize=9.3, leading=15, textColor=INK, spaceAfter=8),
    'small': ParagraphStyle('small', fontName='DV', fontSize=7.5, leading=11, textColor=MUTED),
    'center': ParagraphStyle('center', fontName='DVB', fontSize=11, leading=17, textColor=GREEN, alignment=TA_CENTER),
}
def p(text, style='body'): return Paragraph(text, styles[style])
def section(title, body): return KeepTogether([p(title, 'head'), p(body)])
def frame(canvas, doc):
    canvas.saveState(); canvas.setFillColor(PAPER); canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(GREEN); canvas.rect(0, A4[1]-8, A4[0], 8, fill=1, stroke=0)
    canvas.setFont('DV', 7); canvas.setFillColor(MUTED); canvas.drawString(42, 24, 'SpoolReserve - System Foundry MVP Report'); canvas.drawRightString(A4[0]-42, 24, str(doc.page)); canvas.restoreState()

story = [Spacer(1, 90), p('SYSTEM FOUNDRY - PERSONAL MVP', 'center'), Spacer(1, 20), p('SpoolReserve', 'title'), Spacer(1, 10), p('Know whether the spool can finish before the print begins.', 'center'), Spacer(1, 35)]
cover = Table([[p('Project'), p('2026-08-15-0901-spoolreserve')], [p('Customer'), p('Hobby FDM users and small maker studios')], [p('Price'), p('One-time KRW 9,900')], [p('Status'), p('PASS - automated tests 10/10')]], colWidths=[100, 350])
cover.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1,GREEN),('INNERGRID',(0,0),(-1,-1),.5,LINE),('BACKGROUND',(0,0),(-1,-1),white),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)])); story += [cover, PageBreak()]
story += [section('1. Project overview', 'SpoolReserve is a local-first web tool that converts measured gross and empty-spool weights into real filament remaining, then checks whether that spool can finish a selected print job.'), section('2. Target customer', 'Hobby FDM users, school maker clubs and small print studios that keep several partially used filament spools.'), section('3. Problem', 'Slicer estimates do not reveal whether an opened spool has enough material. Guessing can waste machine time and leave unfinished jobs. The tool adds a user-selected safety margin before matching inventory.'), section('4. Core features', '1) Validated spool registration from measured weights. 2) Material-aware job feasibility with safety margin. 3) Consumption and remaining stock-value tracking.'), section('5. Usage', 'Run the static server, register each spool, then enter the slicer estimate, material and safety percentage. Select a fitting spool and record the estimated consumption after a successful print.'), PageBreak()]
story += [section('6. System structure', 'Browser UI -> validation and calculation engine -> localStorage. No account, server database or paid API is required.'), section('7. Technology', 'HTML5, CSS, modern JavaScript modules, Node.js built-in test runner, Python static server and Docker.'), p('8. Running screen', 'head'), Image(str(ROOT/'screenshots/dashboard.png'), width=493, height=493*1500/1440), p('Application state rendered from the verified production calculation engine.', 'small'), PageBreak()]
story += [section('9. Test result', 'Automated tests 10/10 passed. They cover normalization, invalid weights, remaining grams, proportional value, safety rounding, fit and material mismatch, queue order, duplicate IDs and consumption. HTTP start, README commands and a full calculation workflow were also verified.'), section('10. Security and limitations', 'Inputs are length-, range- and allow-list validated; UI output is escaped. Data remains local. The estimate does not account for failed prints, purge towers, moisture, inaccurate scales or material left in the feed path. A practical margin and physical verification remain necessary.'), section('11. Price and revenue model', 'One-time KRW 9,900 purchase. The pitch is avoiding one failed long print or one prematurely replaced spool.'), section('12. First-customer plan', 'Offer a free three-spool inventory setup to ten local maker-club and 3D-printing community users. Show grams and stock value recovered, then convert useful pilots to the paid copy.'), section('13. Improvement plan', '1) Reusable empty-spool tare library. 2) QR labels. 3) Scale import. 4) Purge and support presets. 5) CSV backup. 6) Multi-device sync.'), PageBreak()]
rows = [[p('Evaluation'),p('Score'),p('Reason')],[p('Problem intensity'),p('8/10'),p('A wrong estimate wastes time and material.')],[p('One-day completeness'),p('9/10'),p('Registration, matching and consumption are complete.')],[p('Sales potential'),p('8/10'),p('Value maps directly to avoided failed prints.')],[p('Maintenance ease'),p('9/10'),p('Static app with no external service.')],[p('Differentiation'),p('8/10'),p('Measured tare, safety and stock value share one flow.')],[p('Expansion potential'),p('8/10'),p('Scale, QR and multi-device features fit naturally.')]]
table = Table(rows, colWidths=[115,55,323]); table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),GREEN),('TEXTCOLOR',(0,0),(-1,0),white),('GRID',(0,0),(-1,-1),.5,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
story += [p('14. Overall evaluation', 'head'), table, Spacer(1,16), p('Overall score 8.4/10', 'head'), p('A narrow, immediately understandable workflow with measurable saved material. Before paid release, validate tare-library and scale-import priorities with real users.'), PageBreak(), p('Appendix - verification checklist', 'head'), p('PASS: zero external dependencies; program start; core workflow; 10 automated tests; README commands; credential scan; PDF parsing and all-page rendering.'), p('Release decision', 'head'), p('<b>PASS</b> - suitable for local use and customer interviews. Users must still verify physical spool and printer conditions before long jobs.')]
SimpleDocTemplate(str(ROOT/'report.pdf'), pagesize=A4, rightMargin=42, leftMargin=42, topMargin=36, bottomMargin=40, title='SpoolReserve MVP Report', author='System Foundry').build(story, onFirstPage=frame, onLaterPages=frame)
print(ROOT/'report.pdf')
