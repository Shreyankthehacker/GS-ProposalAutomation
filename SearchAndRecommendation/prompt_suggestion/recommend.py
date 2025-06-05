
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
 

def get_detailed_module_breakdown(client_requirement, time_cost_recommendation, buyer_info):
    """
    Generate detailed module breakdown with mathematical cost and time distribution
    
    Args:
        client_requirement (str): The client's project requirements
        time_cost_recommendation (str): The generated time and cost recommendation
        buyer_info: Buyer information object
    
    Returns:
        str: Formatted string with detailed breakdown including:
             - Project modules/phases
             - Time allocation per module (with percentages)
             - Cost breakdown per module (with calculations)
             - Resource allocation
             - Risk factors and contingency
    """
    
    # TODO: Implement AI helper logic here
    # This function should:
    # 1. Parse the client requirements to identify key modules/components
    # 2. Extract total time and cost from time_cost_recommendation
    # 3. Break down the project into logical modules (e.g., Planning, Development, Testing, Deployment)
    # 4. Distribute time and cost with mathematical ratios
    # 5. Show calculations and reasoning
    
    # Example return format (replace with your AI generation):
    breakdown_example = """
    <b>🎯 PROJECT MODULE ANALYSIS</b><br><br>
    
    <b>📊 TOTAL PROJECT SCOPE:</b><br>
    • Total Timeline: 12 weeks<br>
    • Total Budget: $15,000<br>
    • Hourly Rate: $75/hour<br>
    • Total Hours: 200 hours<br><br>
    
    <b>🔧 MODULE BREAKDOWN:</b><br><br>
    
    <b>1. Planning & Analysis (15% - 3 weeks)</b><br>
    • Time: 30 hours (15% of 200h)<br>
    • Cost: $2,250 (30h × $75/h)<br>
    • Activities: Requirements gathering, wireframing, technical specs<br><br>
    
    <b>2. UI/UX Design (20% - 2.4 weeks)</b><br>
    • Time: 40 hours (20% of 200h)<br>
    • Cost: $3,000 (40h × $75/h)<br>
    • Activities: Design mockups, user experience flow, prototyping<br><br>
    
    <b>3. Core Development (45% - 5.4 weeks)</b><br>
    • Time: 90 hours (45% of 200h)<br>
    • Cost: $6,750 (90h × $75/h)<br>
    • Activities: Backend development, frontend implementation, integrations<br><br>
    
    <b>4. Testing & QA (10% - 1.2 weeks)</b><br>
    • Time: 20 hours (10% of 200h)<br>
    • Cost: $1,500 (20h × $75/h)<br>
    • Activities: Unit testing, integration testing, bug fixes<br><br>
    
    <b>5. Deployment & Launch (10% - 1.2 weeks)</b><br>
    • Time: 20 hours (10% of 200h)<br>
    • Cost: $1,500 (20h × $75/h)<br>
    • Activities: Server setup, deployment, go-live support<br><br>
    
    <b>💰 COST VERIFICATION:</b><br>
    Planning: $2,250 + Design: $3,000 + Development: $6,750 + Testing: $1,500 + Deployment: $1,500 = <b>$15,000 ✓</b><br><br>
    
    <b>⏱️ TIME VERIFICATION:</b><br>
    30h + 40h + 90h + 20h + 20h = <b>200 hours ✓</b><br><br>
    
    <b>📈 RISK FACTORS:</b><br>
    • Recommended 10% contingency buffer (+$1,500)<br>
    • Complex integrations may require additional 15-20 hours<br>
    • Client feedback cycles could extend timeline by 1-2 weeks
    """
    
    # Replace this with your AI-generated breakdown
    return breakdown_example


# Example usage in your Streamlit app:
# breakdown = get_detailed_module_breakdown(
#     st.session_state.client_requirement,
#     st.session_state.time_cost_recommendation,
#     buyer
# )