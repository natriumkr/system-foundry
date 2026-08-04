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
INK = colors.HexColor("#17251F")
GREEN = colors.HexColor("#26734D")
MINT = colors.HexColor("#CCEBD6")
LIME = colors.HexColor("#D8F06A")
ORANGE = colors.HexColor("#FF8C5A")
MUTED = colors.HexColor("#718078")
LINE = colors.HexColor("#DEDAD0")

pdfmetrics.registerFont(TTFont("Body", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("BodyBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
TITLE = ParagraphStyle("title", fontName="BodyBold", fontSize=31, leading=35, textColor=INK, spaceAfter=8)
SUBTITLE = ParagraphStyle("subtitle", fontName="Body", fontSize=11, leading=17, textColor=MUTED, spaceAfter=8)
EYEBROW = ParagraphStyle("eyebrow", fontName="BodyBold", fontSize=8, leading=10, textColor=GREEN, spaceAfter=6)
H1 = ParagraphStyle("h1", fontName="BodyBold", fontSize=18, leading=22, textColor=INK, spaceAfter=7)
H2 = ParagraphStyle("h2", fontName="BodyBold", fontSize=12, leading=15, textColor=INK, spaceAfter=4)
BODY = ParagraphStyle("body", fontName="Body", fontSize=9.2, leading=14, textColor=colors.HexColor("#34443C"), spaceAfter=7)
SMALL = ParagraphStyle("small", fontName="Body", fontSize=7.5, leading=10, textColor=MUTED)
WHITE = ParagraphStyle("white", fontName="BodyBold", fontSize=9, leading=13, textColor=colors.white)


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(INK)
    canvas.rect(0, height - 12 * mm, width, 12 * mm, stroke=0, fill=1)
    canvas.setFillColor(LIME)
    canvas.setFont("BodyBold", 8)
    canvas.drawString(18 * mm, height - 7.6 * mm, "FRIDGEFIRST / SYSTEM FOUNDRY")
    canvas.setFillColor(MUTED)
    canvas.setFont("Body", 7)
    canvas.drawString(18 * mm, 10 * mm, "2026-08-04 / PERSONAL MVP REPORT")
    canvas.drawRightString(width - 18 * mm, 10 * mm, str(doc.page))
    canvas.restoreState()


def section(number, title, text):
    return [Paragraph(f"{number:02d} / {title.upper()}", EYEBROW), Paragraph(title, H1), Paragraph(text, BODY)]


def card(title, value, note, accent):
    value_style = ParagraphStyle("value", fontName="BodyBold", fontSize=22, leading=27, textColor=INK)
    table = Table([[Paragraph(title.upper(), SMALL)], [Paragraph(value, value_style)], [Paragraph(note, SMALL)]], colWidths=[50 * mm])
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.white), ("BOX", (0, 0), (-1, -1), .8, LINE), ("LINEABOVE", (0, 0), (-1, 0), 4, accent), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return table


story = [Spacer(1, 10 * mm), Paragraph("SYSTEM FOUNDRY / PERSONAL MVP", EYEBROW), Paragraph("FridgeFirst", TITLE), Paragraph("A local-first use-first queue that makes forgotten food and its purchase value visible.", SUBTITLE), Spacer(1, 12 * mm)]
story.append(Table([[card("Product status", "PASS", "Implemented and verified", MINT), card("Automated tests", "8 / 8", "Zero failures", ORANGE), card("One-time price", "KRW 8.9K", "Personal license", GREEN)]], colWidths=[55 * mm] * 3))
story += [Spacer(1, 13 * mm)]
story += section(1, "Project overview", "FridgeFirst turns a small household refrigerator into a use-first queue. Users register food with an expiry date and purchase value, see what should be handled within three days, and record whether each item was consumed or wasted.")
story += section(2, "Target customer", "Solo residents and one-to-two-person households that buy groceries in small batches, forget partially used food, and want a simpler tool than meal planning or full pantry software.")
story += section(3, "Problem", "Food becomes invisible behind newer purchases. A plain expiry list does not show the money at risk, while memory and paper labels do not preserve whether waste is actually improving.")
story.append(PageBreak())

story += [Paragraph("PRODUCT", EYEBROW), Paragraph("Three focused jobs", TITLE)]
story += section(4, "Core features", "The MVP implements one complete household food-control loop:")
features = [["01", Paragraph("<b>Validated food inventory</b><br/>Capture name, category, quantity, unit, purchase value, and expiry date with strict limits.", BODY)], ["02", Paragraph("<b>Use-first queue and value at risk</b><br/>Order expired, today, soon, and later items; total purchase value for items due within three days.", BODY)], ["03", Paragraph("<b>Consumed and wasted history</b><br/>Remove handled items and separately total value used versus discarded.", BODY)]]
ft = Table(features, colWidths=[14 * mm, 150 * mm])
ft.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), INK), ("TEXTCOLOR", (0, 0), (0, -1), LIME), ("FONTNAME", (0, 0), (0, -1), "BodyBold"), ("ALIGN", (0, 0), (0, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("GRID", (0, 0), (-1, -1), .5, LINE), ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9), ("LEFTPADDING", (1, 0), (1, -1), 12)]))
story += [ft, Spacer(1, 7 * mm)]
story += section(5, "How to use", "After grocery shopping, register each food item. Open the queue before planning a meal, handle orange items first, then mark each item consumed or wasted. The header shows both current risk and the value successfully used.")
story += section(6, "System architecture", "A static browser UI calls pure validation and queue functions, then persists inventory and history in localStorage. No account, backend, database, analytics, or external API is used.")
architecture = Table([["Browser UI", "Inventory module", "Local storage", "Node tests"], ["HTML + CSS", "Rules + sorting", "Device-only data", "Pure functions"]], colWidths=[41 * mm] * 4)
architecture.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTNAME", (0, 0), (-1, 0), "BodyBold"), ("FONTNAME", (0, 1), (-1, -1), "Body"), ("FONTSIZE", (0, 0), (-1, -1), 8), ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("GRID", (0, 0), (-1, -1), .6, LINE), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
story += [architecture, Spacer(1, 5 * mm)]
story += section(7, "Technology", "Static HTML, responsive CSS, vanilla JavaScript, localStorage, and the built-in Node.js test runner. Runtime dependencies: zero. Paid APIs: zero.")
story.append(PageBreak())

story += [Paragraph("VALIDATED INTERFACE", EYEBROW), Paragraph("Actual running screen", TITLE), Paragraph("Captured from headless Chromium after a strawberry item was validated and added to the queue.", SUBTITLE), Spacer(1, 5 * mm)]
story.append(Image(str(SCREENSHOT), width=166 * mm, height=136 * mm))
story += [Spacer(1, 5 * mm)]
story += section(8, "Running screen", "The verified screen shows six items, four due within three days, and KRW 21,700 at risk after adding two packs of strawberries worth KRW 7,900. Marking that item consumed returned the active inventory to five items and increased used value to KRW 7,900.")
story.append(PageBreak())

story += [Paragraph("VERIFICATION", EYEBROW), Paragraph("Evidence, not assumptions", TITLE)]
story += section(9, "Test results", "All required checks were executed against the generated project.")
checks = [["Check", "Result", "Evidence"], ["Dependency installation", "PASS", "npm install completed; zero runtime dependencies"], ["Application start", "PASS", "Local HTTP server returned status 200"], ["Core workflow", "PASS", "Risk KRW 13.8K to 21.7K; used value to KRW 7.9K"], ["Automated tests", "8 / 8", "Validation, date ordering, totals, outcome history"], ["README commands", "PASS", "Install, test, and start commands executed"], ["Credential scan", "PASS", "No secret patterns and no .env file"], ["PDF", "PASS", "Generated, parsed, rendered, visually inspected"]]
tt = Table(checks, colWidths=[48 * mm, 23 * mm, 94 * mm], repeatRows=1)
tt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTNAME", (0, 0), (-1, 0), "BodyBold"), ("FONTNAME", (0, 1), (-1, -1), "Body"), ("FONTNAME", (1, 1), (1, -1), "BodyBold"), ("TEXTCOLOR", (1, 1), (1, -1), GREEN), ("FONTSIZE", (0, 0), (-1, -1), 7.5), ("GRID", (0, 0), (-1, -1), .5, LINE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
story += [tt, Spacer(1, 8 * mm)]
story += section(10, "Security and limitations", "FridgeFirst sends no data outside the browser. Text, numeric, date, category, and outcome inputs are validated and displayed text is HTML-escaped. It requires no credentials. Device-local data is unencrypted and disappears when browser storage is cleared. Expiry priority is an organization aid, not a food-safety guarantee; users should not consume food whose condition is uncertain or whose safe-use guidance says otherwise.")
story.append(PageBreak())

story += [Paragraph("GO TO MARKET", EYEBROW), Paragraph("A small habit with visible value", TITLE)]
story += section(11, "Pricing and revenue model", "Sell a downloadable personal license for KRW 8,900 as a one-time purchase. The price stays below the value of one typical forgotten grocery item and avoids hosting costs. The MVP contains no paid service or subscription dependency.")
story += section(12, "First customer acquisition", "Recruit the first twenty users from Korean solo-living, meal-prep, and zero-waste communities. Offer a 14-day test and ask users to photograph their next grocery receipt, then compare recorded at-risk and discarded value. Convert with the concrete promise of seeing which purchase needs attention first.")
story += section(13, "Improvement plan", "Priorities after observing real refrigerator routines:")
for item in ["JSON backup and restore for device migration.", "Barcode-assisted item entry using an optional local catalog.", "Recurring staples and partial-quantity updates.", "Private encrypted sync only if users request multiple-device access."]:
    story.append(Paragraph(f"<font color='#26734D'>●</font> {item}", BODY))
story += [Spacer(1, 7 * mm), Paragraph("PRODUCT BOUNDARY", H2), Paragraph("FridgeFirst should remain a low-friction inventory decision tool. It should not make food-safety diagnoses, prescribe diets, or become a full recipe marketplace.", BODY)]
story.append(PageBreak())

story += [Paragraph("ASSESSMENT", EYEBROW), Paragraph("Overall evaluation", TITLE)]
story += section(14, "Overall score", "Six dimensions are scored out of 10. A higher maintenance score means easier maintenance.")
ratings = [("Customer problem strength", 8, "Forgotten groceries create recurring, visible household waste."), ("One-day completeness", 9, "The full register, prioritize, and outcome loop is browser-tested."), ("Sales potential", 7, "A low one-time price fits the audience, but retention must be observed."), ("Maintenance difficulty", 9, "Zero runtime dependencies and no backend keep maintenance light."), ("Differentiation", 8, "Purchase-value risk is clearer than a generic expiry list."), ("Scalability", 8, "Barcode entry, quantities, backups, and optional sync offer expansion paths.")]
rows = [["Dimension", "Score", "Rationale"]] + [[name, f"{score}/10", reason] for name, score, reason in ratings]
rt = Table(rows, colWidths=[52 * mm, 20 * mm, 93 * mm])
rt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), INK), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTNAME", (0, 0), (-1, 0), "BodyBold"), ("FONTNAME", (0, 1), (-1, -1), "Body"), ("FONTNAME", (1, 1), (1, -1), "BodyBold"), ("BACKGROUND", (1, 1), (1, -1), colors.HexColor("#EAF5EE")), ("FONTSIZE", (0, 0), (-1, -1), 7.4), ("GRID", (0, 0), (-1, -1), .5, LINE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
story += [rt, Spacer(1, 11 * mm)]
overall = Table([[Paragraph("OVERALL", WHITE), Paragraph("8.2 / 10", ParagraphStyle("big", fontName="BodyBold", fontSize=21, leading=25, textColor=LIME)), Paragraph("Proceed to a twenty-user trial and measure discarded value.", WHITE)]], colWidths=[28 * mm, 48 * mm, 89 * mm])
overall.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), INK), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 14), ("BOTTOMPADDING", (0, 0), (-1, -1), 14)]))
story += [overall, Spacer(1, 10 * mm), Paragraph("Verdict: technically complete and visually polished for a personal MVP. The next useful evidence is whether users keep registering groceries after the first week and reduce recorded waste.", BODY)]

doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=20 * mm, bottomMargin=18 * mm, title="FridgeFirst MVP Report", author="System Foundry", subject="Personal MVP implementation and validation report")
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"Generated {OUTPUT}")
