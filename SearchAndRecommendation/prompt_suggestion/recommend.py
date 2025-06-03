
# from state import User
from typing import Optional
import json
# from prompt_suggestion.chains import chain


from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


llm = ChatGoogleGenerativeAI(model = 'gemini-2.0-flash')

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


template = '''
You are a smart autocompletion assistant for writing professional sales proposals.

Based on the given context and company details, generate a list of 3 high-quality autocompletion suggestions. Each suggestion should:
- Start from the last significant word or phrase in the context.
- Be a natural and extended continuation (at least 6-7 sentences).
- Be relevant to the context and company details.
- Maintain a persuasive, business-oriented tone suitable for formal proposals.

Return only a valid Python list of 3 strings. Each string should be a longer paragraph-style continuation. Do not include any explanation, markdown, or other formatting.

Context:
{text}

Company Details:
{company_details}
'''




prompt = ChatPromptTemplate.from_template(template)



chain = prompt | llm | StrOutputParser()
def get_recommendation(text:str ):
    result = chain.invoke({"text":text , "company_details":None}) # returns list of 3 items 
    result = result.strip()
    if result.startswith('```python'):
        result = result[len('```python'):].strip()
    elif result.startswith('```'):
        result = result[len('```'):].strip()
    if result.endswith('```'):
        result = result[:-3].strip()

    return json.loads(result)
 
