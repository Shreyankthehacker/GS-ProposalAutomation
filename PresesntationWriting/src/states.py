from pydantic import BaseModel,Field
from typing import List,Annotated,Optional
import operator

from WebScraper.state import User

class State(BaseModel):
    buyer : Optional[User] = Field(description=' ')
    seller :Optional[User] = Field(description=' ')
    client_requirement: str  
    additional_info : List[str]
    service_dept : str
    sections : List[str] = Field(description="Total sections inside the sales proposal")
    final_result : str = Field(description='')
    