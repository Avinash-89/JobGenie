# utils/reporter.py
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(candidate_name: str, score: int, critique: str) -> bytes:
    """
    Compiles candidate evaluation performance matrices into a clean printable PDF binary stream.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom Brand Colors & Typography Styles
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor("#0F2027"), spaceAfter=15
    )
    section_style = ParagraphStyle(
        'SecTitle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor("#203A43"), spaceBefore=12, spaceAfter=8
    )
    body_style = ParagraphStyle(
        'BodyTextCustom', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor("#333333")
    )
    
    # Build Document Body Architecture
    story.append(Paragraph("Enterprise Talent Acquisition Audit Record", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>Candidate Assessment Trace Profile:</b> {candidate_name}", body_style))
    story.append(Paragraph(f"<b>Calculated Cumulative Alignment Benchmark:</b> {score}%", body_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("System Narrative Technical Critique", section_style))
    story.append(Paragraph(critique, body_style))
    
    # Build document
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()