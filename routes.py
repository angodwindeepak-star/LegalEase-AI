from fastapi import APIRouter, HTTPException

from backend.schemas import (
    GenerateRequest,
    GenerateResponse
)

from backend.services.gemini_generator import (
    GeminiDocumentGenerator
)


router = APIRouter(
    prefix="/api",
    tags=["LegalEase"]
)

generator = GeminiDocumentGenerator()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "LegalEase Backend"
    }


@router.post(
    "/generate",
    response_model=GenerateResponse
)
def generate_document(request: GenerateRequest):

    try:

        generated_text = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            date=request.date
        )

        return GenerateResponse(
            success=True,
            document_type=request.document_type,
            content=generated_text,
            message="Document generated successfully."
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {exc}"
        )