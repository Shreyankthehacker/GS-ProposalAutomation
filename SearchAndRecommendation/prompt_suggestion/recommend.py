
from WebScraper.state import User
from typing import Optional
import json
from chains import chain


def get_recommendation(text:str , org : Optional[User]):
    result = chain.invoke({"text":text , "company_details":org}) # returns list of 3 items 
    result = result.strip()
    if result.startswith('```python'):
        result = result[len('```python'):].strip()
    elif result.startswith('```'):
        result = result[len('```'):].strip()
    if result.endswith('```'):
        result = result[:-3].strip()

    return json.loads(result)
 
