import os
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


class GeminiDocumentGenerator:
    """
    Generates legal document drafts using Google's Gemini API.

    If GEMINI_API_KEY is not configured, the application uses
    a local demo generator so the rest of the project can still
    be tested.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()

        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

        self.max_output_tokens = int(
            os.getenv("MAX_OUTPUT_TOKENS", "12000")
        )

        self.temperature = float(
            os.getenv("TEMPERATURE", "0.2")
        )

        self.client: Optional[genai.Client] = None

        if self.api_key and self.api_key != "YOUR_GEMINI_API_KEY":
            self.client = genai.Client(
                api_key=self.api_key
            )

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        date: str
    ) -> str:

        if not self.client:
            return self._demo_document(
                document_type=document_type,
                parties=parties,
                terms=terms,
                date=date
            )

        prompt = self._build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            date=date
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_output_tokens,
                )
            )

            generated_text = getattr(response, "text", None)

            if not generated_text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return generated_text.strip()

        except Exception as exc:
            # Keep the application usable even when the API
            # is temporarily unavailable.
            print(f"Gemini API error: {exc}")

            return self._demo_document(
                document_type=document_type,
                parties=parties,
                terms=terms,
                date=date
            )

    def _build_prompt(
        self,
        document_type: str,
        parties: str,
        terms: str,
        date: str
    ) -> str:

        return f"""
You are a professional legal-document drafting assistant.

Create a structured draft of the following legal document.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{date}

TERMS AND CONDITIONS:
{terms}

Requirements:

1. Create a clear professional legal-document structure.
2. Include an appropriate title.
3. Include the parties and effective date.
4. Organize the document using numbered sections.
5. Convert the supplied terms into suitable clauses.
6. Include definitions when useful.
7. Include responsibilities and obligations where relevant.
8. Include confidentiality provisions when relevant.
9. Include termination provisions when relevant.
10. Include governing-law/dispute provisions only when appropriate.
11. Include signature sections for the parties.
12. Do not invent specific personal information that was not supplied.
13. Do not claim that the document is legally valid in every jurisdiction.
14. Keep the output editable plain text.
15. Do not use markdown code fences.

Important:
This is a drafting assistant. The resulting document should be reviewed
by a qualified legal professional before being relied upon.

Return only the document draft.
""".strip()

    def _demo_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        date: str
    ) -> str:

        term_list = [
            item.strip()
            for item in terms.split(";")
            if item.strip()
        ]

        lines = []

        lines.append(document_type.upper())
        lines.append("")
        lines.append(f"Effective Date: {date}")
        lines.append("")
        lines.append("PARTIES")
        lines.append("")
        lines.append(parties)
        lines.append("")
        lines.append("AGREEMENT")
        lines.append("")

        lines.append(
            "This document is a draft agreement prepared from "
            "the information provided by the user."
        )

        lines.append("")

        lines.append("1. PURPOSE")
        lines.append("")
        lines.append(
            f"The purpose of this {document_type.lower()} is to "
            "record the terms agreed between the parties."
        )

        lines.append("")

        lines.append("2. TERMS AND CONDITIONS")
        lines.append("")

        if term_list:
            for index, term in enumerate(term_list, start=1):
                lines.append(f"{index}. {term}")
        else:
            lines.append(
                "The parties shall comply with the terms and "
                "conditions agreed between them."
            )

        lines.append("")

        lines.append("3. GENERAL PROVISIONS")
        lines.append("")
        lines.append(
            "The parties should review all provisions and make "
            "any jurisdiction-specific changes required before signing."
        )

        lines.append("")

        lines.append("4. SIGNATURES")
        lines.append("")
        lines.append("Party 1:")
        lines.append("")
        lines.append("Name: ______________________________")
        lines.append("Signature: ___________________________")
        lines.append("Date: _______________________________")
        lines.append("")
        lines.append("Party 2:")
        lines.append("")
        lines.append("Name: ______________________________")
        lines.append("Signature: ___________________________")
        lines.append("Date: _______________________________")
        lines.append("")
        lines.append(
            "LEGAL REVIEW NOTICE: This draft is generated for "
            "document-drafting purposes and should be reviewed by "
            "a qualified legal professional before use."
        )

        return "\n".join(lines)