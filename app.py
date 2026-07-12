import streamlit as st
import os
from google import genai


# Page configuration
st.set_page_config(
    page_title="IdeaHive AI Startup Playbook Generator",
    page_icon="🐝",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# IdeaHive product design layer. This mirrors the homepage's design system,
# while keeping this screen focused on the Playbook Generator task.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Syne:wght@700;800&display=swap');

:root {
    --ih-black: #07070f;
    --ih-deep: #0e0e1c;
    --ih-card: #13131f;
    --ih-border: rgba(120, 100, 255, 0.18);
    --ih-indigo: #6c5ce7;
    --ih-cyan: #00cfe8;
    --ih-soft: #a29bfe;
    --ih-white: #f0eeff;
    --ih-muted: #7f8ca0;
}

#MainMenu, header, footer, .stDeployButton, [data-testid="stToolbar"] { display: none !important; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--ih-black) !important;
    color: var(--ih-white) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background-image: radial-gradient(circle at 50% -16%, rgba(108, 92, 231, 0.18), transparent 34%),
                      radial-gradient(circle at 92% 22%, rgba(0, 207, 232, 0.07), transparent 24%) !important;
}

[data-testid="stBlockContainer"] {
    max-width: 760px !important;
    padding: 18px 24px 56px !important;
}

.ih-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 0 -24px 42px;
    padding: 12px 24px;
    border-bottom: 1px solid var(--ih-border);
    background: rgba(7, 7, 15, 0.72);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
}

.ih-brand { display: inline-flex; align-items: center; gap: 9px; }
.ih-brand img { width: 30px; height: 30px; border-radius: 8px; object-fit: cover; }
.ih-brand-name {
    font-family: 'Syne', sans-serif;
    font-size: 17px;
    font-weight: 800;
    background: linear-gradient(120deg, var(--ih-cyan), var(--ih-soft));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.ih-product-label {
    color: var(--ih-muted);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.ih-hero { position: relative; text-align: center; margin: 0 auto 24px; }
.ih-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 6px 13px;
    margin-bottom: 14px;
    border: 1px solid rgba(0, 207, 232, 0.35);
    border-radius: 50px;
    background: rgba(0, 207, 232, 0.08);
    color: var(--ih-cyan);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.ih-badge::before { content: ''; width: 6px; height: 6px; border-radius: 50%; background: var(--ih-cyan); box-shadow: 0 0 10px var(--ih-cyan); }
.ih-hero h1 {
    margin: 0 0 10px;
    color: var(--ih-white);
    font-family: 'Syne', sans-serif;
    font-size: clamp(30px, 5vw, 46px);
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.08;
}
.ih-gradient-text {
    background: linear-gradient(120deg, var(--ih-indigo), var(--ih-cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.ih-hero p { max-width: 535px; margin: 0 auto; color: var(--ih-muted); font-size: 14px; line-height: 1.65; }

.ih-form-intro, .ih-result-header { margin-bottom: 10px; }
.ih-eyebrow { color: var(--ih-soft); font-size: 11px; font-weight: 700; letter-spacing: 0.11em; text-transform: uppercase; }
.ih-form-title, .ih-result-title { margin: 4px 0 0; color: var(--ih-white); font-family: 'Syne', sans-serif; font-size: 17px; font-weight: 700; }

div[data-testid="stTextArea"] { margin-top: 0 !important; }
div[data-testid="stTextArea"] [data-baseweb="textarea"] {
    border: 1px solid var(--ih-border) !important;
    border-radius: 14px !important;
    background: rgba(7, 7, 15, 0.92) !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.025) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
div[data-testid="stTextArea"] textarea {
    min-height: 104px !important;
    height: 104px !important;
    padding: 16px !important;
    border: 0 !important;
    background: rgba(7, 7, 15, 0.92) !important;
    color: var(--ih-white) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.55 !important;
}
div[data-testid="stTextArea"] textarea::placeholder { color: #657088 !important; }
div[data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within {
    border-color: var(--ih-cyan) !important;
    box-shadow: 0 0 0 3px rgba(0, 207, 232, 0.12), inset 0 1px 0 rgba(255,255,255,0.03) !important;
}

div.stButton { margin-top: 14px; }
div.stButton > button {
    width: 100% !important;
    min-height: 56px !important;
    padding: 0 24px !important;
    border: 0 !important;
    border-radius: 50px !important;
    background: linear-gradient(135deg, var(--ih-indigo), var(--ih-cyan), var(--ih-indigo)) !important;
    background-size: 200% 200% !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 7px 26px rgba(108, 92, 231, 0.32), inset 0 1px 0 rgba(255, 255, 255, 0.18) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease !important;
}
div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(0, 207, 232, 0.28) !important; filter: brightness(1.06); }
div.stButton > button:active { transform: scale(0.985); }
div.stButton > button:focus-visible { outline: 3px solid rgba(0, 207, 232, 0.35) !important; outline-offset: 3px; }

.ih-form-note { margin: 11px 0 0; color: var(--ih-muted); font-size: 12px; text-align: center; }

.ih-loading, .ih-report-shell, [data-testid="stVerticalBlockBorderWrapper"] {
    position: relative;
    overflow: hidden;
    border: 1px solid var(--ih-border);
    border-radius: 20px;
    background: rgba(19, 19, 31, 0.8);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.045), 0 16px 42px rgba(0, 0, 0, 0.18);
}
.ih-loading { padding: 24px; text-align: center; }
.ih-loading::before, .ih-report-shell::before { content: ''; position: absolute; width: 190px; height: 190px; border-radius: 50%; pointer-events: none; filter: blur(4px); }
.ih-loading::before { top: -110px; right: -62px; background: radial-gradient(circle, rgba(0,207,232,0.2), transparent 68%); }
.ih-loading-icon { display: inline-flex; align-items: center; justify-content: center; width: 42px; height: 42px; margin-bottom: 11px; border: 1px solid rgba(0,207,232,0.3); border-radius: 14px; background: rgba(0,207,232,0.08); color: var(--ih-cyan); font-size: 19px; animation: ih-pulse 1.5s ease-in-out infinite; }
.ih-loading h2 { margin: 0 0 5px; color: var(--ih-white); font-family: 'Syne', sans-serif; font-size: 19px; }
.ih-loading p { margin: 0; color: var(--ih-muted); font-size: 13px; }
.ih-loading-status { display: inline-flex; align-items: center; gap: 6px; margin-top: 14px; color: var(--ih-soft); font-size: 11px; font-weight: 600; }
.ih-loading-status::before { content: ''; width: 5px; height: 5px; border-radius: 50%; background: var(--ih-cyan); box-shadow: 0 0 8px var(--ih-cyan); }
@keyframes ih-pulse { 0%, 100% { box-shadow: 0 0 0 rgba(0,207,232,0); } 50% { box-shadow: 0 0 20px rgba(0,207,232,0.26); } }

.ih-report-shell { padding: 24px; margin-bottom: 10px; }
.ih-report-container { margin-bottom: 10px; }
[data-testid="stVerticalBlockBorderWrapper"] {
    padding: 24px !important;
    margin-bottom: 10px;
}
.ih-report-shell::before { bottom: -125px; left: -70px; background: radial-gradient(circle, rgba(108,92,231,0.22), transparent 68%); }
.ih-report-header { position: relative; z-index: 1; padding-bottom: 17px; border-bottom: 1px solid var(--ih-border); }
.ih-report-header span { color: var(--ih-cyan); font-size: 11px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; }
.ih-report-header h2 { margin: 5px 0 0; color: var(--ih-white); font-family: 'Syne', sans-serif; font-size: 22px; line-height: 1.15; }

[data-testid="stMarkdownContainer"] { color: var(--ih-white); }
[data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3 {
    position: relative;
    z-index: 1;
    color: var(--ih-white) !important;
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em;
    line-height: 1.2;
}
[data-testid="stMarkdownContainer"] h1 { margin: 25px 0 12px !important; font-size: 24px !important; }
[data-testid="stMarkdownContainer"] h2 { margin: 23px 0 10px !important; font-size: 19px !important; }
[data-testid="stMarkdownContainer"] h3 { margin: 19px 0 8px !important; font-size: 16px !important; color: var(--ih-soft) !important; }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li { position: relative; z-index: 1; color: #c7c4d7 !important; font-size: 14px; line-height: 1.75; }
[data-testid="stMarkdownContainer"] ul, [data-testid="stMarkdownContainer"] ol { padding-left: 22px; }
[data-testid="stMarkdownContainer"] li::marker { color: var(--ih-cyan); }
[data-testid="stMarkdownContainer"] strong { color: var(--ih-white); }
[data-testid="stMarkdownContainer"] blockquote { margin: 18px 0; padding: 10px 15px; border-left: 2px solid var(--ih-cyan); border-radius: 0 10px 10px 0; background: rgba(0, 207, 232, 0.055); color: var(--ih-soft); }
[data-testid="stMarkdownContainer"] hr { margin: 22px 0; border-color: var(--ih-border); }

div[data-testid="stAlert"] { border-radius: 12px !important; border: 1px solid var(--ih-border) !important; background: rgba(108, 92, 231, 0.12) !important; color: var(--ih-white) !important; }

.ih-reset-note { margin-top: 12px; color: var(--ih-muted); font-size: 12px; text-align: center; }

@media (min-width: 768px) {
    [data-testid="stBlockContainer"] { padding-top: 20px !important; }
    .ih-nav { margin-bottom: 48px; }
    .ih-hero { margin-bottom: 27px; }
    .ih-report-shell, [data-testid="stVerticalBlockBorderWrapper"] { padding: 30px !important; }
}
@media (max-width: 520px) {
    [data-testid="stBlockContainer"] { padding: 8px 16px 24px !important; }
    .ih-nav { margin: 0 -16px 18px; padding: 10px 16px; }
    .ih-product-label { font-size: 9px; }
    .ih-hero h1 { font-size: 30px; }
    .ih-hero p { font-size: 13px; }
    .ih-hero { margin-bottom: 17px; }
    .ih-badge { margin-bottom: 11px; }
    .ih-form-title { font-size: 16px; }
    div[data-testid="stTextArea"] textarea { min-height: 96px !important; height: 96px !important; padding: 14px !important; }
    div.stButton { margin-top: 12px; }
    div.stButton > button { min-height: 54px !important; }
    .ih-report-shell, .ih-loading, [data-testid="stVerticalBlockBorderWrapper"] { border-radius: 16px; padding: 20px !important; }
}
</style>
""", unsafe_allow_html=True)


# Secure API client configuration
gemini_key = st.secrets.get("GEMINI_API_KEY")
if not gemini_key:
    st.error("Missing GEMINI_API_KEY in Streamlit Advanced Settings.")
    st.stop()

client = genai.Client(api_key=gemini_key)

if "app_state" not in st.session_state: st.session_state.app_state = "idle"
if "playbook_data" not in st.session_state: st.session_state.playbook_data = None


# Product header and focused hero
st.markdown("""
<div class="ih-nav">
    <div class="ih-brand">
        <img src="https://i.ibb.co/ymyzDNmj/IMG-20260301-153511-300.webp" alt="IdeaHive logo" />
        <span class="ih-brand-name">IdeaHive</span>
    </div>
    <span class="ih-product-label">AI Playbook</span>
</div>
<section class="ih-hero">
    <div class="ih-badge">Available now</div>
    <h1>Turn your idea into an<br><span class="ih-gradient-text">execution playbook.</span></h1>
    <p>Describe your startup idea and get practical validation steps to move from concept to confident action.</p>
</section>
""", unsafe_allow_html=True)


# Engine logic flow windows
if st.session_state.app_state == "idle":
    st.markdown("""
    <div class="ih-form-intro">
        <div class="ih-eyebrow">Your startup idea</div>
        <div class="ih-form-title">What are you building?</div>
    </div>
    """, unsafe_allow_html=True)
    user_idea = st.text_area("Concept Field", placeholder="Describe your startup concept here...", label_visibility="collapsed", height=104)
    if st.button("Generate my playbook"):
        if not user_idea.strip(): st.warning("Please type an idea first!")
        else:
            st.session_state.app_state = "generating"
            st.session_state.current_idea = user_idea
            st.rerun()
    st.markdown('<p class="ih-form-note">Built for students, solo founders, and first-time entrepreneurs.</p>', unsafe_allow_html=True)

if st.session_state.app_state == "generating":
    st.markdown("""
    <div class="ih-loading">
        <div class="ih-loading-icon">✦</div>
        <h2>Analyzing your startup idea...</h2>
        <p>Building a focused validation playbook for your next move.</p>
        <div class="ih-loading-status">AI analysis in progress</div>
    </div>
    """, unsafe_allow_html=True)
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
    with st.container(border=True):
        st.markdown("""
        <div class="ih-report-container">
        <div class="ih-report-header">
            <span>IdeaHive AI Playbook</span>
            <h2>Your startup validation brief</h2>
        </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(st.session_state.playbook_data)

    if st.button("Test another idea"):
        st.session_state.app_state = "idle"
        st.session_state.playbook_data = None
        st.rerun()
    st.markdown('<p class="ih-reset-note">Start a fresh analysis whenever your idea evolves.</p>', unsafe_allow_html=True)

