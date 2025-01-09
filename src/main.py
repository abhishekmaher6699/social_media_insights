import streamlit as st

# Page configuration - Must be the first Streamlit command
st.set_page_config(
    page_title="Social Media Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

from langflow import get_data

# Custom CSS
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Card styling */
    .stCardContainer {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    /* Metric styling */
    .metric-container {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Header styling */
    h1 {
        color: #1e3d59;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    h2 {
        color: #2d4059;
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 2rem;
    }
    
    h3 {
        color: #2d4059;
        font-size: 1.4rem;
        font-weight: 500;
    }
    
    /* Content type selection styling */
    .content-type-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    /* Custom button styling */
    .stButton>button {
        background-color: #1e3d59;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #2d4059;
        transform: translateY(-2px);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    /* Checkbox styling */
    .stCheckbox>label {
        font-size: 1.1rem;
        padding: 0.5rem;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    .stCheckbox>label:hover {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("""
    <h1>📊 Social Media Performance Dashboard</h1>
""", unsafe_allow_html=True)

# Create columns for better layout
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.markdown("### 🎯 Select Content Types")
    
    # Content type selection with custom styling
    options = {
        "Text": "📝",
        "Image": "🖼️",
        "Video": "🎥",
        "Reels": "📱",
        "Carousel": "🎠"
    }
    
    selected_options = []
    
    # Create a grid of selectbox containers
    cols = st.columns(3)
    for idx, (option, emoji) in enumerate(options.items()):
        with cols[idx % 3]:
            if st.checkbox(f"{emoji} {option}", key=option):
                selected_options.append(option)

    # Submit button with styling
    if st.button("Generate Insights 🚀", use_container_width=True):
        if selected_options:
            # Get data

            with st.spinner("Fetching data... Please wait ⏳"):
            # Get data
                response = get_data(selected_options)
                print(response)
            
            if "metrics" in response:
                st.markdown("## 📈 Performance Metrics (Average)")
                
                # Define the maximum number of columns per row
                max_columns_per_row = 3

                # Create a list of all selected metrics to display
                selected_metrics = [
                    (key, metrics)
                    for key, metrics in response["metrics"].items()
                    if key.lower() in [opt.lower() for opt in selected_options]
                ]
                
                # Group metrics into chunks of max_columns_per_row
                for i in range(0, len(selected_metrics), max_columns_per_row):
                    # Create a new row with the defined number of columns
                    row_metrics = selected_metrics[i:i + max_columns_per_row]
                    metric_cols = st.columns(len(row_metrics))
                    
                    # Display each metric in the respective column
                    for col, (key, metrics) in zip(metric_cols, row_metrics):
                        with col:
                            st.markdown(f"""
                                <h3 style="">{key.capitalize()}</h3>
                            """, unsafe_allow_html=True)
                            
                            # Loop through and display each metric
                            for metric, value in metrics.items():
                                formatted_metric = metric.replace('_', ' ').title()
                                if isinstance(value, (int, float)):
                                    st.metric(formatted_metric, f"{value:,.2f}")
                                else:
                                    st.metric(formatted_metric, value)


            # Insights Section
            if "insights" in response:
                st.markdown("## 💡 Key Insights")
                for key, insights in response["insights"].items():
                    if key.lower() in [opt.lower() for opt in selected_options]:
                        with st.expander(f"📊 {key.capitalize()} Insights", expanded=True):
                            if isinstance(insights, dict):
                                for sub_key, value in insights.items():
                                    st.info(f"**{sub_key.replace('_', ' ').title()}**: {value}")
                            else:
                                st.info(insights)

            # Comparative Analysis
            if "comparative_analysis" in response and response['comparative_analysis']:
                st.markdown("## 🔄 Comparative Analysis")
                with st.expander("View Analysis", expanded=True):
                    for key, analysis in response["comparative_analysis"].items():
                        st.warning(f"**{key.replace('_', ' ').title()}**: {analysis}")

            # Recommendations
            if "recommendations" in response:
                st.markdown("## 🎯 Recommendations to increase engagement")
                for key, recommendations in response["recommendations"].items():
                    if key.lower() in [opt.lower() for opt in selected_options]:
                        with st.expander(f"💡 {key.capitalize()} Recommendations", expanded=True):
                            if isinstance(recommendations, dict):
                                for rec, value in recommendations.items():
                                    st.success(f"**{rec.replace('_', ' ').title()}**: {value}")
                            elif isinstance(recommendations, list):
                                for rec in recommendations:
                                    st.success(rec)
                            else:
                                st.success(recommendations)
        else:
            st.error("🚨 Please select at least one content type to analyze!")

# Footer
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        Made with ❤️ by 🎀 Barbie Girls in a Barbie World 🎀
    </div>
""", unsafe_allow_html=True)