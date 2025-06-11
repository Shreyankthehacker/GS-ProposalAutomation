from SearchAndRecommendation.websiterecommendation.url_utils import get_urls
import streamlit as st
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from SearchAndRecommendation.websiterecommendation.url_utils import get_urls
from WebScraper.scrape import get_data
from WebScraper.scrape_utils import extract_hex_colors
from SearchAndRecommendation.prompt_suggestion.recommend import get_recommendation,get_project_specification
from WebScraper.state import User
from PresesntationWriting.src.main import get_presentation
import os 

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
    global buyer, seller
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
    if f'{section_key}_final_url' not in st.session_state:
        st.session_state[f'{section_key}_final_url'] = ""
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

    # URL input section with 2-column layout
    st.write("**Company Website**")

    # Create two columns for URL input
    url_col1, url_col2 = st.columns([3, 2])

    with url_col1:
        # Show warning only if we've attempted to fetch URLs and found none
        if st.session_state[f'{section_key}_show_url_warning']:
            st.warning(f"⚠️ Couldn't find websites for {company_name}. Enter URL manually:")
        
        # Show dropdown if we have successfully fetched URLs
        if (st.session_state[f'{section_key}_urls_fetched'] and 
            st.session_state[f'{section_key}_suggested_urls'] and 
            len(st.session_state[f'{section_key}_suggested_urls']) > 0):
            
            st.write("**Select or Enter URL:**")
            
            # Create dropdown options with manual entry option
            dropdown_options = ["Type URL manually..."] + st.session_state[f'{section_key}_suggested_urls']
            
            selected_option = st.selectbox(
               '',
                options=dropdown_options,
                key=f"{section_key}_url_dropdown",
                help="Select a suggested URL or choose 'Type URL manually' to enter your own"
            )
            
            # If user selected a suggested URL, update the final URL
            if selected_option != "Type URL manually..." and selected_option in st.session_state[f'{section_key}_suggested_urls']:
                st.session_state[f'{section_key}_final_url'] = selected_option
            
            # Show text input only if "Type URL manually" is selected or no selection made
            if selected_option == "Type URL manually...":
                manual_url = st.text_input(
                    "Enter URL:",
                    value=st.session_state[f'{section_key}_final_url'] if selected_option == "Type URL manually..." else "",
                    placeholder=f"https://example.com",
                    key=f"{section_key}_manual_url_input"
                )
                if manual_url:
                    st.session_state[f'{section_key}_final_url'] = manual_url
        
        else:
            # Show only text input if no suggestions available
            st.write("**Enter Website URL:**")
            manual_url = st.text_input(
                "Website URL:",
                value=st.session_state[f'{section_key}_final_url'],
                placeholder=f"Enter {section_name.lower()} company website URL (e.g., https://example.com)",
                help="Enter the complete URL including https://",
                key=f"{section_key}_direct_url_input"
            )
            
            if manual_url != st.session_state[f'{section_key}_final_url']:
                st.session_state[f'{section_key}_final_url'] = manual_url

    with url_col2:
        # Display final URL in right column
        if st.session_state[f'{section_key}_final_url']:
            st.write("**Final Website URL:**")
            final_url = st.session_state[f'{section_key}_final_url']
            st.markdown(f"🔗 [{final_url}]({final_url})")
            
            # Validate URL format
            if final_url.startswith(('http://', 'https://')):
                st.success("✅ Valid URL")
            else:
                st.error("❌ Invalid URL format")
        else:
            st.write("**Final Website URL:**")
            st.info("No URL selected yet")

    # Continue with scraping section if valid URL exists
    if (st.session_state[f'{section_key}_final_url'] and 
        st.session_state[f'{section_key}_final_url'].startswith(('http://', 'https://'))):
            
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

# Initialize session state
if "client_requirement" not in st.session_state:
    st.session_state.client_requirement = ""
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []
if "suggestion_details" not in st.session_state:
    st.session_state.suggestion_details = {}
if "temp_suggestion" not in st.session_state:
    st.session_state.temp_suggestion = ""
if "suggestions_generated" not in st.session_state:
    st.session_state.suggestions_generated = False
if "added_suggestions" not in st.session_state:
    st.session_state.added_suggestions = set()  # Track added suggestions

# LEFT: Text area for client requirements
with left_col:
    st.session_state.client_requirement = st.text_area(
        "Project Description or Client Requirements",
        value=st.session_state.client_requirement,
        height=250,
        key="client_req_input",
        placeholder="Enter the client's project requirements, objectives, and specifications here..."
    )

# RIGHT: Suggestions and Autocomplete
with right_col:
    if st.button("🔮 Generate Suggestions"):
        try:
            with st.spinner("Generating suggestions..."):
                # Store the dictionary in session state
                st.session_state.suggestion_details = get_recommendation(
                    st.session_state.client_requirement, buyer, seller
                )
                st.session_state.suggestions = list(st.session_state.suggestion_details.keys())
                st.session_state.temp_suggestion = ""  # Reset selection
                st.session_state.suggestions_generated = True
                st.session_state.added_suggestions = set()  # Reset added suggestions
                st.success("Suggestions generated successfully!")
        except Exception as e:
            st.error(f"Error generating suggestions: {str(e)}")
    
    # Only display suggestions if they have been generated
    if st.session_state.suggestions_generated and st.session_state.suggestions:
        # Display suggestions using streamlit components
        for i, suggestion in enumerate(st.session_state.suggestions):
            is_added = suggestion in st.session_state.added_suggestions
            
            col1, col2 = st.columns([1, 9])
            
            with col1:
                # Change button appearance based on whether it's already added
                if is_added:
                    st.button("✅", key=f"added_{i}", disabled=True, help="Already added")
                else:
                    if st.button("➕", key=f"add_{i}", help="Add to requirements"):
                        # Get detailed description from session state dictionary
                        detailed_description = st.session_state.suggestion_details.get(
                            suggestion, f"• {suggestion}"
                        )
                        
                        if st.session_state.client_requirement.strip():
                            st.session_state.client_requirement += f"\n{detailed_description}"
                        else:
                            st.session_state.client_requirement = detailed_description
                        
                        # Mark this suggestion as added
                        st.session_state.added_suggestions.add(suggestion)
                        st.session_state.temp_suggestion = suggestion
                        st.rerun()
            
            with col2:
                # Use different styling for added suggestions
                if is_added:
                    st.success(f"✅ {suggestion} (Added)")
                else:
                    st.write(f"💡 {suggestion}")
        
        # Clear and Refresh buttons
        st.write("")  # Add some space
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🗑️ Clear"):
                st.session_state.suggestions = []
                st.session_state.suggestion_details = {}
                st.session_state.temp_suggestion = ""
                st.session_state.suggestions_generated = False
                st.session_state.added_suggestions = set()  # Clear added suggestions
                st.rerun()
        with col2:
            if st.button("🔄 Refresh"):
                try:
                    with st.spinner("Refreshing suggestions..."):
                        # Generate new suggestions using the same function
                        st.session_state.suggestion_details = get_recommendation(
                            st.session_state.client_requirement, buyer, seller
                        )
                        st.session_state.suggestions = list(st.session_state.suggestion_details.keys())
                        st.session_state.temp_suggestion = ""
                        st.session_state.added_suggestions = set()  # Reset added suggestions
                        st.success("Suggestions refreshed!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error refreshing suggestions: {str(e)}")
    
    elif st.session_state.suggestions_generated and not st.session_state.suggestions:
        st.warning("No suggestions found. Try modifying your requirements or check if buyer/seller data is available.")
    
    elif not st.session_state.suggestions_generated:
        st.info("👆 Click 'Generate Suggestions' to get AI-powered recommendations for your project requirements.")
#------------------------------------------------------
# Project specification box  
# Initialize session state for the selected text
if 'selected_text' not in st.session_state:
    st.session_state.selected_text = ""

# Initialize session state for suggestions
if 'timeline_suggestions' not in st.session_state:
    st.session_state.timeline_suggestions = {}

st.title("Project specifications")

# Create two columns with equal width - left for selection box, right for suggestions
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Selected Item")
    # Display the selected text in a text area (read-only style)
    selected_display = st.text_area(
        label="Current Selection:",
        value=st.session_state.selected_text,
        height=250,
        disabled=True,
        key="selection_display"
    )

with col2:
    st.subheader("")  # Empty subheader to match the vertical spacing of col1
    
    # Center the button
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        # Button to generate timeline suggestions
        if st.button("🔮 Get Timeline Suggestions"):
            try:
                with st.spinner("Generating timeline suggestions..."):
                    # Only call the function when button is clicked
                    st.session_state.timeline_suggestions = get_project_specification(
                        st.session_state.client_requirement, 
                        buyer, 
                        seller
                    )
                    st.success("Timeline suggestions generated!")
            except Exception as e:
                st.error(f"Error generating suggestions: {str(e)}")
    
    # Show notification right under the button
    if not st.session_state.timeline_suggestions:
        st.info("👆 Click 'Get Timeline Suggestions' to generate project specifications based on your requirements.")
    
    # Only show suggestions if they exist
    if st.session_state.timeline_suggestions:
        st.subheader("Available Options")
        
        # Create suggestion boxes with + buttons
        for i, suggestion in enumerate(st.session_state.timeline_suggestions):
            # Create a container for each suggestion
            suggestion_container = st.container()
            
            with suggestion_container:
                # Create columns for the suggestion text and + button
                text_col, button_col = st.columns([4, 1])
                
                with text_col:
                    # Display suggestion in a styled box
                    st.markdown(
                        f"""
                        <div style="
                            border: 2px solid #E0E0E0;
                            border-radius: 8px;
                            padding: 12px;
                            margin: 5px 0;
                            font-size: 14px;
                        ">
                            {suggestion}
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                
                with button_col:
                    # + button for each suggestion
                    if st.button("➕", key=f"add_btn_{i}", help=f"Add '{suggestion}' to selection"):
                        print(suggestion)
                        st.session_state.selected_text = st.session_state.timeline_suggestions[suggestion]
                        st.rerun()

# Move these outside the loop and button - they should always be visible
if st.session_state.timeline_suggestions:
    # Add some spacing
    st.markdown("---")
    
    # Center the action buttons
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        # Create columns for action buttons
        button_col1, button_col2 = st.columns([1, 1])
        
        with button_col1:
            # Clear selection button
            if st.button("🗑️ Clear Selection", help="Clear the current selection"):
                st.session_state.selected_text = ""
                st.rerun()
        
        with button_col2:
            # Clear all suggestions button
            if st.button("🗑️ Clear All Suggestions", help="Clear all timeline suggestions"):
                st.session_state.timeline_suggestions = {}
                st.session_state.selected_text = ""
                st.rerun()

    # Display current selection status
    if st.session_state.selected_text:
        st.success(f"Currently selected: {st.session_state.selected_text[:50]}..." if len(st.session_state.selected_text) > 50 else f"Currently selected: {st.session_state.selected_text}")
        # Debug: Show the full content
        with st.expander("Debug - Full selected content"):
            st.write(st.session_state.selected_text)
    else:
        st.info("No item selected. Click a ➕ button to select an option.")



# Enhanced Report Generation Section
import streamlit as st
import os
import time

# Custom CSS for better styling
st.markdown("""
<style>
    .report-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        color: white;
    }
    
    .report-title {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .generate-btn {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        width: 100%;
        margin: 1rem 0;
    }
    
    .generate-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .download-section {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .success-message {
        background: linear-gradient(45deg, #56ab2f, #a8e6cf);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
        animation: fadeIn 0.5s ease-in;
    }
    
    .error-message {
        background: linear-gradient(45deg, #ff416c, #ff4b2b);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
        animation: shake 0.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3498db;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .btn-container {
        display: flex;
        gap: 10px;
        margin-top: 1rem;
    }
    
    .download-btn {
        flex: 1;
        padding: 12px 20px;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        text-decoration: none;
        text-align: center;
        display: inline-block;
    }
    
    .pdf-btn {
        background: linear-gradient(45deg, #e74c3c, #c0392b);
        color: white;
    }
    
    .html-btn {
        background: linear-gradient(45deg, #3498db, #2980b9);
        color: white;
    }
    
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Main Report Generation Container
st.markdown('<div class="report-container">', unsafe_allow_html=True)
st.markdown('<div class="report-title">📊 AI-Powered Report Generation</div>', unsafe_allow_html=True)

# Report generation button with enhanced styling
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Generate Comprehensive Report", key="generate_report", help="Click to generate your customized business report"):
        # Show loading state
        with st.spinner(""):
            st.markdown('<div class="loading-spinner"></div>', unsafe_allow_html=True)
            st.markdown("**🔄 Generating your report... Please wait**", unsafe_allow_html=True)
            
            # Debug information
            print(type(buyer))
            
            # Generate the report
            result = get_presentation(
                buyer=buyer,
                seller=seller,
                client_requirement=st.session_state.client_requirement,
                service_dept=','.join(st.session_state.get('seller_final_services', [])),
                additonal_info=[st.session_state.get('selected_text', '')]
            )
            
            # Clear loading state
            st.empty()
            
            # Check if report generation was successful
            if result:
                st.markdown("""
                <div class="success-message">
                    ✅ Report Generated Successfully!
                    <br>Your comprehensive business report is ready for download.
                </div>
                """, unsafe_allow_html=True)
                
                # File paths
                html_path = '/home/shreyank/Gen-ai/Growth/professional_proposal.pdf'
                pdf_path = '/home/shreyank/Gen-ai/Growth/professional_proposal.pdf'
                
                # Download section with enhanced styling
                st.markdown('<div class="download-section">', unsafe_allow_html=True)
                st.markdown("### 📥 Download Options")
                
                # Create columns for download buttons
                download_col1, download_col2 = st.columns(2)
                
                # PDF Download
                with download_col1:
                    if os.path.isfile(pdf_path):
                        with open(pdf_path, 'rb') as f:
                            pdf_data = f.read()
                            st.download_button(
                                label="📄 Download PDF Report",
                                data=pdf_data,
                                file_name=f"business_report_{time.strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime='application/pdf',
                                help="Download the report as a PDF file",
                                use_container_width=True
                            )
                        st.success(f"📊 PDF Size: {len(pdf_data)/1024:.1f} KB")
                    else:
                        st.warning("⚠️ PDF file not found")
                
                # HTML Preview
                with download_col2:
                    if os.path.isfile(html_path):
                        # Create a better HTML preview button
                        st.markdown(f"""
                        <div style="text-align: center;">
                            <a href="file://{html_path}" target="_blank" style="text-decoration: none;">
                                <button class="download-btn html-btn" style="width: 100%; margin-bottom: 10px;">
                                    🔍 Preview HTML Report
                                </button>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Alternative: Show HTML content in an expander
                        with st.expander("👁️ Quick Preview", expanded=False):
                            try:
                                with open(html_path, 'r', encoding='utf-8') as f:
                                    html_content = f.read()
                                    # Display first 500 characters as preview
                                    st.code(html_content[:500] + "..." if len(html_content) > 500 else html_content, language='html')
                                st.info("💡 Click 'Preview HTML Report' button above to view the full report in a new tab")
                            except Exception as e:
                                st.error(f"Could not preview HTML: {str(e)}")
                        
                        st.success("✅ HTML file ready")
                    else:
                        st.warning("⚠️ HTML file not found")
                
                st.markdown('</div>', unsafe_allow_html=True)  # Close download-section
                
                # Additional options
                st.markdown("---")
                
                # Report statistics
                info_col1, info_col2, info_col3 = st.columns(3)
                with info_col1:
                    st.metric("📈 Report Status", "Completed", "✅")
                with info_col2:
                    st.metric("⏱️ Generated At", time.strftime('%H:%M:%S'))
                with info_col3:
                    st.metric("📅 Date", time.strftime('%Y-%m-%d'))
                
            else:
                st.markdown("""
                <div class="error-message">
                    ❌ Report Generation Failed
                    <br>Please check your inputs and try again.
                </div>
                """, unsafe_allow_html=True)
                
                # Troubleshooting tips
                with st.expander("🔧 Troubleshooting Tips", expanded=True):
                    st.markdown("""
                    **Common issues and solutions:**
                    - ✅ Ensure all required fields are filled
                    - ✅ Check your internet connection
                    - ✅ Verify file paths are accessible
                    - ✅ Try refreshing the page and generating again
                    - ✅ Contact support if the issue persists
                    """)

st.markdown('</div>', unsafe_allow_html=True)  # Close report-container

# Additional features section
st.markdown("---")
with st.expander("ℹ️ Report Features", expanded=False):
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        **📊 What's Included:**
        - Comprehensive business analysis
        - Visual charts and graphs
        - Executive summary
        - Detailed recommendations
        """)
    
    with feature_col2:
        st.markdown("""
        **🎯 Report Benefits:**
        - Professional formatting
        - Easy to share and present
        - Actionable insights
        - Customized for your needs
        """)

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