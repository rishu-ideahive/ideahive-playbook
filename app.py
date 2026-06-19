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
# 🎨 PREMIUM UI CSS INJECTION
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600&family=Playfair+Display:ital,wght=0,400;0,600;0,700;1,400;1,600&display=swap');
    
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
    
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 60vh;
        background: radial-gradient(circle at top center, rgba(108, 92, 231, 0.15) 0%, rgba(5, 5, 10, 0) 60%);
        pointer-events: none;
        z-index: 0;
    }
    
    [data-testid="stBlockContainer"] {
        max-width: 680px !important;
        padding-top: 4rem !important;
        padding-bottom: 8rem !important;
        position: relative;
        z-index: 10;
    }

    .brand-container {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .brand-logo {
        width: 96px;
        height: 96px;
        object-fit: contain;
        border-radius: 1.25rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        background: rgba(15, 16, 26, 0.5);
        backdrop-filter: blur(8px);
        padding: 0.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    .eyebrow-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        border: 1px solid #1A1B2E;
        background: rgba(15, 16, 26, 0.8);
        color: #FF9933;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 15px rgba(255, 153, 51, 0.1);
    }
    .main-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        line-height: 1.25 !important;
        margin-bottom: 1rem !important;
        letter-spacing: -0.02em !important;
    }
    .italic-gradient {
        font-style: italic;
        background: linear-gradient(135deg, #FF9933, #c96a10);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle-text {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 300;
        line-height: 1.6;
        max-width: 440px;
        margin: 0 auto;
    }

    .stTextArea > div > div > textarea {
        background: #0F101A !important;
        border: 1px solid #1A1B2E !important;
        border-radius: 16px !important;
        color: #f0eeff !important;
        padding: 18px !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    
    .stTextInput > div > div > input {
        background: #131A2A !important;
        border: 1px solid #1A1B2E !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 12px 16px !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #FF9933, #c96a10) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        width: 100% !important;
        box-shadow: 0 4px 24px rgba(255,153,51,0.25) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 32px rgba(255,153,51,0.4) !important;
        color: white !important;
    }

    .playbook-card {
        background-color: #0F101A;
        border: 1px solid #1A1B2E;
        border-radius: 1rem;
        padding: 2.5rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
        margin-top: 1.5rem;
    }
    .playbook-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,153,51,0.5), transparent);
    }
    
    .playbook-output h2 {
        font-family: 'Playfair Display', serif !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.8rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        border-bottom: 1px solid #1A1B2E;
        padding-bottom: 0.5rem;
    }
    .playbook-output h3 {
        font-family: 'Playfair Display', serif !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.4rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    .playbook-output p, .playbook-output li {
        color: #cbd5e1 !important;
        font-weight: 300 !important;
        line-height: 1.75 !important;
        font-size: 16px !important;
    }

    .waitlist-container-card {
        background: rgba(15, 16, 26, 0.9);
        border: 1px solid rgba(255, 153, 51, 0.3);
        border-radius: 1rem;
        padding: 2rem;
        margin-top: 3rem;
        box-shadow: 0 0 25px rgba(255, 153, 51, 0.08);
    }
    .waitlist-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        color: #ffffff;
        margin-bottom: 0.25rem;
        font-weight: 600;
    }
    .waitlist-subtitle {
        color: #94a3b8;
        font-size: 0.875rem;
        font-weight: 300;
        margin-bottom: 1.5rem;
    }

    .skeleton-box {
        background: rgba(26, 27, 46, 0.5);
        border-radius: 0.5rem;
        position: relative;
        overflow: hidden;
        margin-bottom: 1rem;
    }
    .skeleton-box::after {
        content: "";
        position: absolute;
        top: 0; right: 0; bottom: 0; left: 0;
        transform: translateX(-100%);
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.03), transparent);
        animation: shimmer 2s infinite;
    }
    @keyframes shimmer {
        100% { transform: translateX(100%); }
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 2. SECURE API CLIENT CONFIGURATION
# ==========================================
gemini_key = st.secrets.get("GEMINI_API_KEY")

if not gemini_key:
    st.error("Missing GEMINI_API_KEY in Streamlit Advanced Settings Secrets.")
    st.stop()

client = genai.Client(api_key=gemini_key)

# Session state management initialization
if "app_state" not in st.session_state:
    st.session_state.app_state = "idle"
if "playbook_data" not in st.session_state:
    st.session_state.playbook_data = None
if "waitlist_submitted" not in st.session_state:
    st.session_state.waitlist_submitted = False

# --- BRANDING HEADER LAYER ---
st.markdown("""
    <div class="brand-container">
        <img src="https://i.ibb.co/ymyzDNmj/IMG-20260301-153511-300.webp" class="brand-logo" alt="IdeaHive Logo">
        <br>
        <div class="eyebrow-badge">✨ AI Validation Engine 🐝</div>
        <h1 class="main-title">Validate your brilliant<br>idea in <span class="italic-gradient">seconds.</span></h1>
        <p class="subtitle-text">Stop guessing. Start building. Let our strategic AI engine craft a premium execution playbook.</p>
    </div>
""", unsafe_allow_html=True)


# --- STATE 1: SEED CONCEPT INPUT ---
if st.session_state.app_state == "idle":
    user_idea = st.text_area(
        "Enter your startup idea:",
        placeholder="Describe your startup idea briefly... (e.g., A marketplace for high-end second-hand coffee machines)",
        label_visibility="collapsed",
        height=140
    )
    
    submit_click = st.button("Generate My Playbook")
    
    if submit_click:
        if not user_idea.strip():
            st.warning("Please enter a valid startup idea first!")
        else:
            st.session_state.app_state = "generating"
            st.session_state.current_idea = user_idea
            st.rerun()


# --- STATE 2: SHIMMER SKELETON LOADER ---
if st.session_state.app_state == "generating":
    st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <p style="color: #FF9933; font-size: 0.875rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;">
                ✨ Synthesizing Strategy Playbook...
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    skeleton_box = st.empty()
    skeleton_box.markdown("""
        <div class="playbook-card">
            <div class="skeleton-box" style="height: 2rem; width: 35%;"></div>
            <div class="skeleton-box" style="height: 1rem; width: 100%;"></div>
            <div class="skeleton-box" style="height: 1rem; width: 92%;"></div>
            <br>
            <div class="skeleton-box" style="height: 1.75rem; width: 25%;"></div>
            <div class="skeleton-box" style="height: 4rem; width: 100%;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    try:
        prompt_payload = f"""
        You are an expert Startup Validation Engineer.
        Provide a detailed, step-by-step landing page validation playbook blueprint specifically tailored for this startup idea: "{st.session_state.current_idea}".
        Use clean Markdown headers like '## Executive Summary' and '## First 30 Days: Action Plan'.
        List the exact low-friction landing page tools and audience-building software stacks required to run the test efficiently.
        
        Conclude your strategic playbook layout with this exact text message matching our brand container layout pattern:
        "✨ Wishing you the absolute best of luck on your validation journey! Let's build something historic together.  
        — Team IdeaHive 🐝"
        """
        
        # Dual-Model Resiliency Pipeline Strategy (Flash-to-Flash alternative structure)
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_payload
            )
        except Exception as flash_error:
            # Check for rate/overload signals and drop down to high-quota alternative 2.0 architecture safely
            error_msg = str(flash_error)
            if "503" in error_msg or "UNAVAILABLE" in error_msg or "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt_payload
                )
            else:
                raise flash_error

        st.session_state.playbook_data = response.text
        st.session_state.app_state = "results"
        st.rerun()
    except Exception as e:
        st.error(f"Core engine connection failed: {str(e)}")
        st.session_state.app_state = "idle"
        st.stop()


# --- STATE 3: RESULTS + INTERACTIVE WAITLIST ---
if st.session_state.app_state == "results":
    
    st.markdown("""
        <div class="playbook-card">
            <div class="playbook-output">
    """, unsafe_allow_html=True)
    
    st.markdown(st.session_state.playbook_data)
    
    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="waitlist-container-card">
            <div class="waitlist-title">Join the Elite Waitlist</div>
            <div class="waitlist-subtitle">Get early access to our full suite of premium AI validation tools.</div>
        </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.waitlist_submitted:
        with st.form("waitlist_form", clear_on_submit=True):
            email_input = st.text_input("Email Field", placeholder="Enter your email address", label_visibility="collapsed")
            submit_email = st.form_submit_button("Join Elite Waitlist")
            
            if submit_email:
                if email_input.strip() and "@" in email_input:
                    st.session_state.waitlist_submitted = True
                    st.rerun()
                else:
                    st.error("Please provide a valid email address.")
    else:
        st.success("🎉 You're on the list! Welcome to Team IdeaHive. 🐝")
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Test Another Idea"):
        st.session_state.app_state = "idle"
        st.session_state.playbook_data = None
        st.session_state.waitlist_submitted = False
        st.rerun()
