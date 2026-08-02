from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "report.pdf"
SCREENSHOT = ROOT / "screenshots" / "dashboard.png"

NAVY = colors.HexColor("#16213D")
LIME = colors.HexColor("#C9F36A")
CORAL = colors.HexColor("#FF6B57")
PAPER = colors.HexColor("#F4F3EE")
MUTED = colors.HexColor("#6F7890")
LINE = colors.HexColor("#E3E4E0")

pdfmetrics.registerFont(TTFont("Body", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("BodyBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

styles = getSampleStyleSheet()
TITLE = ParagraphStyle("Title", fontName="BodyBold", fontSize=31, leading=35, textColor=NAVY, spaceAfter=8)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Body", fontSize=11, leading=17, textColor=MUTED)
EYEBROW = ParagraphStyle("Eyebrow", fontName="BodyBold", fontSize=8, leading=10, textColor=colors.HexColor("#667442"), spaceAfter=6)
H1 = ParagraphStyle("H1", fontName="BodyBold", fontSize=18, leading=22, textColor=NAVY, spaceBefore=4, spaceAfter=8)
H2 = ParagraphStyle("H2", fontName="BodyBold", fontSize=12, leading=15, textColor=NAVY, spaceBefore=5, spaceAfter=4)
BODY = ParagraphStyle("Body", fontName="Body", fontSize=9.3, leading=14, textColor=colors.HexColor("#30384C"), spaceAfter=7)
SMALL = ParagraphStyle("Small", fontName="Body", fontSize=7.8, leading=11, textColor=MUTED)
WHITE = ParagraphStyle("White", fontName="BodyBold", fontSize=10, leading=14, textColor=colors.white)
SCORE = ParagraphStyle("Score", fontName="BodyBold", fontSize=25, leading=28, textColor=NAVY, alignment=TA_LEFT)


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 12 * mm, width, 12 * mm, stroke=0, fill=1)
    canvas.setFont("BodyBold", 8)
    canvas.setFillColor(LIME)
    canvas.drawString(18 * mm, height - 7.6 * mm, "CLAIMCLOCK / SYSTEM FOUNDRY")
    canvas.setFillColor(MUTED)
    canvas.setFont("Body", 7)
    canvas.drawString(18 * mm, 10 * mm, "2026-08-02 / MVP REPORT / CONFIDENTIAL REVIEW COPY")
    canvas.drawRightString(width - 18 * mm, 10 * mm, f"{doc.page}")
    canvas.restoreState()


def section(number, title, text):
    return [Paragraph(f"{number:02d} / {title.upper()}", EYEBROW), Paragraph(title, H1), Paragraph(text, BODY)]


def bullet(text):
    return Paragraph(f"<font color='#7A9132'>●</font> {text}", BODY)


def card(title, value, note, color=NAVY):
    data = [[Paragraph(title.upper(), SMALL)], [Paragraph(value, SCORE)], [Paragraph(note, SMALL)]]
    table = Table(data, colWidths=[50 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.8, LINE),
        ("LINEABOVE", (0, 0), (-1, 0), 4, color),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


story = []
story += [Spacer(1, 10 * mm), Paragraph("SYSTEM FOUNDRY / BUSINESS MVP", EYEBROW),
          Paragraph("ClaimClock", TITLE),
          Paragraph("A deadline-first operations desk for returns, exchanges, and refunds.", SUBTITLE),
          Spacer(1, 13 * mm)]
story.append(Table([[card("Product status", "PASS", "Implemented and verified", LIME),
                     card("Automated tests", "8 / 8", "Zero failures", CORAL),
                     card("Monthly price", "KRW 19K", "One self-hosted store", NAVY)]],
                   colWidths=[55 * mm] * 3, hAlign="LEFT"))
story += [Spacer(1, 14 * mm)]
story += section(1, "Project overview",
    "ClaimClock is a local-first operations system that turns scattered return, exchange, and refund requests into a prioritized work queue. It was built as a single-admin MVP with no paid API dependency.")
story += section(2, "Target customer",
    "Small Korean online merchants processing five or more customer claims per day, especially Smart Store and direct-to-consumer operators still coordinating work through chat messages and spreadsheets.")
story += section(3, "Problem",
    "Claim details arrive through several channels. A spreadsheet records the case but rarely surfaces urgency, so due dates slip, customer trust declines, and the owner cannot see how much money remains exposed.")
story.append(PageBreak())

story += [Paragraph("PRODUCT", EYEBROW), Paragraph("A narrow workflow with three jobs", TITLE)]
story += section(4, "Core features", "The MVP deliberately limits scope to the following operational loop:")
features = [
    ["01", Paragraph("<b>Validated claim intake</b><br/>Order reference, case type, amount, deadline, alias, and note with server-side limits.", BODY)],
    ["02", Paragraph("<b>Deadline risk dashboard</b><br/>Overdue, urgent (48 hours), watch, safe, and completed classifications calculated from the current date.", BODY)],
    ["03", Paragraph("<b>Status and exposure tracking</b><br/>Open, waiting, and resolved transitions with active-case count and financial exposure total.", BODY)],
]
feature_table = Table(features, colWidths=[14 * mm, 150 * mm])
feature_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), NAVY), ("TEXTCOLOR", (0, 0), (0, -1), LIME),
    ("FONTNAME", (0, 0), (0, -1), "BodyBold"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BOX", (0, 0), (-1, -1), 0.7, LINE),
    ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE), ("TOPPADDING", (0, 0), (-1, -1), 9),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 9), ("LEFTPADDING", (1, 0), (1, -1), 12),
]))
story += [feature_table, Spacer(1, 7 * mm)]
story += section(5, "How to use",
    "Set two required environment variables, start the Python server, sign in with the configured access code, register a case, and work from the highest-risk row. Change the status to waiting or resolved as processing advances.")
story += section(6, "System architecture", "The server is intentionally compact and auditable:")
architecture = Table([
    ["Browser", "HTTP handler", "Domain rules", "SQLite"],
    ["Server-rendered UI", "Session + CSRF", "Validation + risk", "Parameterized SQL"],
], colWidths=[41 * mm] * 4)
architecture.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "BodyBold"), ("FONTNAME", (0, 1), (-1, 1), "Body"),
    ("FONTSIZE", (0, 0), (-1, -1), 8), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.6, LINE), ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story += [architecture, Spacer(1, 5 * mm)]
story += section(7, "Technology", "Python 3 standard library, SQLite, server-rendered HTML/CSS, and unittest. Runtime dependencies: zero. External paid APIs: zero.")
story.append(PageBreak())

story += [Paragraph("VALIDATED INTERFACE", EYEBROW), Paragraph("Actual running screen", TITLE),
          Paragraph("Captured from headless Chromium after login and four real form submissions against a temporary SQLite database.", SUBTITLE), Spacer(1, 6 * mm)]
img = Image(str(SCREENSHOT), width=145 * mm, height=132 * mm)
story += [img, Spacer(1, 5 * mm)]
story += section(8, "Running screen",
    "The captured dashboard shows four active cases, two due within 48 hours, and KRW 271,800 in open exposure. Korean typography is bundled locally, so the interface does not depend on a third-party font CDN.")
story.append(PageBreak())

story += [Paragraph("VERIFICATION", EYEBROW), Paragraph("Evidence, not assumptions", TITLE)]
story += section(9, "Test results", "Every required check was executed against the generated project.")
checks = [
    ["Check", "Result", "Evidence"],
    ["Dependency installation", "PASS", "Fresh venv + empty runtime requirements"],
    ["Application start", "PASS", "GET /health returned HTTP 200"],
    ["Core workflow", "PASS", "Login + four creates + dashboard totals"],
    ["Automated tests", "8 / 8", "Validation, risk, database, status, duplicates"],
    ["README commands", "PASS", "Install, test, and start commands executed"],
    ["Credential scan", "PASS", "No secret patterns or .env file"],
    ["PDF", "PASS", "Generated, parsed, rendered, visually inspected"],
]
test_table = Table(checks, colWidths=[48 * mm, 23 * mm, 94 * mm], repeatRows=1)
test_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "BodyBold"), ("FONTNAME", (0, 1), (-1, -1), "Body"),
    ("FONTNAME", (1, 1), (1, -1), "BodyBold"), ("TEXTCOLOR", (1, 1), (1, -1), colors.HexColor("#557526")),
    ("FONTSIZE", (0, 0), (-1, -1), 7.6), ("GRID", (0, 0), (-1, -1), 0.5, LINE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story += [test_table, Spacer(1, 8 * mm)]
story += section(10, "Security and limitations",
    "No embedded credentials or default admin account. Access key and HMAC session secret are required environment variables. Mutations require an authenticated HttpOnly SameSite cookie and CSRF token. Inputs are length-, type-, amount-, and date-validated; SQL uses parameter binding. The default bind address is localhost. Limitations: single administrator, no TLS termination, no team permissions, no attachment malware scanning, and no marketplace synchronization.")
story.append(PageBreak())

story += [Paragraph("GO TO MARKET", EYEBROW), Paragraph("A sellable wedge", TITLE)]
story += section(11, "Pricing and revenue model",
    "KRW 19,000 per month for one self-hosted store, including updates and email support. A later hosted tier can charge KRW 39,000 per month for automated backups and team access. Ten pilot stores at the base tier produce KRW 190,000 MRR before hosting costs.")
story += section(12, "First customer acquisition",
    "Recruit five operators from Korean Smart Store seller communities. Offer a 14-day pilot in exchange for a 20-minute workflow interview and permission to measure missed-deadline rate. Demonstrate the product with the seller's anonymized last ten claim cases. Convert with a simple promise: one board, every due date visible.")
story += section(13, "Improvement plan", "Prioritized follow-up work after real usage:")
for text in [
    "CSV import/export and daily encrypted backup.",
    "Team accounts with role-based permissions and an audit timeline.",
    "Email or messenger reminders without exposing customer information.",
    "Optional marketplace connectors after validating demand and terms.",
]:
    story.append(bullet(text))
story.append(Spacer(1, 5 * mm))
story += [Paragraph("COMMERCIAL ASSUMPTION", H2), Paragraph(
    "The strongest initial sales angle is operational risk reduction, not generic CRM. ClaimClock should stay specialized until interviews show that merchants will pay for broader support tooling.", BODY)]
story.append(PageBreak())

story += [Paragraph("ASSESSMENT", EYEBROW), Paragraph("Overall evaluation", TITLE)]
story += section(14, "Overall score", "Six dimensions are scored out of 10. Higher maintenance score means easier maintenance.")
ratings = [
    ("Customer problem strength", 8, "Missed claim deadlines create direct refund cost and trust damage."),
    ("One-day completeness", 9, "The full intake-to-resolution loop is implemented and browser-tested."),
    ("Sales potential", 7, "Clear niche and price, but interviews must confirm willingness to switch."),
    ("Maintenance difficulty", 8, "Zero runtime dependencies and a compact SQLite design reduce upkeep."),
    ("Differentiation", 7, "Deadline-first positioning is sharper than spreadsheets, though replicable."),
    ("Scalability", 8, "Team roles, reminders, and connectors create credible expansion paths."),
]
rating_rows = [["Dimension", "Score", "Rationale"]] + [[name, f"{score}/10", reason] for name, score, reason in ratings]
rating_table = Table(rating_rows, colWidths=[52 * mm, 20 * mm, 93 * mm])
rating_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "BodyBold"), ("FONTNAME", (0, 1), (-1, -1), "Body"),
    ("FONTNAME", (1, 1), (1, -1), "BodyBold"), ("BACKGROUND", (1, 1), (1, -1), colors.HexColor("#EFF7DA")),
    ("GRID", (0, 0), (-1, -1), 0.5, LINE), ("FONTSIZE", (0, 0), (-1, -1), 7.4),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story += [rating_table, Spacer(1, 11 * mm)]
overall = Table([[Paragraph("OVERALL", WHITE), Paragraph("7.8 / 10", ParagraphStyle("Big", parent=SCORE, textColor=LIME)),
                  Paragraph("Proceed to five-customer pilot. Keep scope focused on deadline visibility.", WHITE)]],
                colWidths=[28 * mm, 42 * mm, 95 * mm])
overall.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), NAVY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 14), ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
]))
story += [overall, Spacer(1, 10 * mm), Paragraph(
    "Verdict: ClaimClock is technically complete as an MVP and commercially specific enough for pilot sales. The next evidence should come from merchant interviews, not additional features.", BODY)]

doc = SimpleDocTemplate(
    str(OUTPUT), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm,
    topMargin=20 * mm, bottomMargin=18 * mm, title="ClaimClock MVP Report",
    author="System Foundry", subject="Business MVP implementation and validation report",
)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"Generated {OUTPUT}")
