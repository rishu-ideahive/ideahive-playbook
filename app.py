import streamlit as st
import os
from google import genai

# 1. Page Configuration & Setup
st.set_page_config(
    page_title="IdeaHive AI Startup Playbook Generator",
    page_icon="🐝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 🎨 UI & FLOATING AVATAR BOX LAYER (CSS)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght=0,400;0,600;0,700;1,400;1,600&display=swap');
    
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stToolbar"] {display: none;}
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #05050A !important;
        color: #cbd5e1 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-testid="stBlockContainer"] {
        max-width: 680px !important;
        padding-top: 3rem !important;
        padding-bottom: 8rem !important;
    }

    /* 🤖 FLOATING AVATAR WORKSPACE CONTAINER */
    .avatar-fixed-stage {
        position: fixed;
        bottom: 25px;
        right: 25px;
        width: 140px;
        height: 140px;
        background: rgba(15, 16, 26, 0.75);
        border: 2px solid rgba(255, 153, 51, 0.4);
        border-radius: 50%;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6), 0 0 20px rgba(255, 153, 51, 0.15);
        z-index: 99999;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: visible;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .avatar-fixed-stage:hover {
        transform: scale(1.08);
        border-color: #FF9933;
    }

    /* Little live pulsing light dot on her frame */
    .live-status-dot {
        position: absolute;
        top: 8px;
        right: 12px;
        width: 10px;
        height: 10px;
        background-color: #4ade80;
        border-radius: 50%;
        box-shadow: 0 0 8px #4ade80;
    }

    .placeholder-text {
        color: #ffffff;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        text-align: center;
    }

    /* Main Content Typography Styling */
    .brand-container { text-align: center; margin-bottom: 2rem; }
    .main-title { font-family: 'Playfair Display', serif !important; font-size: 2.3rem !important; color: #ffffff !important; }
    .italic-gradient { font-style: italic; background: linear-gradient(135deg, #FF9933, #c96a10); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    .stTextArea > div > div > textarea { background: #0F101A !important; border: 1px solid #1A1B2E !important; border-radius: 16px !important; color: #f0eeff !important; padding: 18px !important; }
    div.stButton > button { background: linear-gradient(135deg, #FF9933, #c96a10) !important; color: white !important; width: 100% !important; border-radius: 12px !important; padding: 12px 28px !important; }
    .playbook-card { background-color: #0F101A; border: 1px solid #1A1B2E; border-radius: 1rem; padding: 2.5rem; }
    </style>
""", unsafe_allow_html=True)

# --- EMBEDDING THE FLOATING AVATAR GLASS COMPONENT STAGE ---
st.markdown("""
    <div class="avatar-fixed-stage" onclick="alert('Aiva is getting assembled! High-fidelity 3D rendering pipeline initializing...')">
        <div class="live-status-dot"></div>
        <div class="placeholder-text">🤖 AIVA<br><span style="font-size:10px; opacity:0.6;">[Stage Ready]</span></div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 2. SECURE API CLIENT CONFIGURATION
# ==========================================
gemini_key = st.secrets.get("GEMINI_API_KEY")
if not gemini_key:
    st.error("Missing GEMINI_API_KEY in Streamlit Advanced Settings.")
    st.stop()

client = genai.Client(api_key=gemini_key)

if "app_state" not in st.session_state: st.session_state.app_state = "idle"
if "playbook_data" not in st.session_state: st.session_state.playbook_data = None

# --- HEADER APP LAYOUT ---
st.markdown("""
    <div class="brand-container">
        <div class="eyebrow-badge" style="color:#FF9933; font-size: 12px; margin-bottom:10px;">✨ AI Validation Engine 🐝</div>
        <h1 class="main-title">Validate your brilliant<br>idea in <span class="italic-gradient">seconds.</span></h1>
    </div>
""", unsafe_allow_html=True)

# --- ENGINE LOGIC FLOW WINDOWS ---
if st.session_state.app_state == "idle":
    user_idea = st.text_area("Concept Field", placeholder="Describe your startup concept here...", label_visibility="collapsed", height=130)
    if st.button("Generate My Playbook"):
        if not user_idea.strip(): st.warning("Please type an idea first!")
        else:
            st.session_state.app_state = "generating"
            st.session_state.current_idea = user_idea
            st.rerun()

if st.session_state.app_state == "generating":
    st.info("⚙️ Synthesizing premium target market matrix playbook structural layers...")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Provide a step-by-step startup validation playbook for: {st.session_state.current_idea}"
        )
        st.session_state.playbook_data = response.text
        st.session_state.app_state = "results"
        st.rerun()
    except Exception as e:
        st.error(f"Engine connection anomaly: {str(e)}")
        st.session_state.app_state = "idle"

if st.session_state.app_state == "results":
    st.markdown('<div class="playbook-card">', unsafe_allow_html=True)
    st.markdown(st.session_state.playbook_data)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Test Another Idea"):
        st.session_state.app_state = "idle"
        st.session_state.playbook_data = None
        st.rerun()
