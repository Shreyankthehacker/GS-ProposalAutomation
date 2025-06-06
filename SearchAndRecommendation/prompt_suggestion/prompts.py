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


time_template = '''You are a senior project planner and estimator.

Given the following:

- 📄 **Project Specification & Requirements**:
{project_specifications}

- 🧑‍💼 **Buyer Details**:
{buyer_details}

- 🏢 **Seller (Service Provider) Details**:
{seller_details}

Your task is to suggest **three project timeline recommendations**:

1. ⏱️ Aggressive Timeline  
2. ⚖️ Balanced Timeline  
3. 🧘 Relaxed Timeline

Each must include:
- Total Duration (in days)
- Total Estimated Cost (in USD)
- Suggested Team Size (number of people)

Return the result as a **Python dictionary** formatted exactly like:

```python
{
  "5 days 3000$ and team of 20 people": """ 
  • Phase 1: Planning (1 day)
    - Team: 2 Project Managers
    - Tasks: Define scope, stakeholder alignment
    - Cost: $500

  • Phase 2: Development (2 days)
    - Team: 10 Developers, 3 Designers
    - Tasks: Build UI, backend APIs
    - Cost: $1800

  • Phase 3: Testing & QA (1 day)
    - Team: 3 QA Engineers
    - Tasks: Functional testing, bug fixes
    - Cost: $400

  • Phase 4: Deployment (1 day)
    - Team: 2 DevOps
    - Tasks: Setup production, monitoring
    - Cost: $300
  """,

  "10 days 5000$ and team of 10 people": """ 
  • Phase 1: ...
  """,

  "15 days 6000$ and team of 6 people": """ 
  • Phase 1: ...
  """
}
'''