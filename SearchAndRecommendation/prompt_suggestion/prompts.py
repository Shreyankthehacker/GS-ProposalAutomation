template = """
You are a proposal writing assistant.

Given the client requirements, generate 3 strategic recommendations with short summaries and detailed breakdowns, focusing on:
1. Core services or offerings to highlight
2. Pain points to address
3. Goals to support or accomplish

Return your output as a valid Python dictionary where:
- Each key is a short summary (title-style sentence).
- Each value is a multiline string with 5–6 bullet points explaining how to implement/support that item in the sales proposal.

Buyer Details :
{buyer}

Seller Details :
{seller}
"""
