from io import BytesIO

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)
from reportlab.lib import colors

from document_utils.common import sanitize_text


def format_pdf(
    text: str,
    doc_type: str,
    logo_bytes: bytes | None = None,
    terms: str = ""
) -> bytes:

    output = BytesIO()

    document = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "LegalEaseTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        spaceAfter=14
    )

    heading_style = ParagraphStyle(
        "LegalEaseHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=8,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        "LegalEaseBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        spaceAfter=7
    )

    story = []

    # Logo
    if logo_bytes:

        try:

            logo_stream = BytesIO(logo_bytes)

            logo = Image(
                logo_stream,
                width=1.25 * inch,
                height=1.25 * inch
            )

            logo.hAlign = "CENTER"

            story.append(logo)
            story.append(Spacer(1, 8))

        except Exception:
            pass

    # Title
    story.append(
        Paragraph(
            sanitize_text(doc_type).upper(),
            title_style
        )
    )

    clean_text = sanitize_text(text)

    lines = clean_text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            story.append(Spacer(1, 5))
            continue

        safe_line = (
            line
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        if (
            len(line) < 100
            and (
                line.isupper()
                or line[:2].isdigit()
                or line.startswith("SECTION")
                or line.startswith("ARTICLE")
            )
        ):

            story.append(
                Paragraph(
                    safe_line,
                    heading_style
                )
            )

        else:

            story.append(
                Paragraph(
                    safe_line,
                    body_style
                )
            )

    # Terms table
    term_list = [
        item.strip()
        for item in terms.split(";")
        if item.strip()
    ]

    if term_list:

        story.append(Spacer(1, 10))

        story.append(
            Paragraph(
                "KEY TERMS",
                heading_style
            )
        )

        table_data = [
            ["No.", "Term"]
        ]

        for index, term in enumerate(
            term_list,
            start=1
        ):

            table_data.append(
                [
                    str(index),
                    term
                ]
            )

        table = Table(
            table_data,
            colWidths=[
                0.6 * inch,
                5.8 * inch
            ]
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        9
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),
                ]
            )
        )

        story.append(table)

    def add_footer(canvas, doc):
        canvas.saveState()

        canvas.setFont(
            "Helvetica",
            8
        )

        canvas.drawCentredString(
            A4[0] / 2,
            0.35 * inch,
            "Generated with LegalEase - AI Legal Document Drafting"
        )

        canvas.restoreState()

    document.build(
        story,
        onFirstPage=add_footer,
        onLaterPages=add_footer
    )

    output.seek(0)

    return output.getvalue()