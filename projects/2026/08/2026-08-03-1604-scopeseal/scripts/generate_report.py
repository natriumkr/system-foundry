from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "report.pdf"
SCREENSHOT = ROOT / "screenshots" / "dashboard.png"

INK = colors.HexColor("#141B31")
BLUE = colors.HexColor("#4B67FF")
MINT = colors.HexColor("#A9EBC4")
AMBER = colors.HexColor("#FFD36B")
RED = colors.HexColor("#FF766A")
MUTED = colors.HexColor("#6E7891")
LINE = colors.HexColor("#E5E2DB")

pdfmetrics.registerFont(TTFont("Body", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("BodyBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

TITLE = ParagraphStyle("title", fontName="BodyBold", fontSize=31, leading=35, textColor=INK, spaceAfter=8)
SUBTITLE = ParagraphStyle("subtitle", fontName="Body", fontSize=11, leading=17, textColor=MUTED, spaceAfter=8)
EYEBROW = ParagraphStyle("eyebrow", fontName="BodyBold", fontSize=8, leading=10, textColor=BLUE, spaceAfter=6)
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
    canvas.setFillColor(MINT)
    canvas.setFont("BodyBold", 8)
    canvas.drawString(18 * mm, height - 7.6 * mm, "SCOPESEAL / SYSTEM FOUNDRY")
    canvas.setFillColor(MUTED)
    canvas.setFont("Body", 7)
    canvas.drawString(18 * mm, 10 * mm, "2026-08-03 / BUSINESS MVP REPORT")
    canvas.drawRightString(width - 18 * mm, 10 * mm, str(doc.page))
    canvas.restoreState()


def section(number, title, text):
    return [Paragraph(f"{number:02d} / {title.upper()}", EYEBROW), Paragraph(title, H1), Paragraph(text, BODY)]


def card(title, value, note, accent):
    value_style = ParagraphStyle("value", fontName="BodyBold", fontSize=22, leading=27, textColor=INK)
    table = Table([[Paragraph(title.upper(), SMALL)], [Paragraph(value, value_style)], [Paragraph(note, SMALL)]], colWidths=[50 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white), ("BOX", (0, 0), (-1, -1), .8, LINE),
        ("LINEABOVE", (0, 0), (-1, 0), 4, accent), ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


story = [Spacer(1, 10 * mm), Paragraph("SYSTEM FOUNDRY / BUSINESS MVP", EYEBROW), Paragraph("ScopeSeal", TITLE),
         Paragraph("A local-first change-request ledger that turns revision scope into visible approval and billing decisions.", SUBTITLE), Spacer(1, 12 * mm)]
story.append(Table([[card("Product status", "PASS", "Implemented and verified", MINT), card("Automated tests", "8 / 8", "Zero failures", AMBER), card("Monthly price", "KRW 24K", "Per studio", BLUE)]], colWidths=[55 * mm] * 3))
story += [Spacer(1, 13 * mm)]
story += section(1, "Project overview", "ScopeSeal gives small creative studios a single ledger for revision requests. It compares every request with the contracted revision allowance, calculates a transparent additional-charge estimate, and records approval status before work begins.")
story += section(2, "Target customer", "Two-to-ten-person web, design, and video studios, plus freelancer teams that receive client revisions through email and messengers but do not need a full project-management suite.")
story += section(3, "Problem", "Revision requests are easy to start and hard to bill when contract scope, remaining rounds, effort, and approval live in different places. Studios absorb unplanned work or create client friction with late, unsupported invoices.")
story.append(PageBreak())

story += [Paragraph("PRODUCT", EYEBROW), Paragraph("Three focused jobs", TITLE)]
story += section(4, "Core features", "The MVP implements one complete scope-control loop:")
features = [
    ["01", Paragraph("<b>Validated contract and request intake</b><br/>Store project alias, revision allowance, hourly rate, scope flag, effort, and request date.", BODY)],
    ["02", Paragraph("<b>Automatic allowance and fee classification</b><br/>Use included rounds in sequence, then estimate exhausted or out-of-scope work at the contract rate.", BODY)],
    ["03", Paragraph("<b>Approval-status tracking</b><br/>Move requests through review, quote sent, approved, and complete while keeping billable totals visible.", BODY)],
]
ft = Table(features, colWidths=[14 * mm, 150 * mm])
ft.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), INK), ("TEXTCOLOR", (0, 0), (0, -1), MINT),
    ("FONTNAME", (0, 0), (0, -1), "BodyBold"), ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("GRID", (0, 0), (-1, -1), .5, LINE),
    ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ("LEFTPADDING", (1, 0), (1, -1), 12),
]))
story += [ft, Spacer(1, 7 * mm)]
story += section(5, "How to use", "Set the contract baseline, then register each client request before work starts. Review the automatic included-or-billable label and fee estimate, send the quote if necessary, and update the request status after the client responds.")
story += section(6, "System architecture", "A static browser application loads a pure validation and classification module, renders the ledger, and saves project data in localStorage. There is no account server, database, or external data transfer.")
architecture = Table([["Browser UI", "Scope module", "Local storage", "Node tests"], ["HTML + CSS", "Rules + validation", "Device-only data", "Pure functions"]], colWidths=[41 * mm] * 4)
architecture.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "BodyBold"), ("FONTNAME", (0, 1), (-1, 1), "Body"),
    ("FONTSIZE", (0, 0), (-1, -1), 8), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), .6, LINE), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story += [architecture, Spacer(1, 5 * mm)]
story += section(7, "Technology", "Static HTML, responsive CSS, vanilla JavaScript, localStorage, and the built-in Node.js test runner. Runtime dependency count: zero. Paid API count: zero.")
story.append(PageBreak())

story += [Paragraph("VALIDATED INTERFACE", EYEBROW), Paragraph("Actual running screen", TITLE), Paragraph("Captured from headless Chromium after a new 1.5-hour revision request was validated and classified.", SUBTITLE), Spacer(1, 5 * mm)]
story.append(Image(str(SCREENSHOT), width=166 * mm, height=136 * mm))
story += [Spacer(1, 5 * mm)]
story += section(8, "Running screen", "The verified screen shows four open requests, zero included rounds remaining, KRW 570,000 in estimated additional charges, and three requests awaiting approval. The new request was classified as allowance exhausted with a KRW 90,000 estimate; changing its status to approved reduced the approval queue to two.")
story.append(PageBreak())

story += [Paragraph("VERIFICATION", EYEBROW), Paragraph("Evidence, not assumptions", TITLE)]
story += section(9, "Test results", "All required checks were executed against the generated project.")
checks = [
    ["Check", "Result", "Evidence"],
    ["Dependency installation", "PASS", "npm install completed; zero runtime dependencies"],
    ["Application start", "PASS", "Local HTTP server returned status 200"],
    ["Core workflow", "PASS", "Fee changed KRW 480K to 570K; approvals changed 3 to 2"],
    ["Automated tests", "8 / 8", "Validation, allowance order, fees, status updates"],
    ["README commands", "PASS", "Install, test, and start commands executed"],
    ["Credential scan", "PASS", "No secret patterns and no .env file"],
    ["PDF", "PASS", "Generated, parsed, rendered, visually inspected"],
]
tt = Table(checks, colWidths=[48 * mm, 23 * mm, 94 * mm], repeatRows=1)
tt.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "BodyBold"), ("FONTNAME", (0, 1), (-1, -1), "Body"),
    ("FONTNAME", (1, 1), (1, -1), "BodyBold"), ("TEXTCOLOR", (1, 1), (1, -1), BLUE),
    ("FONTSIZE", (0, 0), (-1, -1), 7.5), ("GRID", (0, 0), (-1, -1), .5, LINE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story += [tt, Spacer(1, 8 * mm)]
story += section(10, "Security and limitations", "ScopeSeal sends no data to external services. Text, number, date, and enumerated values are validated; displayed user text is HTML-escaped; no credentials are required. Use client aliases because device-local data is unencrypted. Storage clearing causes data loss, there is no multi-user audit trail, and fee estimates require confirmation against the signed contract. ScopeSeal is an operations aid, not legal advice or an invoice system.")
story.append(PageBreak())

story += [Paragraph("GO TO MARKET", EYEBROW), Paragraph("Sell clarity before complexity", TITLE)]
story += section(11, "Pricing and revenue model", "Charge KRW 24,000 per studio per month for the local-first MVP, including unlimited local projects and updates. A later team tier can add encrypted sync and approval links at KRW 59,000 per month, but no paid service is required by this version.")
story += section(12, "First customer acquisition", "Recruit ten studios from Korean freelance design and video-production communities. Offer a 14-day pilot on one active client project, then compare untracked revision hours and time-to-approval with the prior messenger workflow. Convert with a reusable change-order summary and evidence of avoided unpaid work.")
story += section(13, "Improvement plan", "Priorities after observing real client revisions:")
for item in ["JSON backup and restore for device migration.", "Exportable approval summary and change-order PDF.", "Multiple projects with archived contract baselines.", "Authenticated encrypted team sync only after multi-user demand is proven."]:
    story.append(Paragraph(f"<font color='#4B67FF'>●</font> {item}", BODY))
story += [Spacer(1, 7 * mm), Paragraph("COMMERCIAL ASSUMPTION", H2), Paragraph("ScopeSeal should stay narrower than full project management. Its value is making the moment between client request and studio work commercially explicit.", BODY)]
story.append(PageBreak())

story += [Paragraph("ASSESSMENT", EYEBROW), Paragraph("Overall evaluation", TITLE)]
story += section(14, "Overall score", "Six dimensions are scored out of 10. A higher maintenance score means easier maintenance.")
ratings = [
    ("Customer problem strength", 9, "Unpaid scope creep directly reduces studio margin and recurs across projects."),
    ("One-day completeness", 9, "The full request, fee, and approval loop is implemented and browser-tested."),
    ("Sales potential", 8, "Clear financial value supports a small monthly price; interviews remain necessary."),
    ("Maintenance difficulty", 9, "Zero runtime dependencies and no backend keep maintenance light."),
    ("Differentiation", 7, "Scope-first calculations are focused, though adjacent PM tools exist."),
    ("Scalability", 8, "Exports, multiple projects, approval links, and team sync create expansion paths."),
]
rows = [["Dimension", "Score", "Rationale"]] + [[name, f"{score}/10", reason] for name, score, reason in ratings]
rt = Table(rows, colWidths=[52 * mm, 20 * mm, 93 * mm])
rt.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "BodyBold"), ("FONTNAME", (0, 1), (-1, -1), "Body"),
    ("FONTNAME", (1, 1), (1, -1), "BodyBold"), ("BACKGROUND", (1, 1), (1, -1), colors.HexColor("#EEF1FF")),
    ("FONTSIZE", (0, 0), (-1, -1), 7.4), ("GRID", (0, 0), (-1, -1), .5, LINE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story += [rt, Spacer(1, 11 * mm)]
overall = Table([[Paragraph("OVERALL", WHITE), Paragraph("8.3 / 10", ParagraphStyle("big", fontName="BodyBold", fontSize=21, leading=25, textColor=MINT)), Paragraph("Proceed to a ten-studio pilot and measure unpaid hours avoided.", WHITE)]], colWidths=[28 * mm, 48 * mm, 89 * mm])
overall.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), INK), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 14), ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
]))
story += [overall, Spacer(1, 10 * mm), Paragraph("Verdict: technically complete and commercially focused for a business MVP. The next evidence is whether studios consistently log requests before starting work and recover measurable revision revenue.", BODY)]

doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=20 * mm, bottomMargin=18 * mm, title="ScopeSeal MVP Report", author="System Foundry", subject="Business MVP implementation and validation report")
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"Generated {OUTPUT}")
