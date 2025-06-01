from pydantic import BaseModel,Field

class User(BaseModel):
    name : str = Field(description="name of the organziation")
    logo : str = Field(description="Logo of the given website")
    detailed_description : str = Field(description='A detailed description of what the organization does ')


