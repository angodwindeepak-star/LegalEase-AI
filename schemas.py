from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    document_type: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Type of legal document"
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=10000,
        description="Parties involved in the agreement"
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=15000,
        description="Terms and conditions"
    )

    date: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Effective date"
    )


class GenerateResponse(BaseModel):
    success: bool
    document_type: str
    content: str
    message: str = ""