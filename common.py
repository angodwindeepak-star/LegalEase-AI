import re
from pathlib import Path


def sanitize_text(text: str) -> str:
    """
    Clean common typographic characters and excessive whitespace.
    """

    if not text:
        return ""

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
        "\u2022": "-",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def safe_filename(name: str) -> str:

    name = sanitize_text(name)

    name = re.sub(
        r"[^a-zA-Z0-9_\- ]+",
        "",
        name
    )

    name = name.strip().replace(" ", "_")

    return name or "LegalEase_Document"


def validate_logo(logo_bytes: bytes) -> bool:
    """
    Basic validation for an uploaded logo.
    """

    if not logo_bytes:
        return False

    allowed_signatures = [
        b"\x89PNG",
        b"\xff\xd8\xff",
        b"GIF8",
    ]

    return any(
        logo_bytes.startswith(signature)
        for signature in allowed_signatures
    )