from SearchAndRecommendation.prompt_suggestion.prompts import template,time_template
from SearchAndRecommendation.prompt_suggestion.llm import llm

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser




prompt = ChatPromptTemplate.from_template(template)

time_prompt = ChatPromptTemplate.from_template(time_template)

chain = prompt | llm | StrOutputParser()

time_chain = time_prompt | llm | StrOutputParser()
