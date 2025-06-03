from langchain_google_genai import ChatGoogleGenerativeAI
from WebScraper.state import User
from typing import Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


llm = ChatGoogleGenerativeAI(model = 'gemini-2.0-flash')


template = '''
You are an intelligent autocompletion assistant for writing sales proposals.

Based on the existing context and company details, identify the last significant word or phrase (e.g., "shareholders", "efficiency", "data-driven approach") and generate 3 smart, professional autocompletion suggestions that continue the sentence or paragraph starting with that word or phrase.

Each suggestion should:
- Start with the given word or phrase exactly as in the context.
- Continue with a relevant, persuasive, and context-aware sentence fragment or full sentence.
- Be tailored to the company’s profile and the tone of a sales proposal.

Context:
{text}

Company Details:
{company_details}

Return 3 autocompletions starting with the last major word or phrase.
'''


prompt = ChatPromptTemplate.from_template(template)



chain = prompt | llm | StrOutputParser()


def get_recommendation(text:str , org : Optional[User]):
    result = chain.invoke({"text":text , "company_details":org}) # returns list of 3 items 
    return result
 
