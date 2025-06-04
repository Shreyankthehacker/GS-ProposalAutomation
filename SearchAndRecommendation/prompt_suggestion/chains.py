from SearchAndRecommendation.prompt_suggestion.prompts import template
from SearchAndRecommendation.prompt_suggestion.llm import llm

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser




prompt = ChatPromptTemplate.from_template(template)



chain = prompt | llm | StrOutputParser()
