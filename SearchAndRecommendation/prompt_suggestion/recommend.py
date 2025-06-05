
from WebScraper.state import User
from typing import Optional
import json
from SearchAndRecommendation.prompt_suggestion.chains import chain



def get_recommendation(text:str , user : User ):
    result = chain.invoke({"text":text , "company_details":user}) # returns list of 3 items 
    result = result.strip()
    if result.startswith('```python'):
        result = result[len('```python'):].strip()
    elif result.startswith('```'):
        result = result[len('```'):].strip()
    if result.endswith('```'):
        result = result[:-3].strip()

    return json.loads(result)
 
