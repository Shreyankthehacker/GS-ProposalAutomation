from SearchAndRecommendation.websiterecommendation.url_utils import get_urls
import streamlit as st
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from SearchAndRecommendation.websiterecommendation.url_utils import get_urls
from WebScraper.scrape import get_data
from WebScraper.scrape_utils import extract_hex_colors
from SearchAndRecommendation.prompt_suggestion.recommend import get_recommendation,get_detailed_module_breakdown


from WebScraper.state import User

buyer = None
seller =None 

# ✅ Make app full-width
st.set_page_config(layout="wide", page_title="XPRT Proposal Maker")

# ✅ Optional: Improve spacing with CSS
st.markdown("""
    <style>
        .block-container {
            padding: 2rem 3rem;
        }
        .stTextInput, .stSelectbox, .stButton {
            font-size: 1rem;
        }
        .stMarkdown h3 {
            font-size: 1.4rem;
        }
        img {
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# SOLUTION 2: Thread-based approach (most reliable for Streamlit)
import asyncio
from concurrent.futures import ThreadPoolExecutor

def get_urls_threaded(company_name):
    """Run async get_urls in a thread-safe way."""
    print(f"Company url is being fetched for {company_name}")
    def run_in_thread():
        try:
            return asyncio.run(get_urls(company_name))
        except Exception as e:
            print(f"Error in get_urls: {e}")
            return None

    with ThreadPoolExecutor() as executor:
        future = executor.submit(run_in_thread)
        result = future.result()
        print(f"URLs result: {result}")
        return result if result else []

# SOLUTION 3: Using st.cache_data for performance
@st.cache_data
def get_urls_cached(company_name):
    """Cached version using threading approach"""
    return get_urls_threaded(company_name)

# SCRAPING FUNCTION - Replace with your actual scraping implementation
def scrape_website_info(url):
    def run_in_thread():
        return asyncio.run(get_data(url))

    with ThreadPoolExecutor() as executor:
        future = executor.submit(run_in_thread)
        result = future.result()
        print(result)
        return result
    
def get_time_cost_recommendations(s, buyer):
    return "Budget: $5,000 - $8,000, Timeline: 4-6 weeks, Details: Based on project complexity..."
def display_scraped_data(scraped_data, section_name):
    """Display the scraped company data in a nice format"""
    if not scraped_data:
        return
    if section_name.lower()=='buyer':
        buyer = scraped_data
    else:
        seller = scraped_data
    st.success(f"✅ {section_name} data scraped successfully!")
    
    with st.container():
        st.subheader(f"📊 {section_name} Company Details")

        # Top full-width: Company name and description
        if scraped_data.name:
            st.markdown(f"### 🏢 {scraped_data.name}")

        if scraped_data.description:
            st.markdown("**📝 Description:**")
            st.write(scraped_data.description)

        # Bottom: Two columns
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("**🏷️ Logo:**")
            if scraped_data.logo:
                try:
                    st.image(scraped_data.logo, caption="Company Logo", width=180)
                except Exception as e:
                    st.error(f"Could not load logo: {str(e)}")
                    st.write(f"Logo URL: {scraped_data.logo}")
            else:
                st.info("No logo available")

        with col2:
            st.markdown("**🛠️ Services Offered:**")
            services = scraped_data.services
            if services:
                if isinstance(services, list):
                    for service in services:
                        st.markdown(f"🔹 {service}")
                else:
                    st.write(services)

def create_company_section(section_name, section_key):
    """Create a reusable company section with URL suggestions and scraping"""
    
    st.subheader(f"{section_name} Information")
    
    # Initialize session state for this section first
    if f'{section_key}_suggested_urls' not in st.session_state:
        st.session_state[f'{section_key}_suggested_urls'] = []
    if f'{section_key}_last_company' not in st.session_state:
        st.session_state[f'{section_key}_last_company'] = ""
    if f'{section_key}_current_url' not in st.session_state:
        st.session_state[f'{section_key}_current_url'] = ""
    if f'{section_key}_scraped_data' not in st.session_state:
        st.session_state[f'{section_key}_scraped_data'] = None
    if f'{section_key}_company_name' not in st.session_state:
        st.session_state[f'{section_key}_company_name'] = ""
    if f'{section_key}_urls_fetched' not in st.session_state:
        st.session_state[f'{section_key}_urls_fetched'] = False
    if f'{section_key}_show_url_warning' not in st.session_state:
        st.session_state[f'{section_key}_show_url_warning'] = False
    
    # Company name input
    company_name = st.text_input(
        f"Enter {section_name} Company Name", 
        value=st.session_state[f'{section_key}_company_name'],
        key=f"{section_key}_name"
    )
    
    # Update session state when company name changes
    if company_name != st.session_state[f'{section_key}_company_name']:
        st.session_state[f'{section_key}_company_name'] = company_name
        # Reset URL fetching state when company name changes
        st.session_state[f'{section_key}_urls_fetched'] = False
        st.session_state[f'{section_key}_show_url_warning'] = False
        st.session_state[f'{section_key}_suggested_urls'] = []
    
    # Show "Get Suggestions" button only if company name exists and URLs haven't been fetched
    if company_name and not st.session_state[f'{section_key}_urls_fetched']:
        if st.button(f"🔍 Get Website Suggestions for {company_name}", key=f"{section_key}_fetch_btn"):
            st.session_state[f'{section_key}_urls_fetched'] = True
            
            # Show loading spinner
            with st.spinner(f"Searching for {company_name} websites..."):
                try:
                    print(f"Company name is {company_name}")
                    suggested_urls = get_urls_threaded(company_name)
                    print(f"In frontend the suggested urls are", suggested_urls)
                    
                    if suggested_urls and len(suggested_urls) > 0:
                        st.session_state[f'{section_key}_suggested_urls'] = suggested_urls
                        st.session_state[f'{section_key}_last_company'] = company_name
                        st.success(f"Found {len(suggested_urls)} website suggestions!")
                        st.session_state[f'{section_key}_show_url_warning'] = False
                    else:
                        st.session_state[f'{section_key}_suggested_urls'] = []
                        st.session_state[f'{section_key}_show_url_warning'] = True
                        st.warning(f"⚠️ No relevant websites found for {company_name}. Please enter the URL manually below.")
                        
                except Exception as e:
                    st.error(f"Error fetching URLs: {str(e)}")
                    st.session_state[f'{section_key}_suggested_urls'] = []
                    st.session_state[f'{section_key}_show_url_warning'] = True
                
                st.rerun()
    
    # Show "Search Again" button if URLs have been fetched
    if st.session_state[f'{section_key}_urls_fetched'] and company_name:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button(f"🔄 Search Again", key=f"{section_key}_refresh"):
                st.session_state[f'{section_key}_urls_fetched'] = False
                st.session_state[f'{section_key}_suggested_urls'] = []
                st.session_state[f'{section_key}_show_url_warning'] = False
                st.rerun()
    
    # URL input section
    st.write("**Company Website**")
    
    # Show dropdown only if we have successfully fetched URLs
    if (st.session_state[f'{section_key}_urls_fetched'] and 
        st.session_state[f'{section_key}_suggested_urls'] and 
        len(st.session_state[f'{section_key}_suggested_urls']) > 0):
        
        st.write("**Select from suggested URLs:**")
        
        # Create dropdown options
        dropdown_options = ["Select a URL..."] + st.session_state[f'{section_key}_suggested_urls']
        
        selected_url = st.selectbox(
            "Choose URL:",
            options=dropdown_options,
            key=f"{section_key}_url_dropdown",
            help="Select a suggested URL or enter manually below"
        )
        
        # If user selected a URL from dropdown, update the text input
        if selected_url != "Select a URL..." and selected_url != st.session_state[f'{section_key}_current_url']:
            st.session_state[f'{section_key}_current_url'] = selected_url
    
    # Show warning only if we've attempted to fetch URLs and found none
    elif st.session_state[f'{section_key}_show_url_warning']:
        st.warning(f"⚠️ Couldn't find any relevant websites for {company_name}. Please enter the URL manually below.")

    # Main text input where user can type (always visible)
    final_url = st.text_input(
        "Website URL:",
        value=st.session_state[f'{section_key}_current_url'],
        placeholder=f"Enter {section_name.lower()} company website URL (e.g., https://example.com)",
        help="Enter the complete URL including https://",
        key=f"{section_key}_url_input"
    )

    # Update session state when text input changes
    if final_url != st.session_state[f'{section_key}_current_url']:
        st.session_state[f'{section_key}_current_url'] = final_url
        
    # Display final URL and scraping section     
    if final_url:
        st.markdown(f"🔗 Final Website URL: [{final_url}]({final_url})")
                
        # Validate URL format
        if final_url.startswith(('http://', 'https://')):
            st.success("✅ Valid URL format")
                        
            # SCRAPING SECTION
            st.write("---")
    st.write("**🔍 Website Scraping**")
                        
    col1, col2 = st.columns([1, 1])
                        
    with col1:
        # Scrape button
        if st.button(f"🚀 Get {section_name} details", key=f"{section_key}_scrape_btn"):
            with st.spinner(f"Fetching {section_name} website data..."):
                try:
                    # Pass the confirmed URL to scraping function
                    scraped_data = scrape_website_info(final_url)
                    st.session_state[f'{section_key}_scraped_data'] = scraped_data
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error Fetching website: {str(e)}")
                        
    with col2:
        # Clear scraped data button
        if st.session_state[f'{section_key}_scraped_data']:
            if st.button(f"🗑️ Clear {section_name} Data", key=f"{section_key}_clear_btn"):
                st.session_state[f'{section_key}_scraped_data'] = None
                # Also clear services data when clearing scraped data
                st.session_state[f'{section_key}_selected_services'] = []
                st.session_state[f'{section_key}_additional_services'] = ""
                if f'{section_key}_final_services' in st.session_state:
                    del st.session_state[f'{section_key}_final_services']
                if f'{section_key}_services_string' in st.session_state:
                    del st.session_state[f'{section_key}_services_string']
                st.rerun()

    # Display scraped data if available
    if st.session_state[f'{section_key}_scraped_data']:
        st.write("---")
        display_scraped_data(st.session_state[f'{section_key}_scraped_data'], section_name)
                        
        # Extract services from scraped data
        scraped_data = st.session_state[f'{section_key}_scraped_data']
        services_list = []
                        
        if hasattr(scraped_data, 'services'):
            services_data = scraped_data.services  # Access as attribute, not dictionary key
            
            if isinstance(services_data, list):
                # Filter out empty strings and clean the services
                services_list = [s.strip() for s in services_data if s and s.strip()]
            elif isinstance(services_data, str) and services_data.strip():
                # Split by common delimiters if it's a string
                services_list = [s.strip() for s in services_data.replace('\n', ',').split(',') if s.strip()]

        # Fallback: If scraped_data is a dictionary (for backward compatibility)
        elif isinstance(scraped_data, dict):
            # Primary check for 'services' key
            if 'services' in scraped_data:
                services_data = scraped_data['services']
                if isinstance(services_data, list):
                    services_list = [s.strip() for s in services_data if s and s.strip()]
                elif isinstance(services_data, str) and services_data.strip():
                    services_list = [s.strip() for s in services_data.replace('\n', ',').split(',') if s.strip()]
            
            # Fallback to other possible keys if 'services' key is empty or not found
            if not services_list:
                for key in ['Services', 'services_offered', 'offerings', 'products', 'service_list']:
                    if key in scraped_data:
                        services_data = scraped_data[key]
                        if isinstance(services_data, list):
                            services_list = [s.strip() for s in services_data if s and s.strip()]
                        elif isinstance(services_data, str) and services_data.strip():
                            services_list = [s.strip() for s in services_data.replace('\n', ',').split(',') if s.strip()]
                        if services_list:
                            break
        # Services Related Selection Section
        st.write("---")
        st.write("**🛠️ Services Related**")
                        
        # Initialize session state for selected services if not exists
        if f'{section_key}_selected_services' not in st.session_state:
            st.session_state[f'{section_key}_selected_services'] = []
        
        # Initialize session state for additional services text if not exists
        if f'{section_key}_additional_services' not in st.session_state:
            st.session_state[f'{section_key}_additional_services'] = ""
                        
        # Show checkboxes for available services (if any)
        if services_list:
            st.write("**Select services from website:**")
            st.caption(f"Found {len(services_list)} services from the website")
            
            # Create a more organized layout for checkboxes if there are many services
            if len(services_list) > 6:
                # Use columns for better organization with many services
                cols = st.columns(2)
                for i, service in enumerate(services_list):
                    with cols[i % 2]:
                        is_selected = st.checkbox(
                            service,
                            value=service in st.session_state[f'{section_key}_selected_services'],
                            key=f"{section_key}_service_checkbox_{i}"
                        )
                        if is_selected and service not in st.session_state[f'{section_key}_selected_services']:
                            st.session_state[f'{section_key}_selected_services'].append(service)
                        elif not is_selected and service in st.session_state[f'{section_key}_selected_services']:
                            st.session_state[f'{section_key}_selected_services'].remove(service)
            else:
                # Single column for fewer services
                for i, service in enumerate(services_list):
                    is_selected = st.checkbox(
                        service,
                        value=service in st.session_state[f'{section_key}_selected_services'],
                        key=f"{section_key}_service_checkbox_{i}"
                    )
                    if is_selected and service not in st.session_state[f'{section_key}_selected_services']:
                        st.session_state[f'{section_key}_selected_services'].append(service)
                    elif not is_selected and service in st.session_state[f'{section_key}_selected_services']:
                        st.session_state[f'{section_key}_selected_services'].remove(service)
            
            # Show selected services summary
            if st.session_state[f'{section_key}_selected_services']:
                st.success(f"✅ Selected ({len(st.session_state[f'{section_key}_selected_services'])}): {', '.join(st.session_state[f'{section_key}_selected_services'])}")
            
            # Quick select buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✅ Select All", key=f"{section_key}_select_all"):
                    st.session_state[f'{section_key}_selected_services'] = services_list.copy()
                    st.rerun()
            with col2:
                if st.button("❌ Deselect All", key=f"{section_key}_deselect_all"):
                    st.session_state[f'{section_key}_selected_services'] = []
                    st.rerun()
        else:
            st.info("🔍 No services found in the scraped data. You can add custom services below.")
        
        # Additional services text area
        st.write("**Additional services (if any):**")
        additional_services_text = st.text_area(
            "Enter any other services related to this project:",
            value=st.session_state[f'{section_key}_additional_services'],
            height=100,
            key=f"{section_key}_additional_services_input",
            placeholder="e.g., Custom API Development, Database Design, Cloud Deployment..."
        )
        
        # Update session state for additional services
        st.session_state[f'{section_key}_additional_services'] = additional_services_text
        
        # Combined services display
        st.write("---")
        st.write("**📋 Final Services Summary:**")
        
        # Combine selected services and additional services
        all_services = []
        
        # Add selected services from checkboxes
        if st.session_state[f'{section_key}_selected_services']:
            all_services.extend(st.session_state[f'{section_key}_selected_services'])
        
        # Add additional services (split by comma and clean)
        if additional_services_text.strip():
            additional_list = [s.strip() for s in additional_services_text.replace('\n', ',').split(',') if s.strip()]
            all_services.extend(additional_list)
        
        # Remove duplicates while preserving order
        unique_services = []
        for service in all_services:
            if service not in unique_services:
                unique_services.append(service)
        
        # Display final services
        if unique_services:
            st.info(f"🎯 **Total Services ({len(unique_services)}):** {', '.join(unique_services)}")
            
            # Store combined services in session state for later use
            st.session_state[f'{section_key}_final_services'] = unique_services
            
            # Optional: Export services as comma-separated string
            st.session_state[f'{section_key}_services_string'] = ', '.join(unique_services)
            
            # Show breakdown
            with st.expander("📊 Services Breakdown"):
                if st.session_state[f'{section_key}_selected_services']:
                    st.write(f"**From Website ({len(st.session_state[f'{section_key}_selected_services'])}):** {', '.join(st.session_state[f'{section_key}_selected_services'])}")
                if additional_services_text.strip():
                    additional_count = len([s.strip() for s in additional_services_text.replace('\n', ',').split(',') if s.strip()])
                    st.write(f"**Additional ({additional_count}):** {additional_services_text}")
        else:
            st.warning("⚠️ No services selected yet.")
        
        # Clear all selections button
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🗑️ Clear Services", key=f"{section_key}_clear_services"):
                st.session_state[f'{section_key}_selected_services'] = []
                st.session_state[f'{section_key}_additional_services'] = ""
                if f'{section_key}_final_services' in st.session_state:
                    del st.session_state[f'{section_key}_final_services']
                if f'{section_key}_services_string' in st.session_state:
                    del st.session_state[f'{section_key}_services_string']
                st.rerun()                # 🎨 Display Color Palette
                try:
                    st.write("**🎨 Colors Desirable to the website and logo**")
                    colors = extract_hex_colors(st.session_state[f'{section_key}_current_url'])
                    if colors:
                        st.markdown("Here are the primary colors from the company website:")
                        color_cols = st.columns(len(colors))
                        for i, color in enumerate(colors):
                            with color_cols[i]:
                                st.markdown(
                                    f"<div style='background-color:{color}; width:100%; height:50px; border-radius:8px;'></div><p style='text-align:center;'>{color}</p>",
                                    unsafe_allow_html=True
                                )
                    else:
                        st.info("No prominent colors detected from the website.")
                except Exception as e:
                    st.warning(f"Could not extract color palette: {str(e)}")
# MAIN STREAMLIT APP
st.title("🏢 XPRT Proposal Maker")

# Create sections side by side
left_col, right_col = st.columns(2)

with left_col:
    create_company_section("Seller", "seller")

with right_col:
    create_company_section("Buyer", "buyer")

st.divider()

# # Summary section
# if st.session_state.get('seller_scraped_data') or st.session_state.get('buyer_scraped_data'):
#     st.header("📋 Summary")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         if st.session_state.get('seller_scraped_data'):
#             seller_data = st.session_state['seller_scraped_data']
#             st.subheader("📤 Seller Summary")
#             st.write(f"**Company:** {seller_data.name, 'N/A')}")
#             st.write(f"**Services:** {len(seller_data.services, []))} listed")
#         else:
#             st.info("No seller data available")
    
#     with col2:
#         if st.session_state.get('buyer_scraped_data'):
#             buyer_data = st.session_state['buyer_scraped_data']
#             st.subheader("📥 Buyer Summary")
#             st.write(f"**Company:** {buyer_data.get('name', 'N/A')}")
#             st.write(f"**Services:** {len(buyer_data.get('services', []))} listed")
#         else:
#             st.info("No buyer data available")

#---------------------------------------------

st.subheader("Client Requirement")

# Create two columns
left_col, right_col = st.columns(2)

# Session state for client requirement and recommendation (kept separate)
if "client_requirement" not in st.session_state:
    st.session_state.client_requirement = ""
if "time_cost_recommendation" not in st.session_state:
    st.session_state.time_cost_recommendation = ""

# LEFT: Client requirement input only
with left_col:
    st.session_state.client_requirement = st.text_area(
        "Project Description or Client Requirements",
        value=st.session_state.client_requirement,
        height=250,
        key="client_req_input",
        placeholder="Enter the client's project requirements, objectives, and specifications here..."
    )

# RIGHT: Time & Cost Recommendations (separate from client requirements)
with right_col:
    # Buttons for generating recommendations
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("Get Recommendation"):
            if st.session_state.client_requirement.strip():
                # Generate recommendation based on client requirements
                st.session_state.time_cost_recommendation = get_time_cost_recommendations(
                    st.session_state.client_requirement, buyer
                )
            else:
                st.warning("Please enter client requirements first")
    
    with col2:
        if st.button("🔄 Re-get"):
            if st.session_state.client_requirement.strip():
                # Re-generate recommendation
                st.session_state.time_cost_recommendation = get_time_cost_recommendations(
                    st.session_state.client_requirement, buyer
                )
            else:
                st.warning("Please enter client requirements first")
    
    # Display recommendation in a separate box (not mixed with requirements)
    if st.session_state.time_cost_recommendation:
        st.subheader("📅💰 Time & Cost Recommendation")
        
        # Display the recommendation in a styled box
        st.markdown(
            f"""
            <div style="
                border: 2px solid #4CAF50;
                padding: 15px;
                border-radius: 10px;
                background-color: #f9f9f9;
                margin-top: 10px;
            ">
                <h4 style="color: #2E7D32; margin-top: 0;">Recommended Timeline & Budget</h4>
                <div style="color: #333; line-height: 1.6;">
                    {st.session_state.time_cost_recommendation}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Optional: Add button to copy recommendation to proposal
        if st.button("📋 Use This Recommendation", key="use_recommendation"):
            st.success("Recommendation ready to be included in your proposal!")
            # You can add logic here to pass this to your proposal generation

# Session state for detailed breakdown
if "detailed_breakdown" not in st.session_state:
    st.session_state.detailed_breakdown = ""

# BOTTOM: Detailed Module Breakdown (full width)
st.subheader("🔧 Detailed Module Breakdown")

# Button to generate breakdown
col1, col2, col3 = st.columns([2, 2, 6])

with col1:
    if st.button("📊 Generate Breakdown"):
        if st.session_state.client_requirement.strip() and st.session_state.time_cost_recommendation.strip():
            # Generate detailed breakdown
            st.session_state.detailed_breakdown = get_detailed_module_breakdown(
                st.session_state.client_requirement,
                st.session_state.time_cost_recommendation,
                buyer
            )
        else:
            st.warning("Please enter requirements and get recommendations first")

with col2:
    if st.button("🔄 Re-generate"):
        if st.session_state.client_requirement.strip() and st.session_state.time_cost_recommendation.strip():
            # Re-generate breakdown
            st.session_state.detailed_breakdown = get_detailed_module_breakdown(
                st.session_state.client_requirement,
                st.session_state.time_cost_recommendation,
                buyer
            )
        else:
            st.warning("Please enter requirements and get recommendations first")

# Display detailed breakdown
if st.session_state.detailed_breakdown:
    st.markdown(
        f"""
        <div style="
            border: 2px solid #FF9800;
            padding: 20px;
            border-radius: 12px;
            background-color: #fff8e1;
            margin-top: 15px;
        ">
            <h4 style="color: #E65100; margin-top: 0;">📋 Project Module Breakdown & Cost Analysis</h4>
            <div style="color: #333; line-height: 1.6; font-family: 'Courier New', monospace;">
                {st.session_state.detailed_breakdown}

        """,
        unsafe_allow_html=True
    )# Debug section
if st.checkbox("Show debug info"):
    st.write("**Debug Information:**")
    
    # Seller info
    st.write("**Seller:**")
    st.write(f"Company: {st.session_state.get('seller_company_name', 'N/A')}")
    st.write(f"URLs Fetched: {st.session_state.get('seller_urls_fetched', False)}")
    st.write(f"Show Warning: {st.session_state.get('seller_show_url_warning', False)}")
    st.write(f"Suggested URLs: {st.session_state.get('seller_suggested_urls', [])}")
    st.write(f"Final URL: {st.session_state.get('seller_current_url', 'N/A')}")
    st.write(f"Scraped Data: {'Available' if st.session_state.get('seller_scraped_data') else 'None'}")
    
    # Buyer info
    st.write("**Buyer:**")
    st.write(f"Company: {st.session_state.get('buyer_company_name', 'N/A')}")
    st.write(f"URLs Fetched: {st.session_state.get('buyer_urls_fetched', False)}")
    st.write(f"Show Warning: {st.session_state.get('buyer_show_url_warning', False)}")
    st.write(f"Suggested URLs: {st.session_state.get('buyer_suggested_urls', [])}")
    st.write(f"Final URL: {st.session_state.get('buyer_current_url', 'N/A')}")
    st.write(f"Scraped Data: {'Available' if st.session_state.get('buyer_scraped_data') else 'None'}")