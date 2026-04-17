from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from sympy import content
from datetime import datetime

def generate_pdf(summary, positives, negatives, sentiment_img, wordcloud_img, file_path="report.pdf"):
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = styles["Title"]
    heading_style = styles["Heading2"]

    positive_style = ParagraphStyle(
        name="PositiveStyle",
        parent=styles["Normal"],
        textColor=colors.green,
        fontName="Helvetica-Bold"
    )

    negative_style = ParagraphStyle(
        name="NegativeStyle",
        parent=styles["Normal"],
        textColor=colors.red,
        fontName="Helvetica-Bold"
    )

    normal_style = styles["Normal"]

    content = []

    # Title
    content.append(Paragraph("Customer Review Analysis Report", title_style))
    content.append(Spacer(1, 12))

    # Summary
    content.append(Paragraph("Summary:", heading_style))
    content.append(Paragraph(summary, normal_style))
    content.append(Spacer(1, 12))

    # Positives (GREEN)
    content.append(Paragraph("Positives:", heading_style))
    for p in positives:
        content.append(Paragraph(f"🟢 {p}", positive_style))

    content.append(Spacer(1, 12))

    # Negatives (RED)
    content.append(Paragraph("Negatives:", heading_style))
    for n in negatives:
        content.append(Paragraph(f"🔴 {n}", negative_style))

    content.append(Spacer(1, 12))

    # Add Sentiment Chart
    content.append(Paragraph("Sentiment Distribution:", styles["Heading2"]))
    content.append(Image(sentiment_img, width=400, height=250))

    content.append(Spacer(1, 20))

    # Add Word Cloud
    content.append(Paragraph("Word Cloud:", styles["Heading2"]))
    content.append(Image(wordcloud_img, width=400, height=250))

    content.append(Spacer(1, 20))

    content.append(Paragraph(
    f"Generated on: {datetime.now().strftime('%d %B %Y')}",
    normal_style
    ))      
    content.append(Spacer(1, 12))

    doc.build(content)

    return file_path