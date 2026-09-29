from io import BytesIO

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.shared import Inches, Pt

from document_utils.common import sanitize_text


def format_docx(
    text: str,
    doc_type: str,
    logo_bytes: bytes | None = None,
    terms: str = ""
) -> bytes:

    document = Document()

    section = document.sections[0]

    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    # Default font
    styles = document.styles

    normal_style = styles["Normal"]

    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(11)

    # Logo
    if logo_bytes:

        try:
            logo_stream = BytesIO(logo_bytes)

            paragraph = document.add_paragraph()

            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

            run = paragraph.add_run()

            run.add_picture(
                logo_stream,
                width=Inches(1.3)
            )

        except Exception:
            pass

    # Title
    title = document.add_paragraph()

    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = title.add_run(
        sanitize_text(doc_type).upper()
    )

    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)

    # Body
    clean_text = sanitize_text(text)

    paragraphs = clean_text.split("\n")

    for line in paragraphs:

        line = line.strip()

        if not line:
            document.add_paragraph()
            continue

        paragraph = document.add_paragraph()

        # Detect headings
        if (
            len(line) < 100
            and (
                line.isupper()
                or line[:2].isdigit()
                or line.startswith("SECTION")
                or line.startswith("ARTICLE")
            )
        ):

            run = paragraph.add_run(line)

            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)

        else:

            run = paragraph.add_run(line)

            run.font.name = "Times New Roman"
            run.font.size = Pt(11)

    # Terms table
    term_list = [
        item.strip()
        for item in terms.split(";")
        if item.strip()
    ]

    if term_list:

        document.add_paragraph()

        heading = document.add_paragraph()

        heading_run = heading.add_run(
            "KEY TERMS"
        )

        heading_run.bold = True
        heading_run.font.name = "Times New Roman"
        heading_run.font.size = Pt(12)

        table = document.add_table(
            rows=1,
            cols=2
        )

        table.style = "Table Grid"

        table.rows[0].cells[0].text = "No."
        table.rows[0].cells[1].text = "Term"

        for index, term in enumerate(
            term_list,
            start=1
        ):

            cells = table.add_row().cells

            cells[0].text = str(index)
            cells[1].text = term

    # Footer
    footer = section.footer

    footer_paragraph = footer.paragraphs[0]

    footer_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    footer_run = footer_paragraph.add_run(
        "Generated with LegalEase - AI Legal Document Drafting"
    )

    footer_run.font.name = "Times New Roman"
    footer_run.font.size = Pt(8)

    output = BytesIO()

    document.save(output)

    output.seek(0)

    return output.getvalue()