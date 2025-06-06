
from WebScraper.state import User
from typing import Optional
import json
from SearchAndRecommendation.prompt_suggestion.chains import chain,time_chain
import ast 



def get_recommendation(text:str , buyer : User ,seller : User):
    result = chain.invoke({"text":text , "buyer":buyer,'seller':seller}) # returns list of 3 items 
    result = result.strip()
    if result.startswith('```python'):
        result = result[len('```python'):].strip()
    elif result.startswith('```'):
        result = result[len('```'):].strip()
    if result.endswith('```'):
        result = result[:-3].strip()
    
    result = ast.literal_eval(result)
    print(type(result))

    return result
 



def get_project_specification(text:str , buyer :User , seller : User):
    '''{project_specifications}

    - 🧑‍💼 **Buyer Details**:
    {buyer_details}

    - 🏢 **Seller (Service Provider) Details**:
    {seller_details}'''
    result = time_chain.invoke({'project_specifications':text,'buyer_details':buyer,'seller_details':seller})
    if result.startswith('```python'):
        result = result[len('```python'):].strip()
    elif result.startswith('```'):
        result = result[len('```'):].strip()
    if result.endswith('```'):
        result = result[:-3].strip()
    
    result = ast.literal_eval(result)
    print(type(result))

    return result


