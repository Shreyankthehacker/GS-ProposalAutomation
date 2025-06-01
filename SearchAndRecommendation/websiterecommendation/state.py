from pydantic import BaseModel,Field

class WebSite(BaseModel):
    website_name : str = Field(description="Website name")
    website_url : str = Field(description="Website url")
