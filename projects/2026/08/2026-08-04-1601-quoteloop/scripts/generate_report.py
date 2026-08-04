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
INK = colors.HexColor("#101B35")
BLUE = colors.HexColor("#4668FF")
PALE = colors.HexColor("#E9EEFF")
CYAN = colors.HexColor("#6DD0E5")
CORAL = colors.HexColor("#F5665C")
MUTED = colors.HexColor("#74809A")
LINE = colors.HexColor("#DDD9CF")

pdfmetrics.registerFont(TTFont("Body", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("BodyBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
TITLE = ParagraphStyle("title", fontName="BodyBold", fontSize=31, leading=35, textColor=INK, spaceAfter=8)
SUBTITLE = ParagraphStyle("subtitle", fontName="Body", fontSize=11, leading=17, textColor=MUTED, spaceAfter=8)
EYEBROW = ParagraphStyle("eyebrow", fontName="BodyBold", fontSize=8, leading=10, textColor=BLUE, spaceAfter=6)
H1 = ParagraphStyle("h1", fontName="BodyBold", fontSize=18, leading=22, textColor=INK, spaceAfter=7)
H2 = ParagraphStyle("h2", fontName="BodyBold", fontSize=12, leading=15, textColor=INK, spaceAfter=4)
BODY = ParagraphStyle("body", fontName="Body", fontSize=9.2, leading=14, textColor=colors.HexColor("#35415B"), spaceAfter=7)
SMALL = ParagraphStyle("small", fontName="Body", fontSize=7.5, leading=10, textColor=MUTED)
WHITE = ParagraphStyle("white", fontName="BodyBold", fontSize=9, leading=13, textColor=colors.white)


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(INK)
    canvas.rect(0, height - 12 * mm, width, 12 * mm, stroke=0, fill=1)
    canvas.setFillColor(CYAN)
    canvas.setFont("BodyBold", 8)
    canvas.drawString(18 * mm, height - 7.6 * mm, "QUOTELOOP / SYSTEM FOUNDRY")
    canvas.setFillColor(MUTED)
    canvas.setFont("Body", 7)
    canvas.drawString(18 * mm, 10 * mm, "2026-08-04 / BUSINESS MVP REPORT")
    canvas.drawRightString(width - 18 * mm, 10 * mm, str(doc.page))
    canvas.restoreState()


def section(number, title, text):
    return [Paragraph(f"{number:02d} / {title.upper()}", EYEBROW), Paragraph(title, H1), Paragraph(text, BODY)]


def card(title, value, note, accent):
    value_style = ParagraphStyle("value", fontName="BodyBold", fontSize=22, leading=27, textColor=INK)
    table = Table([[Paragraph(title.upper(), SMALL)], [Paragraph(value, value_style)], [Paragraph(note, SMALL)]], colWidths=[50 * mm])
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.white), ("BOX", (0, 0), (-1, -1), .8, LINE), ("LINEABOVE", (0, 0), (-1, 0), 4, accent), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return table


story = [Spacer(1, 10 * mm), Paragraph("SYSTEM FOUNDRY / BUSINESS MVP", EYEBROW), Paragraph("QuoteLoop", TITLE), Paragraph("A local-first follow-up queue that keeps sent quotes visible until a decision is recorded.", SUBTITLE), Spacer(1, 12 * mm)]
story.append(Table([[card("Product status", "PASS", "Implemented and verified", CYAN), card("Automated tests", "8 / 8", "Zero failures", CORAL), card("Monthly price", "KRW 17K", "Per business", BLUE)]], colWidths=[55 * mm] * 3))
story += [Spacer(1, 13 * mm)]
story += section(1, "Project overview", "QuoteLoop gives a small service business one place to register sent quotes, see which prospect needs a follow-up today, and measure open, weighted, and won pipeline value. It deliberately avoids becoming a full CRM.")
story += section(2, "Target customer", "Solo operators and teams of two to ten selling photography, video, design, cleaning, repair, or other quote-based services without a dedicated sales system.")
story += section(3, "Problem", "Quotes often leave the operator's attention after email delivery. Spreadsheet rows do not surface urgency, and generic task tools do not connect the next contact date to potential revenue, so promising work quietly goes cold.")
story.append(PageBreak())

story += [Paragraph("PRODUCT", EYEBROW), Paragraph("Three focused jobs", TITLE)]
story += section(4, "Core features", "The MVP implements a complete quote follow-up loop:")
features = [["01", Paragraph("<b>Validated quote intake</b><br/>Capture an anonymous client alias, service, amount, probability, status, and follow-up date with strict limits.", BODY)], ["02", Paragraph("<b>Urgency queue</b><br/>Order overdue, today, upcoming, and closed quotes so the next useful action stays visible.", BODY)], ["03", Paragraph("<b>Weighted pipeline tracking</b><br/>Calculate open value, probability-weighted value, overdue count, and won revenue as status changes.", BODY)]]
ft = Table(features, colWidths=[14 * mm, 150 * mm])
ft.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), INK), ("TEXTCOLOR", (0, 0), (0, -1), CYAN), ("FONTNAME", (0, 0), (0, -1), "BodyBold"), ("ALIGN", (0, 0), (0, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("GRID", (0, 0), (-1, -1), .5, LINE), ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9), ("LEFTPADDING", (1, 0), (1, -1), 12)]))
story += [ft, Spacer(1, 7 * mm)]
story += section(5, "How to use", "After sending a quote, register it with a non-identifying client alias and choose the next contact date. Work down the queue from overdue to later. When the customer decides, change the status to won or lost so open and won totals update immediately.")
story += section(6, "System architecture", "A static browser UI calls pure validation, urgency, and aggregation functions. State is saved only in localStorage. The same pure module is exercised by Node tests; no server, account, database, analytics, or external API exists.")
architecture = Table([["Browser UI", "Pipeline module", "Local storage", "Node tests"], ["HTML + CSS", "Rules + totals", "Device-only data", "Pure functions"]], colWidths=[41 * mm] * 4)
architecture.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTNAME", (0, 0), (-1, 0), "BodyBold"), ("FONTNAME", (0, 1), (-1, -1), "Body"), ("FONTSIZE", (0, 0), (-1, -1), 8), ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("GRID", (0, 0), (-1, -1), .6, LINE), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
story += [architecture, Spacer(1, 5 * mm)]
story += section(7, "Technology", "Static HTML, responsive CSS, vanilla JavaScript, localStorage, bundled Noto Sans KR fonts, and the built-in Node.js test runner. Runtime dependencies: zero. Paid APIs: zero.")
story.append(PageBreak())

story += [Paragraph("VALIDATED INTERFACE", EYEBROW), Paragraph("Actual running screen", TITLE), Paragraph("Captured from headless Chromium after a new showroom quote was validated and added.", SUBTITLE), Spacer(1, 4 * mm)]
story.append(Image(str(SCREENSHOT), width=166 * mm, height=153 * mm))
story += [Spacer(1, 4 * mm)]
story += section(8, "Running screen", "The verified screen shows four open quotes, one overdue follow-up, KRW 6.66M open value, and KRW 4.17M weighted pipeline after adding a KRW 1.5M showroom quote. Marking it won returned open totals to their starting values and raised won revenue to KRW 2.7M.")
story.append(PageBreak())

story += [Paragraph("VERIFICATION", EYEBROW), Paragraph("Evidence, not assumptions", TITLE)]
story += section(9, "Test results", "Every required check was executed against the generated project.")
checks = [["Check", "Result", "Evidence"], ["Dependency installation", "PASS", "npm install completed; zero runtime dependencies"], ["Application start", "PASS", "README HTTP server returned status 200"], ["Core workflow", "PASS", "Open 3 to 4 to 3; weighted KRW 3.42M to 4.17M"], ["Automated tests", "8 / 8", "Validation, urgency, totals, status transitions"], ["README commands", "PASS", "Install, test, and start commands executed"], ["Credential scan", "PASS", "No secret patterns and no .env file"], ["PDF", "PASS", "Generated, parsed, rendered, visually inspected"]]
tt = Table(checks, colWidths=[48 * mm, 23 * mm, 94 * mm], repeatRows=1)
tt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTNAME", (0, 0), (-1, 0), "BodyBold"), ("FONTNAME", (0, 1), (-1, -1), "Body"), ("FONTNAME", (1, 1), (1, -1), "BodyBold"), ("TEXTCOLOR", (1, 1), (1, -1), BLUE), ("FONTSIZE", (0, 0), (-1, -1), 7.5), ("GRID", (0, 0), (-1, -1), .5, LINE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
story += [tt, Spacer(1, 8 * mm)]
story += section(10, "Security and limitations", "QuoteLoop sends no data outside the browser. Text, amount, probability, status, and date inputs are validated; displayed user text is HTML-escaped. It requires no credentials and encourages non-identifying aliases. Device-local data is unencrypted and disappears when browser storage is cleared. Probability is a manual estimate, not a revenue guarantee. The MVP has no email automation, contact database, team accounts, or CRM synchronization.")
story.append(PageBreak())

story += [Paragraph("GO TO MARKET", EYEBROW), Paragraph("Make follow-up revenue visible", TITLE)]
story += section(11, "Pricing and revenue model", "Charge KRW 17,000 per business per month, including local use and updates. A single recovered small service quote can cover many months. The MVP itself has no hosting or paid-service dependency; a future hosted tier would add encrypted sync and multiple seats.")
story += section(12, "First customer acquisition", "Recruit the first fifteen businesses from local photography, design, cleaning, and repair communities. Import only their five most recent open quotes, run a two-week follow-up sprint, and compare overdue count and won value. Convert with the concrete result of recovered quotes rather than generic productivity claims.")
story += section(13, "Improvement plan", "Priorities after validating repeated use:")
for item in ["JSON backup and restore for device migration.", "Reusable service templates and default probability bands.", "Calendar reminders without storing customer contact details.", "Private encrypted sync and role-based team access only after demand is proven."]:
    story.append(Paragraph(f"<font color='#4668FF'>●</font> {item}", BODY))
story += [Spacer(1, 7 * mm), Paragraph("PRODUCT BOUNDARY", H2), Paragraph("QuoteLoop should remain a focused follow-up control surface. It should not become an unprotected contact database, send messages without review, or claim that probability-weighted value is guaranteed revenue.", BODY)]
story.append(PageBreak())

story += [Paragraph("ASSESSMENT", EYEBROW), Paragraph("Overall evaluation", TITLE)]
story += section(14, "Overall score", "Six dimensions are scored out of 10. A higher maintenance score means easier maintenance.")
ratings = [("Customer problem strength", 8, "Missed follow-ups directly delay or lose service revenue."), ("One-day completeness", 9, "The register, prioritize, total, and close loop is browser-tested."), ("Sales potential", 8, "Recovering one quote gives a clear monthly subscription value case."), ("Maintenance difficulty", 9, "Zero runtime dependencies and no backend keep maintenance light."), ("Differentiation", 7, "Urgency plus weighted value is useful, though CRM tools overlap."), ("Scalability", 8, "Templates, reminders, encrypted sync, and seats offer expansion paths.")]
rows = [["Dimension", "Score", "Rationale"]] + [[name, f"{score}/10", reason] for name, score, reason in ratings]
rt = Table(rows, colWidths=[52 * mm, 20 * mm, 93 * mm])
rt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTNAME", (0, 0), (-1, 0), "BodyBold"), ("FONTNAME", (0, 1), (-1, -1), "Body"), ("FONTNAME", (1, 1), (1, -1), "BodyBold"), ("BACKGROUND", (1, 1), (1, -1), PALE), ("FONTSIZE", (0, 0), (-1, -1), 7.4), ("GRID", (0, 0), (-1, -1), .5, LINE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
story += [rt, Spacer(1, 11 * mm)]
overall = Table([[Paragraph("OVERALL", WHITE), Paragraph("8.2 / 10", ParagraphStyle("big", fontName="BodyBold", fontSize=21, leading=25, textColor=CYAN)), Paragraph("Proceed to a fifteen-business follow-up sprint.", WHITE)]], colWidths=[28 * mm, 48 * mm, 89 * mm])
overall.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), INK), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 14), ("BOTTOMPADDING", (0, 0), (-1, -1), 14)]))
story += [overall, Spacer(1, 10 * mm), Paragraph("Verdict: technically complete and visually polished for a business MVP. The next decisive evidence is whether overdue follow-ups fall and won revenue rises during a two-week customer trial.", BODY)]

doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=20 * mm, bottomMargin=18 * mm, title="QuoteLoop MVP Report", author="System Foundry", subject="Business MVP implementation and validation report")
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"Generated {OUTPUT}")
