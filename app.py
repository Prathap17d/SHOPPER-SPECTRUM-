import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

# -------------------------------------------------------------
# 1. PAGE CONFIGURATION & BALANCED READABILITY THEME
# -------------------------------------------------------------
st.set_page_config(
    page_title="Shopper Spectrum - Corporate Analytics Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize navigation state if it doesn't exist yet
if 'active_module' not in st.session_state:
    st.session_state.active_module = "Executive Overview"

# Clean, Targeted Global Styling Injection
st.markdown("""
    <style>
        /* MAIN APPS BACKGROUND */
        .stApp {
            background-color: #fdfbf7 !important;
        }
        
        /* THE FIX: TARGETING NATIVE TITLE LINKS AND HEADER WRAPPERS FORCEFULLY */
        .stApp h1, .stApp h1 a, [data-testid="stHeader"] h1, [data-testid="stMarkdownContainer"] h1 {
            font-size: 44px !important;  /* Perfect, large header size */
            font-weight: 900 !important;
            color: #111827 !important;
            text-decoration: none !important;
            line-height: 1.2 !important;
            display: block !important;
        }
        
        /* CONTENT SUB-HEADERS */
        h2, h3 {
            font-size: 24px !important;  
            font-weight: 800 !important;
            color: #111827 !important;
        }
        h4 {
            font-weight: 700 !important;
            font-size: 20px !important;
        }
        
        /* PARAGRAPHS & BASIC TEXT LABELS */
        p, li, span, label {
            font-size: 16px !important;  
            line-height: 1.6 !important;
        }

        /* TARGETING STREAMLIT DROPDOWNS & INPUT BOXES */
        .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
            font-size: 17px !important;  
            font-weight: 600 !important;
            height: auto !important;
            padding: 6px !important;
        }
        
        /* PREMIUM SIDEBAR SURFACE */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #cae6df 0%, #f3e9cb 100%) !important;
            border-right: 1px solid #d1d5db;
        }
        
        .sidebar-title {
            font-size: 22px !important;   
            font-weight: 900 !important;
            color: #111827 !important;
            letter-spacing: 1.5px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        /* ALIGNED SIDEBAR NAVIGATION BUTTONS */
        .stSidebar div.stButton button {
            font-size: 15px !important;   
            font-weight: 800 !important;
            padding: 10px 14px !important; 
            border-radius: 10px !important;
            margin-bottom: 12px !important;
            border: 2px solid #b5d1ca !important;
            background-color: rgba(255, 255, 255, 0.6) !important;
            color: #1f2937 !important;
            text-align: center !important;  
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            width: 100% !important;
        }
        .stSidebar div.stButton button:hover {
            background-color: #ffffff !important;
            border-color: #1e3a8a !important;
            color: #1e3a8a !important;
        }
        
        /* MAIN ACTION BUTTONS */
        .main .stButton>button {
            background-color: #1e3a8a !important;
            color: white !important;
            border-radius: 10px !important;
            font-weight: 800 !important;
            font-size: 18px !important;   
            width: 100% !important;
            padding: 12px !important;
            border: none !important;
        }
        
        /* WORK CARDS */
        .premium-card {
            background-color: #ffffff;
            padding: 25px; 
            border-radius: 16px;
            border: 1px solid #e5e7eb;
            margin-bottom: 25px;
        }
        
        /* DATA METRICS CARDS */
        .kpi-card {
            background-color: #ffffff;
            padding: 20px 15px;
            border-radius: 14px;
            border: 1px solid #e5e7eb;
            border-top: 5px solid #1e3a8a;
            text-align: center;
        }
        .kpi-lbl {
            font-size: 12px !important;   
            color: #4b5563 !important;
            font-weight: 800 !important;
            text-transform: uppercase;
        }
        .kpi-val {
            font-size: 22px !important;   
            font-weight: 900 !important;
            color: #111827 !important;
            margin: 8px 0px !important;
        }
        .kpi-sub {
            font-size: 13px !important;   
            color: #6b7280 !important;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. LOAD SERIALIZED ASSETS
# -------------------------------------------------------------
@st.cache_resource
def load_models():
    p_kmeans = 'models/kmeans_model.pkl'
    p_scaler = 'models/scaler.pkl'
    p_sim = 'models/item_similarity.pkl'
    
    kmeans, scaler, item_sim_df = None, None, None
    
    try:
        if os.path.exists(p_kmeans):
            with open(p_kmeans, 'rb') as f:
                kmeans = pickle.load(f)
        if os.path.exists(p_scaler):
            with open(p_scaler, 'rb') as f:
                scaler = pickle.load(f)
        if os.path.exists(p_sim):
            with open(p_sim, 'rb') as f:
                item_sim_df = pickle.load(f)
    except Exception as e:
        st.sidebar.error(f"Data Loading Error: {e}")
        
    return kmeans, scaler, item_sim_df

kmeans, scaler, item_sim_df = load_models()

# -------------------------------------------------------------
# 3. SIDEBAR NAVIGATION PANEL
# -------------------------------------------------------------
st.sidebar.markdown("<p class='sidebar-title'>NAVIGATION</p>", unsafe_allow_html=True)

if st.sidebar.button("📋 Executive Overview", key="btn_overview", use_container_width=True):
    st.session_state.active_module = "Executive Overview"

if st.sidebar.button("🎯 Customer Segmentation Matrix", key="btn_segment", use_container_width=True):
    st.session_state.active_module = "Customer Segmentation Matrix"

if st.sidebar.button("🛍️ Product Recommendation Index", key="btn_recom", use_container_width=True):
    st.session_state.active_module = "Product Recommendation Index"

app_mode = st.session_state.active_module

# -------------------------------------------------------------
# MAIN DASHBOARD INTERFACE (Using Native Streamlit Element)
# -------------------------------------------------------------
st.markdown("""
    <div style="
        font-size: 62px;
        font-weight: 950;
        color: #111827;
        letter-spacing: -1px;
        line-height: 1.1;
        margin-top: 10px;
    ">
        Shopper Spectrum Analytics Portal
    </div>
""", unsafe_allow_html=True)

st.markdown("<p style='color: #4b5563 !important; font-size: 25px !important; margin-top: -10px !important; margin-bottom: 25px !important;'>Strategic Behavioral Modeling & Customer Affinity Engine</p>", unsafe_allow_html=True)
st.markdown("---")

# MODULE 1: OVERVIEW (Populated with EDA conclusions)
if app_mode == "Executive Overview":
    st.markdown("""
        <div class='premium-card'>
            <h3 style='margin-top:0; font-size: 24px; font-weight: 700; color: #111827;'>Operational Parameters</h3>
            <p style='color: #374151; font-size: 16px; line-height: 1.6; margin-bottom:0;'>
                This centralized workspace serves as an enterprise decision matrix. 
                Use the scaled sidebar module options on the left to seamlessly run real-time 
                machine learning customer profile checks or query product-to-product cross-selling 
                recommendations from your model results.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='font-weight: 700; color: #111827; margin-top: 25px;'>Data Discovery Insights</h3>", unsafe_allow_html=True)
    
    # Updated Grid of 5 cards showing deep product insights
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
            <div class='kpi-card'>
                <div class='kpi-lbl'>Primary Market Hub</div>
                <div class='kpi-val' style='font-size: 16px; font-weight: 700;'>United Kingdom</div>
                <div style='color: #6b7280; font-size: 12px; margin-top:4px;'>349,203 Core Transactions</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class='kpi-card'>
                <div class='kpi-lbl'>Peak Sales Volatility</div>
                <div class='kpi-val' style='font-size: 16px; font-weight: 700;'>November Velocity</div>
                <div style='color: #16a34a; font-size: 12px; margin-top:4px;'>Revenue Peak > 1.15M</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class='kpi-card'>
                <div class='kpi-lbl'>Highest Bulk Order</div>
                <div class='kpi-val' style='font-size: 14px; font-weight: 700;'>Paper Craft, Little Birdie</div>
                <div style='color: #dc2626; font-size: 12px; margin-top:4px;'>80,995 Units (Single Order)</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
            <div class='kpi-card'>
                <div class='kpi-lbl'>Top Consistent Bestseller</div>
                <div class='kpi-val' style='font-size: 14px; font-weight: 700;'>White Heart T-Light Holder</div>
                <div style='color: #2563eb; font-size: 12px; margin-top:4px;'>Highest Transaction Frequency</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col5:
        st.markdown("""
            <div class='kpi-card'>
                <div class='kpi-lbl'>Lowest Demand Lines</div>
                <div class='kpi-val' style='font-size: 14px; font-weight: 700;'>Letter "Z" Bling Key Ring</div>
                <div style='color: #6b7280; font-size: 12px; margin-top:4px;'>1 Unit Sold (Clearance Risk)</div>
            </div>
        """, unsafe_allow_html=True)

# MODULE 2: SEGMENTATION
elif app_mode == "Customer Segmentation Matrix":
    st.markdown("<h3>Real-Time Profiling Interface</h3>", unsafe_allow_html=True)
    
    if kmeans is None or scaler is None:
        st.warning("⚠️ Segmentation Model files ('kmeans_model.pkl' or 'scaler.pkl') were not detected in your 'models/' folder. Please verify the files.")
    else:
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("<h4>Input Metrics</h4>", unsafe_allow_html=True)
            recency = st.number_input("Recency (Days since last active invoice)", min_value=0, max_value=365, value=30)
            frequency = st.number_input("Frequency (Aggregate unique order volume)", min_value=1, max_value=500, value=5)
            monetary = st.number_input("Monetary Value (Gross accumulated account revenue)", min_value=1.0, value=500.0)
            
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            predict_btn = st.button("Evaluate Account Profile")
            
        with col2:
            st.markdown("<h4>Model Assignment</h4>", unsafe_allow_html=True)
            if predict_btn:
                input_data = np.array([[recency, frequency, monetary]])
                scaled_input = scaler.transform(input_data)
                cluster_pred = kmeans.predict(scaled_input)[0]
                
                cluster_names = {
                    2: ('High-Value VIP Asset', '#16a34a', 'Prioritize premium direct lines and loyalty rewards.'),
                    0: ('Regular Shopper', '#2563eb', 'Maintain operational engagement via routine promotional updates.'),
                    3: ('Occasional Buyer', '#d97706', 'Deploy targeted coupon sequences to catalyze order frequencies.'),
                    1: ('At-Risk Customer Index', '#dc2626', 'Deploy high-incentive win-back frameworks immediately.')
                }
                name, color, strategy = cluster_names.get(cluster_pred, ('Unclassified', '#4b5563', 'Awaiting variables.'))
                
                st.markdown(f"""
                    <div style='background-color: #ffffff; padding: 25px; border-radius: 12px; border: 1px solid #e5e7eb; border-left: 8px solid {color};'>
                        <h3 style='color: {color}; margin-top:0; font-size: 25px !important;'>{name}</h3>
                        <p style='margin-top: 12px; margin-bottom:0;'><b>Action Protocol:</b> {strategy}</p>
                    </div>
                """, unsafe_allow_html=True)

# MODULE 3: RECOMMENDATIONS
elif app_mode == "Product Recommendation Index":
    st.markdown("<h3>Cross-Selling Affinity Configuration</h3>", unsafe_allow_html=True)
    
    if item_sim_df is None:
        st.warning("⚠️ Product Similarity file ('item_similarity.pkl') was not detected or is empty inside your 'models/' folder.")
    else:
        product_list = item_sim_df.index.tolist()
        
        if len(product_list) == 0:
            st.error("❌ The loaded similarity matrix dataset contains 0 products.")
        else:
            selected_product = st.selectbox("Search Active Stock Catalog:", product_list)
            
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            if st.button("Generate Affinity Matches"):
                similar_items = item_sim_df[selected_product].sort_values(ascending=False).iloc[1:6]
                
                st.markdown("<h4 style='margin-top:25px; margin-bottom:12px;'>Associated Target Items:</h4>", unsafe_allow_html=True)
                for item, score in zip(similar_items.index, similar_items.values):
                    st.markdown(f"""
                        <div style='background-color: white; padding: 18px 20px; border-radius: 10px; border: 1px solid #e5e7eb; margin-bottom: 12px;'>
                            <span style='font-weight: 700; color: #374151;'>{item}</span> 
                            <span style='float:right; color:#2563eb; font-weight:900;'>{(score*100):.1f}% Match</span>
                        </div>
                    """, unsafe_allow_html=True)