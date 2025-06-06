import streamlit as st

# Initialize session state for the selected text
if 'selected_text' not in st.session_state:
    st.session_state.selected_text = ""

# Define the suggestions dictionary - key: short display, value: full content
suggestions = {
    "ML Model": "Machine Learning Model: A comprehensive framework for building predictive models using supervised and unsupervised learning algorithms. Includes data preprocessing, feature engineering, model training, validation, and deployment pipelines.",
    "Data Pipeline": "Data Analysis Pipeline: An end-to-end solution for data processing and analytics. Features data ingestion, cleaning, transformation, statistical analysis, visualization, and automated reporting capabilities.",
    "Web Framework": "Web Application Framework: A full-stack development framework for building modern web applications. Includes frontend components, backend APIs, database integration, authentication, and deployment tools."
}

st.title("Text Selection Interface")

# Create two columns - left for selection box, right for suggestions
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Selected Item")
    # Display the selected text in a text area (read-only style)
    selected_display = st.text_area(
        label="Current Selection:",
        value=st.session_state.selected_text,
        height=150,
        disabled=True,
        key="selection_display"
    )

with col2:
    st.subheader("Available Options")
    
    # Create suggestion boxes with + buttons
    for i, suggestion in enumerate(suggestions):
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
                        background-color: #F8F9FA;
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
                    st.session_state.selected_text = suggestions[suggestion]
                    st.rerun()

# Add some spacing
st.markdown("---")

# Optional: Add a clear button to reset selection
if st.button("🗑️ Clear Selection", help="Clear the current selection"):
    st.session_state.selected_text = ""
    st.rerun()

# Display current selection status with debugging
if st.session_state.selected_text:
    st.success(f"Currently selected: {st.session_state.selected_text[:50]}..." if len(st.session_state.selected_text) > 50 else f"Currently selected: {st.session_state.selected_text}")
    # Debug: Show the full content
    with st.expander("Debug - Full selected content"):
        st.write(st.session_state.selected_text)
else:
    st.info("No item selected. Click a ➕ button to select an option.")