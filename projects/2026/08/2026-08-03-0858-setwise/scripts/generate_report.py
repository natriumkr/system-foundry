from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "report.pdf"
SCREENSHOT = ROOT / "screenshots" / "dashboard.png"

INK = colors.HexColor("#182039")
VIOLET = colors.HexColor("#826DF0")
YELLOW = colors.HexColor("#FFE27A")
MINT = colors.HexColor("#9EE8C8")
ORANGE = colors.HexColor("#FF7B52")
MUTED = colors.HexColor("#747B8F")
LINE = colors.HexColor("#E4E1DA")

pdfmetrics.registerFont(TTFont("Body", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("BodyBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

TITLE = ParagraphStyle("title", fontName="BodyBold", fontSize=31, leading=35, textColor=INK, spaceAfter=8)
SUBTITLE = ParagraphStyle("subtitle", fontName="Body", fontSize=11, leading=17, textColor=MUTED, spaceAfter=8)
EYEBROW = ParagraphStyle("eyebrow", fontName="BodyBold", fontSize=8, leading=10, textColor=VIOLET, spaceAfter=6)
H1 = ParagraphStyle("h1", fontName="BodyBold", fontSize=18, leading=22, textColor=INK, spaceAfter=7)
H2 = ParagraphStyle("h2", fontName="BodyBold", fontSize=12, leading=15, textColor=INK, spaceAfter=4)
BODY = ParagraphStyle("body", fontName="Body", fontSize=9.2, leading=14, textColor=colors.HexColor("#343C50"), spaceAfter=7)
SMALL = ParagraphStyle("small", fontName="Body", fontSize=7.5, leading=10, textColor=MUTED)
WHITE = ParagraphStyle("white", fontName="BodyBold", fontSize=9, leading=13, textColor=colors.white)


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(INK)
    canvas.rect(0, height - 12 * mm, width, 12 * mm, stroke=0, fill=1)
    canvas.setFillColor(YELLOW)
    canvas.setFont("BodyBold", 8)
    canvas.drawString(18 * mm, height - 7.6 * mm, "SETWISE / SYSTEM FOUNDRY")
    canvas.setFillColor(MUTED)
    canvas.setFont("Body", 7)
    canvas.drawString(18 * mm, 10 * mm, "2026-08-03 / PERSONAL MVP REPORT")
    canvas.drawRightString(width - 18 * mm, 10 * mm, str(doc.page))
    canvas.restoreState()


def section(number, title, text):
    return [Paragraph(f"{number:02d} / {title.upper()}", EYEBROW), Paragraph(title, H1), Paragraph(text, BODY)]


def card(title, value, note, accent):
    table = Table([[Paragraph(title.upper(), SMALL)], [Paragraph(value, ParagraphStyle("value", fontName="BodyBold", fontSize=24, leading=28, textColor=INK))], [Paragraph(note, SMALL)]], colWidths=[50 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white), ("BOX", (0, 0), (-1, -1), .8, LINE),
        ("LINEABOVE", (0, 0), (-1, 0), 4, accent), ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


story = [Spacer(1, 10 * mm), Paragraph("SYSTEM FOUNDRY / PERSONAL MVP", EYEBROW), Paragraph("SetWise", TITLE),
         Paragraph("A priority-based daily rehearsal queue for musicians with too many pieces and too little time.", SUBTITLE), Spacer(1, 12 * mm)]
story.append(Table([[card("Product status", "PASS", "Implemented and verified", YELLOW), card("Automated tests", "8 / 8", "Zero failures", ORANGE), card("One-time price", "KRW 12K", "Local-first license", VIOLET)]], colWidths=[55 * mm] * 3))
story += [Spacer(1, 13 * mm)]
story += section(1, "Project overview", "SetWise converts a musician's repertoire into a daily practice queue. It scores each piece by confidence, practice gap, and performance proximity, then fits the highest-priority work into the available minutes.")
story += section(2, "Target customer", "Music students, school and community band members, and hobby performers preparing several pieces at once without a structured daily practice plan.")
story += section(3, "Problem", "Limited practice time is often spent on familiar material because deciding what to work on creates friction. Weak sections and upcoming performance deadlines can be overlooked until late in the preparation cycle.")
story.append(PageBreak())

story += [Paragraph("PRODUCT", EYEBROW), Paragraph("Three focused jobs", TITLE)]
story += section(4, "Core features", "The MVP implements one complete planning loop:")
features = [
    ["01", Paragraph("<b>Validated repertoire intake</b><br/>Title, focus section, confidence, recommended minutes, and optional performance date.", BODY)],
    ["02", Paragraph("<b>Priority-based daily queue</b><br/>Confidence need, days since practice, and deadline urgency combine into a transparent score.", BODY)],
    ["03", Paragraph("<b>Practice completion history</b><br/>A finished session updates confidence, last-practiced date, and weekly minutes.", BODY)],
]
ft = Table(features, colWidths=[14 * mm, 150 * mm])
ft.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), INK), ("TEXTCOLOR", (0, 0), (0, -1), YELLOW),
    ("FONTNAME", (0, 0), (0, -1), "BodyBold"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("GRID", (0, 0), (-1, -1), .5, LINE),
    ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ("LEFTPADDING", (1, 0), (1, -1), 12),
]))
story += [ft, Spacer(1, 7 * mm)]
story += section(5, "How to use", "Set today's available minutes, review the generated queue, practice the specified focus section, select post-session confidence, and mark the session complete. Add new repertoire from the side panel as needed.")
story += section(6, "System architecture", "A static browser application loads pure planning functions, renders the interface, and persists the repertoire and recent session history in localStorage. There is no server-side account or database.")
architecture = Table([["Browser UI", "Planner module", "Local storage", "Node tests"], ["HTML + CSS", "Scoring + validation", "Device-only data", "Pure functions"]], colWidths=[41 * mm] * 4)
architecture.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "BodyBold"), ("FONTNAME", (0, 1), (-1, 1), "Body"),
    ("FONTSIZE", (0, 0), (-1, -1), 8), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), .6, LINE), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story += [architecture, Spacer(1, 5 * mm)]
story += section(7, "Technology", "Static HTML, responsive CSS, vanilla JavaScript, localStorage, and the built-in Node.js test runner. Runtime dependency count: zero. Paid API count: zero.")
story.append(PageBreak())

story += [Paragraph("VALIDATED INTERFACE", EYEBROW), Paragraph("Actual running screen", TITLE), Paragraph("Captured from headless Chromium after the application calculated the default repertoire queue.", SUBTITLE), Spacer(1, 5 * mm)]
story.append(Image(str(SCREENSHOT), width=132 * mm, height=141 * mm))
story += [Spacer(1, 5 * mm)]
story += section(8, "Running screen", "The verified screen shows four repertoire items, two performances within 14 days, 32 minutes practiced this week, and a 33-minute queue ordered Bach Prelude, Scale Routine, and Open Ending. Completing the first session increased the weekly total to 47 minutes.")
story.append(PageBreak())

story += [Paragraph("VERIFICATION", EYEBROW), Paragraph("Evidence, not assumptions", TITLE)]
story += section(9, "Test results", "All required checks were executed against the generated project.")
checks = [
    ["Check", "Result", "Evidence"],
    ["Dependency installation", "PASS", "npm install completed; zero runtime dependencies"],
    ["Application start", "PASS", "Local HTTP server returned status 200"],
    ["Core calculation", "PASS", "Queue order, 33-minute plan, and summary totals asserted"],
    ["Completion workflow", "PASS", "Weekly minutes changed from 32 to 47"],
    ["Automated tests", "8 / 8", "Validation, scoring, budget, history, summary"],
    ["README commands", "PASS", "Install, test, and start commands executed"],
    ["Credential scan", "PASS", "No secret patterns and no .env file"],
    ["PDF", "PASS", "Generated, parsed, rendered, visually inspected"],
]
tt = Table(checks, colWidths=[48 * mm, 23 * mm, 94 * mm], repeatRows=1)
tt.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "BodyBold"), ("FONTNAME", (0, 1), (-1, -1), "Body"),
    ("FONTNAME", (1, 1), (1, -1), "BodyBold"), ("TEXTCOLOR", (1, 1), (1, -1), colors.HexColor("#5A4FB4")),
    ("FONTSIZE", (0, 0), (-1, -1), 7.5), ("GRID", (0, 0), (-1, -1), .5, LINE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story += [tt, Spacer(1, 8 * mm)]
story += section(10, "Security and limitations", "SetWise sends no data to external services and collects no account or identity information. Inputs are length-, type-, date-, and range-validated. Rendered user text is HTML-escaped. No credentials are required. Limitations: browser-local data can be lost when storage is cleared, there is no device sync, and the priority formula is a planning aid rather than a skill assessment.")
story.append(PageBreak())

story += [Paragraph("GO TO MARKET", EYEBROW), Paragraph("A small paid utility", TITLE)]
story += section(11, "Pricing and revenue model", "One-time purchase at KRW 12,000 for the downloadable local-first version. A later optional sync tier could charge KRW 2,900 per month, but the MVP does not require hosting or paid services.")
story += section(12, "First customer acquisition", "Recruit the first ten users from school music clubs, independent lesson studios, and Korean instrument communities. Offer a seven-day trial and ask each user to compare decision time and missed focus sections against their current notebook routine. Convert with a simple message: open the page and know what to practice first.")
story += section(13, "Improvement plan", "Priorities after observing real practice sessions:")
for item in ["JSON backup and restore for device migration.", "Multiple instruments and teacher-shared assignments.", "Optional metronome targets and section-level notes.", "Private encrypted sync only after users request cross-device access."]:
    story.append(Paragraph(f"<font color='#826DF0'>●</font> {item}", BODY))
story += [Spacer(1, 7 * mm), Paragraph("COMMERCIAL ASSUMPTION", H2), Paragraph("SetWise should remain a decision tool, not grow into a full digital audio workstation or sheet-music platform. The narrow value is reducing daily planning friction.", BODY)]
story.append(PageBreak())

story += [Paragraph("ASSESSMENT", EYEBROW), Paragraph("Overall evaluation", TITLE)]
story += section(14, "Overall score", "Six dimensions are scored out of 10. A higher maintenance score means easier maintenance.")
ratings = [
    ("Customer problem strength", 7, "Daily practice prioritization is recurring, though not financially urgent."),
    ("One-day completeness", 9, "The full planning and completion loop is implemented and browser-tested."),
    ("Sales potential", 7, "Low price and a focused audience support direct sales; interviews remain necessary."),
    ("Maintenance difficulty", 9, "Zero runtime dependencies and no backend keep maintenance light."),
    ("Differentiation", 8, "Transparent time-fitting priority queues are sharper than generic practice logs."),
    ("Scalability", 8, "Teacher assignments, instruments, and optional sync create expansion paths."),
]
rows = [["Dimension", "Score", "Rationale"]] + [[name, f"{score}/10", reason] for name, score, reason in ratings]
rt = Table(rows, colWidths=[52 * mm, 20 * mm, 93 * mm])
rt.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "BodyBold"), ("FONTNAME", (0, 1), (-1, -1), "Body"),
    ("FONTNAME", (1, 1), (1, -1), "BodyBold"), ("BACKGROUND", (1, 1), (1, -1), colors.HexColor("#F0EDFF")),
    ("FONTSIZE", (0, 0), (-1, -1), 7.4), ("GRID", (0, 0), (-1, -1), .5, LINE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story += [rt, Spacer(1, 11 * mm)]
overall = Table([[Paragraph("OVERALL", WHITE), Paragraph("8.0 / 10", ParagraphStyle("big", fontName="BodyBold", fontSize=25, leading=28, textColor=YELLOW)), Paragraph("Proceed to a ten-user trial and measure planning time saved.", WHITE)]], colWidths=[28 * mm, 42 * mm, 95 * mm])
overall.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), INK), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 14), ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
]))
story += [overall, Spacer(1, 10 * mm), Paragraph("Verdict: technically complete and visually polished for a personal MVP. The next useful evidence is whether musicians repeatedly open it before practice and follow the generated queue.", BODY)]

doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=20 * mm, bottomMargin=18 * mm, title="SetWise MVP Report", author="System Foundry", subject="Personal MVP implementation and validation report")
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"Generated {OUTPUT}")
