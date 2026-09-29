from document_utils.docx_export import format_docx
from document_utils.pdf_export import format_pdf


def test_docx_export():

    content = """
    EMPLOYMENT CONTRACT

    1. PURPOSE

    This is a test legal document.

    2. TERMS

    The employee shall perform the agreed responsibilities.
    """

    result = format_docx(
        text=content,
        doc_type="Employment Contract",
        terms="Salary: INR 50,000; Notice: 30 days"
    )

    assert isinstance(result, bytes)

    # DOCX files are ZIP-based.
    assert result[:2] == b"PK"


def test_pdf_export():

    content = """
    EMPLOYMENT CONTRACT

    1. PURPOSE

    This is a test legal document.
    """

    result = format_pdf(
        text=content,
        doc_type="Employment Contract",
        terms="Salary: INR 50,000; Notice: 30 days"
    )

    assert isinstance(result, bytes)

    assert result.startswith(
        b"%PDF"
    )