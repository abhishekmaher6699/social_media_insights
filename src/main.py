import streamlit as st
import pandas as pd
import plotly.express as px
data = pd.read_csv('./src/data/social_media_final_draft.csv')

st.set_page_config(
    page_title="Social Media Performance Dashboard",
    page_icon="🚀",
    layout="wide"
)

from langflow import get_data

st.markdown("""
<style>
    /* General layout and background */

    .main {
        padding: 2rem;
        background: #003049; /* Dark Blue */
        border-radius: 20px;
        box-shadow: none;
    }

    /* Header styling */
    h1 {
        color: #fdf0d5;  /* Light Beige */
        font-family: 'Gothic', serif;
        font-size: 3.8rem;
        font-weight: 900;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 3rem;
        position: relative;
    }

    h1::before, h1::after {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        font-size: 2.5rem;
    }

    h1::before { left: 2rem; }
    h1::after { right: 2rem; }

    h2 {
        color: #c1121f;  /* Bright Red */
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 1.8rem;
        border-bottom: 2px solid #c1121f;
        padding-bottom: 0.5rem;
    }

    h3 {
        color: #fdf0d5;  /* Light Beige */
        font-size: 2rem;
        font-weight: 600;
    }

    /* Add space between the header and content */
    .stTextInput, .stSelectbox, .stRadio, .stCheckbox, .stButton {
        margin-top: 2rem;
    }

    /* Metric container styling */
    .metric-container {
        background: #C0FDFB; /* Bright red */
        border: 2px solid #FDF0D5; /* beige */
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        transition: all 0.4s ease;
    }

    .metric-container:hover {
        transform: none;
        box-shadow: none;
        border-color: #fdf0d5;
    }

    /* Button styling */
    .stButton>button {
        background: #FDF0D5; /* Beige */
        color: #080602; 
        border: 2px solid #fdf0d5;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1.3rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .stButton>button:hover {
        transform: translateY(0);
        box-shadow: none;
    }

    /* Checkbox styling */
    .stCheckbox {
        background: #C0FDFB;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }

    

    .stCheckbox>label {
        font-size: 1.4rem;
        color: #fdf0d5;  /* Beige */
        font-weight: 600;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        font-size: 1.4rem;
        font-weight: 700;
        background: #003049; /* Dark Blue */
        color: #fdf0d5;  /* Light Beige */
        border-radius: 10px;
        padding: 1rem 1.5rem;
        border: 1px solid #c1121f;
        margin: 0.8rem 0;
    }

    .streamlit-expanderHeader:hover {
        background: #c1121f; /* Bright Red */
        color: #003049; /* Dark Blue */
        border-color: #fdf0d5;
    }

    /* Info, warning, and success boxes styling */
    .stInfo, .stWarning, .stSuccess {
        background: #003049; /* Dark Blue */
        color: #fdf0d5;  /* Light Beige */
        padding: 1rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        border-left: 4px solid;
    }

    .stInfo { border-color: #fdf0d5; }
    .stWarning { border-color: #c1121f; }
    .stSuccess { border-color: #780000; }

    /* Metric value styling */
    .stMetric {
        background: #C0FDFB
        padding: 2rem;
        border-radius: 8px;
        border: 1px solid #5D737E
        margin: 0.5rem 0;
    }

   

    .metric-value {
        color: #c1121f !important; /* Bright Red */
        font-size: 1 rem !important;
        font-weight: bold !important;
    }

    .metric-label {
        color: #fdf0d5 !important; /* Light Beige */
        font-size: 1.2rem !important;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
        background: #003049; /* Dark Blue */
    }

    ::-webkit-scrollbar-thumb {
        background: #c1121f; /* Bright Red */
        border-radius: 6px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #780000; /* Deep Red */
    }

    /* Footer styling */
    .footer {
        text-align: center;
        color: #fdf0d5;  /* Light Beige */
        padding: 2rem;
        margin-top: 3rem;
        font-size: 1.2rem;
        border-top: 2px solid #c1121f;
        background: #003049; /* Dark Blue */
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
    <h1>📊 Social Media Performance Dashboard</h1>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.markdown("### 🎯 Select Content Types")
    
    options = {
        "Text": "📝",
        "Image": "🖼️",
        "Video": "🎥",
        "Reels": "📱",
        "Carousel": "🎠"
    }
    
    selected_options = []
    
    cols = st.columns(3)
    for idx, (option, emoji) in enumerate(options.items()):
        with cols[idx % 3]:
            if st.checkbox(f"{emoji} {option}", key=option):
                selected_options.append(option)

    if st.button("Generate Insights 🚀", use_container_width=True):
        if selected_options:
            # Get data

            with st.spinner("Fetching data... Please wait ⏳"):
            # Get data
                response = get_data(selected_options)
                print(response)


                data['Engagement_Rate'] = ((data['Likes'] + data['Shares'] + data['Comments']) / data['Reach']) * 100

                average_metrics_df = data.groupby('Post_Type').agg({
                    'Likes': 'mean',
                    'Shares': 'mean',
                    'Comments': 'mean',
                    'Reach': 'mean',
                    'Engagement_Rate': 'mean'
                }).reset_index()

                average_metrics_df.columns = [
                    'Post Type', 'Average Likes', 'Average Shares', 
                    'Average Comments', 'Average Reach', 'Engagement Rate (%)'
                ]

                average_metrics_df['Engagement Rate (%)'] = average_metrics_df['Engagement Rate (%)'].round(2)

                average_metrics_df = average_metrics_df[average_metrics_df['Post Type'].isin(selected_options)]
                average_metrics_df.set_index("Post Type", inplace=True)

                st.markdown("## 📈 Performance Metrics (Average)")
                st.dataframe(average_metrics_df.style.format(precision=2, na_rep="-"), use_container_width=True)


                st.markdown("## 📊 Visualization of Post Performance")


                post_distribution_fig = px.pie(
                    data, 
                    names='Post_Type', 
                    title='🔵 Post Distribution by Type', 
                    hole=0.4,  
                    template='plotly'
                )
                st.plotly_chart(post_distribution_fig, use_container_width=True)

                average_metrics = data.groupby('Post_Type', as_index=False)[['Likes', 'Shares', 'Comments', 'Reach']].mean()
                average_metrics_fig = px.bar(
                    average_metrics.melt(id_vars='Post_Type', var_name='Metric', value_name='Average Value'), 
                    x='Post_Type', 
                    y='Average Value', 
                    color='Metric', 
                    barmode='group', 
                    title=' 📊 Average Likes, Shares, Comments, and Reach by Post Type', 
                    template='plotly',
                    labels={'Average Value': 'Average Value', 'Post_Type': 'Post Type'}
                )
                st.plotly_chart(average_metrics_fig, use_container_width=True)   
            


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

            if "comparative_analysis" in response and response['comparative_analysis']:
                st.markdown("## 🔄 Comparative Analysis")
                with st.expander("View Analysis", expanded=True):
                    for key, analysis in response["comparative_analysis"].items():
                        st.warning(f"**{key.replace('_', ' ').title()}**: {analysis}")

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


st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        Made with ❤️ by 🎀 Barbie Girls in a Barbie World 🎀
    </div>
""", unsafe_allow_html=True)