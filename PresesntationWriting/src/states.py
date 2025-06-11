from pydantic import BaseModel,Field
from typing import List,Annotated,Optional
import operator

from WebScraper.state import User

class State(BaseModel):
    buyer : User
    seller :User
    client_requirement: str  
    additional_info : List[str]
    service_dept : str
    sections : List[str] 
    final_result : str 
    