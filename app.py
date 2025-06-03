
from SearchAndRecommendation.url_recommendation.url_utils import get_urls_from_company_name
import streamlit as st
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from SearchAndRecommendation.url_recommendation.url_utils import get_urls_from_company_name
from WebScraper.scrape import get_data
from WebScraper.scrape_utils import extract_hex_colors

# ✅ Make app full-width
st.set_page_config(layout="wide", page_title="Company Info Scraper")

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





def display_scraped_data(scraped_data, section_name):
    """Display the scraped company data in a nice format"""
    if not scraped_data:
        return
    
    st.success(f"✅ {section_name} data scraped successfully!")
    
    # Create a nice container for the scraped data
    with st.container():
        st.subheader(f"📊 {section_name} Company Details")
        
        # Create two columns for layout
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Display logo
            if scraped_data.get('logo'):
                try:
                    st.image(scraped_data['logo'], caption=f"{section_name} Logo", width=200)
                except Exception as e:
                    st.error(f"Could not load logo: {str(e)}")
                    st.write(f"Logo URL: {scraped_data['logo']}")
            else:
                st.info("No logo available")
        
        with col2:
            # Display company name
            if scraped_data.get('name'):
                st.markdown(f"### 🏢 {scraped_data['name']}")
            
            # Display description
            if scraped_data.get('description'):
                st.markdown("**📝 Description:**")
                st.write(scraped_data['description'])
        
        # Display services in full width
        if scraped_data.get('services'):
            st.markdown("**🛠️ Services Offered:**")
            
            # Display services as badges
            services = scraped_data['services']
            if isinstance(services, list):
                # Create columns for services (3 per row)
                service_cols = st.columns(3)
                for i, service in enumerate(services):
                    col_idx = i % 3
                    with service_cols[col_idx]:
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
    if f'{section_key}_is_fetching' not in st.session_state:
        st.session_state[f'{section_key}_is_fetching'] = False
    
    # Company name input - preserve value during fetching
    company_name = st.text_input(
        f"Enter {section_name} Company Name", 
        value=st.session_state[f'{section_key}_company_name'],
        key=f"{section_key}_name"
    )
    
    # Update session state when company name changes
    if company_name != st.session_state[f'{section_key}_company_name']:
        st.session_state[f'{section_key}_company_name'] = company_name
    
    # Fetch URLs when company name changes and is not empty
    if (company_name and 
        company_name != st.session_state[f'{section_key}_last_company'] and 
        not st.session_state[f'{section_key}_is_fetching']):
        
        st.write(f"Fetching suggestions for: **{company_name}**")
        
        # Set fetching state
        st.session_state[f'{section_key}_is_fetching'] = True
        
        # Show loading spinner
        with st.spinner("Getting URL suggestions..."):
            try:
                print(f"Company name is {company_name}")
                # Use the threaded approach (most reliable)
                suggested_urls =asyncio.run(get_urls_from_company_name(company_name))
                print(f"In frontend the suggested urls are",suggested_urls)
                st.session_state[f'{section_key}_suggested_urls'] = suggested_urls
                st.session_state[f'{section_key}_last_company'] = company_name
                st.success("URLs fetched successfully!")
            except Exception as e:
                st.error(f"Error fetching URLs: {str(e)}")
                st.session_state[f'{section_key}_suggested_urls'] = []
            finally:
                # Reset fetching state
                st.session_state[f'{section_key}_is_fetching'] = False
                st.rerun()
    
    # URL input section
    st.write("**Company Website**")
    
    # Show dropdown if we have suggested URLs
    if st.session_state[f'{section_key}_suggested_urls']:
        st.write("**Select from suggested URLs:**")
        
        # Create dropdown options
        dropdown_options = ["Select a URL..."] + st.session_state[f'{section_key}_suggested_urls']
        
        selected_url = st.selectbox(
            "Choose URL:",
            options=dropdown_options,
            key=f"{section_key}_url_dropdown",
            help="Select a suggested URL or choose 'Select a URL...' to enter manually"
        )
        
        # If user selected a URL from dropdown, update the text input
        if selected_url != "Select a URL..." and selected_url != st.session_state[f'{section_key}_current_url']:
            st.session_state[f'{section_key}_current_url'] = selected_url
    
    # Main text input where user can type (always visible)
    final_url = st.text_input(
        "Website URL:",
        value=st.session_state[f'{section_key}_current_url'],
        placeholder=f"Enter {section_name.lower()} company website URL or select from dropdown above...",
        help="Type your URL directly or select from the dropdown suggestions above",
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
                if st.button(f"🚀 Scrape {section_name} Website", key=f"{section_key}_scrape_btn"):
                    with st.spinner(f"Scraping {section_name} website data..."):
                        try:
                            # Pass the confirmed URL to scraping function
                            scraped_data = asyncio.run(get_data(final_url))
                            st.session_state[f'{section_key}_scraped_data'] = scraped_data
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error scraping website: {str(e)}")
            
            with col2:
                # Clear scraped data button
                if st.session_state[f'{section_key}_scraped_data']:
                    if st.button(f"🗑️ Clear {section_name} Data", key=f"{section_key}_clear_btn"):
                        st.session_state[f'{section_key}_scraped_data'] = None
                        st.rerun()
        else:
            st.warning("⚠️ URL should start with http:// or https://")
    
    # Display scraped data if available
    if st.session_state[f'{section_key}_scraped_data']:
        st.write("---")
        display_scraped_data(st.session_state[f'{section_key}_scraped_data'], section_name)
            # 🎨 Display Color Palette
    try:
        st.write("**🎨 Extracted Color Palette**")
        colors = extract_hex_colors(st.session_state[f'{section_key}_current_url'])  # Implement this function
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

    # Manual refresh button for URL suggestions
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button(f"🔄 Refresh {section_name} URL Suggestions", key=f"{section_key}_refresh"):
            if company_name:
                st.session_state[f'{section_key}_is_fetching'] = True
                with st.spinner("Fetching fresh suggestions..."):
                    try:
                        # Clear cache and fetch new results
                        #get_urls_from_company_name_cached.clear()
                        urls = get_urls_from_company_name(company_name)
                        st.session_state[f'{section_key}_suggested_urls'] = urls
                        st.session_state[f'{section_key}_last_company'] = company_name
                        st.success("Fresh suggestions loaded!")
                    except Exception as e:
                        st.error(f"Error fetching URLs: {str(e)}")
                    finally:
                        st.session_state[f'{section_key}_is_fetching'] = False
                        st.rerun()
            else:
                st.warning(f"Please enter a {section_name.lower()} company name first")
    
    with col2:
        # Clear suggestions button
        if st.session_state[f'{section_key}_suggested_urls']:
            if st.button(f"🗑️ Clear {section_name} Suggestions", key=f"{section_key}_clear_suggestions"):
                st.session_state[f'{section_key}_suggested_urls'] = []
                st.session_state[f'{section_key}_last_company'] = ""
                st.rerun()

# MAIN STREAMLIT APP
st.title("🏢 Company Info Intake & Scraper")

# Create sections
# Create sections side by side
left_col, right_col = st.columns(2)

with left_col:
    create_company_section("Seller", "seller")

with right_col:
    create_company_section("Buyer", "buyer")

st.divider()

# Summary section
if st.session_state.get('seller_scraped_data') or st.session_state.get('buyer_scraped_data'):
    st.header("📋 Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.get('seller_scraped_data'):
            seller_data = st.session_state['seller_scraped_data']
            st.subheader("📤 Seller Summary")
            st.write(f"**Company:** {seller_data.get('name', 'N/A')}")
            st.write(f"**Services:** {len(seller_data.get('services', []))} listed")
        else:
            st.info("No seller data available")
    
    with col2:
        if st.session_state.get('buyer_scraped_data'):
            buyer_data = st.session_state['buyer_scraped_data']
            st.subheader("📥 Buyer Summary")
            st.write(f"**Company:** {buyer_data.get('name', 'N/A')}")
            st.write(f"**Services:** {len(buyer_data.get('services', []))} listed")
        else:
            st.info("No buyer data available")

# Debug section
if st.checkbox("Show debug info"):
    st.write("**Debug Information:**")
    
    # Seller info
    st.write("**Seller:**")
    st.write(f"Company: {st.session_state.get('seller_company_name', 'N/A')}")
    st.write(f"Last Company: {st.session_state.get('seller_last_company', 'N/A')}")
    st.write(f"Is Fetching: {st.session_state.get('seller_is_fetching', False)}")
    st.write(f"Suggested URLs: {st.session_state.get('seller_suggested_urls', [])}")
    st.write(f"Final URL: {st.session_state.get('seller_current_url', 'N/A')}")
    st.write(f"Scraped Data: {'Available' if st.session_state.get('seller_scraped_data') else 'None'}")
    
    # Buyer info
    st.write("**Buyer:**")
    st.write(f"Company: {st.session_state.get('buyer_company_name', 'N/A')}")
    st.write(f"Last Company: {st.session_state.get('buyer_last_company', 'N/A')}")
    st.write(f"Is Fetching: {st.session_state.get('buyer_is_fetching', False)}")
    st.write(f"Suggested URLs: {st.session_state.get('buyer_suggested_urls', [])}")
    st.write(f"Final URL: {st.session_state.get('buyer_current_url', 'N/A')}")
    st.write(f"Scraped Data: {'Available' if st.session_state.get('buyer_scraped_data') else 'None'}")