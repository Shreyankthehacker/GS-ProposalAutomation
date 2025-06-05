from pydantic import BaseModel,Field
from typing import List

class User(BaseModel):
    name : str = Field(description="name of the organziation")
    logo : str = Field(description="Logo of the given website")
    description : str = Field(description='A detailed description of what the organization does ')
    services: List[str] = Field(description="A list of services offered by the organization on the given website")
  