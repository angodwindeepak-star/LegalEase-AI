import os
import sys
import html
import requests
import streamlit as st

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
from document_utils.common import safe_filename
from document_utils.docx_export import format_docx
from document_utils.pdf_export import format_pdf


load_dotenv()


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


APP_NAME = os.getenv(
    "APP_NAME",
    "LegalEase"
)


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        opacity: 0.75;
        margin-bottom: 30px;
    }

    .preview-box {
        background-color: #111827;
        color: #f9fafb;
        border-radius: 12px;
        padding: 25px;
        max-height: 600px;
        overflow-y: auto;
        white-space: pre-wrap;
        line-height: 1.6;
        font-family: Georgia, serif;
    }

    .info-box {
        padding: 15px;
        border-radius: 10px;
        background-color: rgba(128, 128, 128, 0.12);
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "generated_document" not in st.session_state:
    st.session_state.generated_document = ""

if "document_type" not in st.session_state:
    st.session_state.document_type = ""

if "terms" not in st.session_state:
    st.session_state.terms = ""

if "logo_bytes" not in st.session_state:
    st.session_state.logo_bytes = None


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Legal Document Drafting Assistant'
    '</div>',
    unsafe_allow_html=True
)


st.info(
    "LegalEase creates editable legal-document drafts from your "
    "inputs. Review the generated document carefully and obtain "
    "professional legal advice before relying on it."
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ Document Settings")

    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement (NDA)",
            "Lease Agreement",
            "Freelance Agreement",
            "Service Agreement",
            "Partnership Agreement",
            "Consulting Agreement",
            "Sales Agreement",
            "General Agreement",
            "Other"
        ]
    )

    if document_type == "Other":

        document_type = st.text_input(
            "Enter Document Type",
            placeholder="Example: Software License Agreement"
        )

    effective_date = st.text_input(
        "Effective Date",
        placeholder="Example: 01 October 2026"
    )

    logo = st.file_uploader(
        "Upload Company Logo",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )

    if logo:

        logo_bytes = logo.getvalue()

        st.session_state.logo_bytes = logo_bytes

        st.image(
            logo_bytes,
            caption="Uploaded Logo",
            width=150
        )

    else:

        st.session_state.logo_bytes = None


# ---------------------------------------------------------
# Main input area
# ---------------------------------------------------------

left, right = st.columns(
    [1, 1]
)


with left:

    st.subheader("👥 Parties")

    parties = st.text_area(
        "Enter the parties involved",
        height=180,
        placeholder=(
            "Example:\n"
            "Party 1: ABC Technologies Pvt. Ltd.\n"
            "Party 2: John Doe\n\n"
            "Include names, roles, addresses or other relevant "
            "details that should appear in the document."
        )
    )


with right:

    st.subheader("📋 Terms & Conditions")

    terms = st.text_area(
        "Enter terms separated by semicolons (;)",
        height=180,
        placeholder=(
            "Example:\n"
            "Monthly salary: INR 50,000; "
            "Confidentiality period: 2 years; "
            "Notice period: 30 days; "
            "Working hours: 9 AM to 6 PM"
        )
    )


# ---------------------------------------------------------
# Generate button
# ---------------------------------------------------------

st.divider()


generate_clicked = st.button(
    "🚀 Generate Legal Document",
    type="primary",
    use_container_width=True
)


if generate_clicked:

    if not document_type.strip():

        st.error(
            "Please select or enter a document type."
        )

    elif not parties.strip():

        st.error(
            "Please enter the parties involved."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms and conditions."
        )

    elif not effective_date.strip():

        st.error(
            "Please enter the effective date."
        )

    else:

        payload = {
            "document_type": document_type.strip(),
            "parties": parties.strip(),
            "terms": terms.strip(),
            "date": effective_date.strip()
        }

        with st.spinner(
            "Generating your legal document..."
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/api/generate",
                    json=payload,
                    timeout=180
                )

                if response.status_code == 200:

                    data = response.json()

                    if data.get("success"):

                        st.session_state.generated_document = (
                            data.get("content", "")
                        )

                        st.session_state.document_type = (
                            document_type
                        )

                        st.session_state.terms = terms

                        st.success(
                            "Document generated successfully!"
                        )

                    else:

                        st.error(
                            data.get(
                                "message",
                                "Generation failed."
                            )
                        )

                else:

                    try:
                        error_data = response.json()
                        error_message = error_data.get(
                            "detail",
                            response.text
                        )
                    except Exception:
                        error_message = response.text

                    st.error(
                        f"Backend error: {error_message}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to the FastAPI backend. "
                    "Please make sure the backend is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. Please try again."
                )

            except Exception as exc:

                st.error(
                    f"Unexpected error: {exc}"
                )


# ---------------------------------------------------------
# Generated document
# ---------------------------------------------------------

if st.session_state.generated_document:

    st.divider()

    st.subheader("📄 Generated Document")

    edited_document = st.text_area(
        "Edit the document if required",
        value=st.session_state.generated_document,
        height=600
    )

    st.session_state.generated_document = edited_document

    # -----------------------------------------------------
    # Preview
    # -----------------------------------------------------

    st.subheader("👁️ Preview")

    preview_html = html.escape(
        edited_document
    )

    st.markdown(
        f"""
        <div class="preview-box">
        {preview_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # -----------------------------------------------------
    # Download files
    # -----------------------------------------------------

    st.subheader("⬇️ Download")

    file_base_name = safe_filename(
        st.session_state.document_type
    )

    col1, col2, col3 = st.columns(3)

    # TXT
    with col1:

        st.download_button(
            label="📄 Download TXT",
            data=edited_document.encode(
                "utf-8"
            ),
            file_name=f"{file_base_name}.txt",
            mime="text/plain",
            use_container_width=True
        )

    # DOCX
    with col2:

        try:

            docx_bytes = format_docx(
                text=edited_document,
                doc_type=st.session_state.document_type,
                logo_bytes=st.session_state.logo_bytes,
                terms=st.session_state.terms
            )

            st.download_button(
                label="📝 Download DOCX",
                data=docx_bytes,
                file_name=f"{file_base_name}.docx",
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.wordprocessingml.document"
                ),
                use_container_width=True
            )

        except Exception as exc:

            st.error(
                f"DOCX export failed: {exc}"
            )

    # PDF
    with col3:

        try:

            pdf_bytes = format_pdf(
                text=edited_document,
                doc_type=st.session_state.document_type,
                logo_bytes=st.session_state.logo_bytes,
                terms=st.session_state.terms
            )

            st.download_button(
                label="📕 Download PDF",
                data=pdf_bytes,
                file_name=f"{file_base_name}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        except Exception as exc:

            st.error(
                f"PDF export failed: {exc}"
            )