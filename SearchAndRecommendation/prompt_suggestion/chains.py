from prompts import template
from llm import llm

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser




prompt = ChatPromptTemplate.from_template(template)



chain = prompt | llm | StrOutputParser()
