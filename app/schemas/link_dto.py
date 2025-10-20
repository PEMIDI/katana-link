from pydantic import BaseModel, HttpUrl, Field


class LinkCreate(BaseModel):
    long_link: HttpUrl = Field(
        ...,
        description="The long URL that the short link redirects to."
    )


from pydantic import BaseModel


class LinkRead(BaseModel):
    short_link: str = None
    long_link: str = None


class GetLongUrlRequest(BaseModel):
    short_url: str = None


class GetLongUrlResponse(BaseModel):
    long_url: str = None