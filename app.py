import streamlit as st
import os
import logging
import time
import httpx
from google import genai
from google.genai import types


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
    padding: 0 24px 32px !important;
}
[data-testid="stMainBlockContainer"], [data-testid="stMain"] .block-container {
    padding-top: 0 !important;
}

.ih-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 0 -24px 22px;
    padding: 10px 24px;
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

.ih-hero { position: relative; text-align: center; margin: 0 auto 20px; }
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
    outline: none !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
div[data-testid="stTextArea"] [data-baseweb="textarea"]:hover { border-color: rgba(162, 155, 254, 0.55) !important; }
div[data-testid="stTextArea"] textarea {
    min-height: 110px !important;
    height: 110px !important;
    padding: 16px !important;
    border: 0 !important;
    background: rgba(7, 7, 15, 0.92) !important;
    color: var(--ih-white) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.55 !important;
    outline: none !important;
    box-shadow: none !important;
}
div[data-testid="stTextArea"] textarea::placeholder { color: #657088 !important; }
div[data-testid="stTextArea"] textarea:focus, div[data-testid="stTextArea"] textarea:focus-visible { outline: none !important; box-shadow: none !important; }
div[data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within {
    border-color: var(--ih-cyan) !important;
    box-shadow: 0 0 0 3px rgba(0, 207, 232, 0.12), inset 0 1px 0 rgba(255,255,255,0.03) !important;
}

div.stButton { display: flex; justify-content: center; margin-top: 16px; }
div.stButton > button {
    width: 100% !important;
    max-width: 520px !important;
    min-height: 60px !important;
    padding: 0 24px !important;
    border: 0 !important;
    border-radius: 18px !important;
    background: linear-gradient(110deg, #5846d8 0%, var(--ih-indigo) 38%, #12bfdc 72%, var(--ih-cyan) 100%) !important;
    background-size: 180% 180% !important;
    background-position: 0% 50% !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 10px 26px rgba(0, 207, 232, 0.18), 0 7px 20px rgba(108, 92, 231, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    transition: transform 0.2s ease, box-shadow 0.25s ease, filter 0.25s ease, background-position 0.35s ease !important;
}
div.stButton > button:hover { transform: translateY(-2px); background-position: 100% 50% !important; box-shadow: 0 13px 32px rgba(0, 207, 232, 0.28), 0 8px 24px rgba(108, 92, 231, 0.34) !important; filter: brightness(1.05); }
div.stButton > button:active { transform: scale(0.985); }
div.stButton > button:focus-visible { outline: 3px solid rgba(0, 207, 232, 0.35) !important; outline-offset: 3px; }
div.stButton > button:disabled { opacity: 0.52 !important; box-shadow: none !important; filter: saturate(0.65) !important; transform: none !important; }

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
.ih-loading-steps { display: grid; gap: 8px; max-width: 330px; margin: 18px auto 0; text-align: left; }
.ih-loading-step { display: flex; align-items: center; gap: 9px; color: #c7c4d7; font-size: 12px; animation: ih-step-in 0.45s ease both; }
.ih-loading-step:nth-child(2) { animation-delay: 0.1s; }
.ih-loading-step:nth-child(3) { animation-delay: 0.2s; }
.ih-loading-step:nth-child(4) { animation-delay: 0.3s; }
.ih-loading-step::before { content: '✓'; display: inline-grid; place-items: center; width: 17px; height: 17px; border: 1px solid rgba(0,207,232,0.3); border-radius: 50%; background: rgba(0,207,232,0.07); color: var(--ih-cyan); font-size: 10px; font-weight: 700; }
@keyframes ih-step-in { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
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
    [data-testid="stBlockContainer"] { padding-top: 0 !important; }
    .ih-nav { margin-bottom: 24px; }
    .ih-hero { margin-bottom: 22px; }
    .ih-report-shell, [data-testid="stVerticalBlockBorderWrapper"] { padding: 30px !important; }
}
@media (max-width: 520px) {
    [data-testid="stBlockContainer"] { padding: 0 16px 18px !important; }
    .ih-nav { margin: 0 -16px 16px; padding: 9px 16px; }
    .ih-product-label { font-size: 9px; }
    .ih-hero h1 { font-size: 30px; }
    .ih-hero p { font-size: 13px; }
    .ih-hero { margin-bottom: 16px; }
    .ih-badge { margin-bottom: 11px; }
    .ih-form-title { font-size: 16px; }
    div[data-testid="stTextArea"] textarea { min-height: 96px !important; height: 96px !important; padding: 14px !important; }
    div.stButton { margin-top: 14px; }
    div.stButton > button { max-width: none !important; min-height: 60px !important; }
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


logger = logging.getLogger(__name__)
RETRY_DELAYS_SECONDS = (2, 4, 8, 16)
MAX_GEMINI_ATTEMPTS = 5
MAX_RETRY_WINDOW_SECONDS = 60
GEMINI_REQUEST_TIMEOUT_MS = 30_000  # per-attempt cap so a hung request can't block retries forever


class GeminiRetryExhaustedError(Exception):
    """Raised when a temporary Gemini outage outlasts the bounded retry plan."""


def _is_retryable_gemini_error(error):
    """Prefer structured Gemini/HTTP error data; use text only when none exists."""
    # A request that hung and hit our own timeout is a temporary condition by
    # definition, not a permanent one. httpx timeout exceptions don't always
    # carry a usable message, so this is checked by type rather than text.
    if isinstance(error, (httpx.TimeoutException, httpx.ConnectError)):
        return True

    structured_values = []

    for source in (error, getattr(error, "response", None)):
        if source is None:
            continue
        for attribute in ("status_code", "status", "code", "error_code"):
            value = getattr(source, attribute, None)
            if value is not None:
                structured_values.append(value)

    if structured_values:
        for value in structured_values:
            if isinstance(value, int) and not isinstance(value, bool) and value == 503:
                return True
            normalized_value = str(value).strip().upper()
            if normalized_value in {"503", "UNAVAILABLE", "SERVICE_UNAVAILABLE"}:
                return True
        return False

    fallback_message = str(error).lower()
    temporary_markers = (
        "503",
        "service unavailable",
        "model is overloaded",
        "model is experiencing high demand",
        "temporary unavailable",
        "unavailable",
    )
    return any(marker in fallback_message for marker in temporary_markers)


def generate_content_with_retry(client, model, contents, on_retry=None):
    """Run the existing request with bounded backoff for temporary service failures only."""
    started_at = time.monotonic()

    for attempt in range(1, MAX_GEMINI_ATTEMPTS + 1):
        try:
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    http_options=types.HttpOptions(timeout=GEMINI_REQUEST_TIMEOUT_MS)
                ),
            )
        except Exception as error:
            if not _is_retryable_gemini_error(error):
                logger.exception("Non-retryable Gemini request failure on attempt %s", attempt)
                raise

            if attempt == MAX_GEMINI_ATTEMPTS:
                logger.exception("Temporary Gemini failure on final attempt %s", attempt)
                raise GeminiRetryExhaustedError() from error

            retry_delay = RETRY_DELAYS_SECONDS[attempt - 1]
            if time.monotonic() + retry_delay > started_at + MAX_RETRY_WINDOW_SECONDS:
                logger.exception(
                    "Gemini retry window expired after attempt %s; original error: %s",
                    attempt,
                    error,
                )
                raise GeminiRetryExhaustedError() from error

            logger.warning(
                "Temporary Gemini failure on attempt %s; retrying in %s seconds. Original error: %s",
                attempt,
                retry_delay,
                error,
            )
            if on_retry:
                on_retry(attempt)
            time.sleep(retry_delay)

if "app_state" not in st.session_state: st.session_state.app_state = "idle"
if "playbook_data" not in st.session_state: st.session_state.playbook_data = None


def render_loading_card(target, title, message):
    """Render the existing branded loading treatment with user-friendly status copy."""
    target.markdown(f"""
    <div class="ih-loading">
        <div class="ih-loading-icon">✦</div>
        <h2>{title}</h2>
        <p>{message}</p>
        <div class="ih-loading-steps">
            <div class="ih-loading-step">Understanding your idea</div>
            <div class="ih-loading-step">Identifying target users</div>
            <div class="ih-loading-step">Evaluating the opportunity</div>
            <div class="ih-loading-step">Building your execution roadmap</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


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
    user_idea = st.text_area("Concept Field", placeholder="Describe your startup concept here...", label_visibility="collapsed", height=110)
    if st.button("🚀 Generate AI Playbook →"):
        if not user_idea.strip(): st.warning("Please type an idea first!")
        else:
            st.session_state.app_state = "generating"
            st.session_state.current_idea = user_idea
            st.rerun()
    st.markdown('<p class="ih-form-note">Built for students, solo founders, and first-time entrepreneurs.</p>', unsafe_allow_html=True)

if st.session_state.app_state == "generating":
    loading_slot = st.empty()
    render_loading_card(
        loading_slot,
        "🧠 Analyzing your startup...",
        "Turning your idea into a clear path forward.",
    )

    def _update_loading_on_retry(attempt):
        """Advance the existing loading card as retries happen, so the screen never looks frozen."""
        next_attempt = attempt + 1
        stage_copy = {
            1: ("⚡ AI engine is busy...", "Retrying automatically..."),
            2: ("🔄 Retrying automatically...", f"Attempt {next_attempt} of {MAX_GEMINI_ATTEMPTS}"),
            3: ("🔄 Retrying automatically...", f"Attempt {next_attempt} of {MAX_GEMINI_ATTEMPTS}"),
            4: ("✨ Almost there...", f"Attempt {next_attempt} of {MAX_GEMINI_ATTEMPTS}"),
        }
        title, message = stage_copy.get(
            attempt, ("🔄 Retrying automatically...", f"Attempt {next_attempt} of {MAX_GEMINI_ATTEMPTS}")
        )
        render_loading_card(loading_slot, title, message)

    try:
        response = generate_content_with_retry(
            client=client,
            model="gemini-2.5-flash",
            on_retry=_update_loading_on_retry,
            contents=f"""
You are an experienced early-stage startup advisor. Produce a concise, rigorous, and actionable startup playbook for the idea below.

Startup idea: {st.session_state.current_idea}

Write for a founder who must decide what to validate and build next. Use crisp, direct language similar to an excellent YC, Sequoia, or First Round partner memo. Do not use hype, filler, greetings, generic encouragement, or phrases such as "Great idea", "This is exciting", or "As an AI". Do not repeat the idea unnecessarily. Be realistic about uncertainty: distinguish assumptions from facts, avoid invented market figures, and state practical ways to validate uncertain claims.

Return Markdown only. Use the following exact H1 headings, in this exact order. Do not omit a section. Use short paragraphs and focused bullets; use numbered steps where sequence matters. Do not use tables.

# Startup Snapshot
Give a concise description of the business, the customer, and the core job-to-be-done.

---

# Problem
Explain the real-world problem, who feels it, why current workarounds fail, and why it matters now.

---

# Target Customer
Cover the primary audience, secondary audience, and ideal early adopters. Make each segment specific enough to reach.

---

# Value Proposition
State the promised outcome, why users would choose it over alternatives, and the clearest differentiator.

---

# Market Opportunity
Assess relevant trends, likely demand signals, and realistic potential. Do not claim market size figures unless they are supplied; name the assumptions that need validation.

---

# Competitor Landscape
Identify likely categories of existing solutions, their strengths and weaknesses, and a defensible wedge for differentiation. Do not invent specific competitors unless they are widely obvious from the idea.

---

# MVP Roadmap
Provide Phase 1, Phase 2, and Phase 3. Clearly state what to build first, what to postpone, and the measurable outcome that unlocks the next phase.

---

# Recommended Tech Stack
Recommend Frontend, Backend, Database, AI, Hosting, Payments, and Analytics. For each, give one practical default choice and a brief reason. Mark components as optional where the MVP does not need them.

---

# Revenue Model
Evaluate subscriptions, freemium, marketplace, commission, and licensing where relevant. Recommend the best fit, explain why, and name a simple initial pricing test.

---

# Go-To-Market Plan
Provide concrete plans for the first 100 users and first 1,000 users. Cover community, content, partnerships, Product Hunt only if relevant, and a specific social strategy. Prioritize channels where the target customer already gathers.

---

# Risks
List the largest execution, market, technical, and founder risks. For each risk, give an early warning signal and a mitigation or test.

---

# 30-Day Action Plan
Organize concrete, achievable tasks into Week 1, Week 2, Week 3, and Week 4. Focus on validation and shipping evidence, not abstract planning.

---

# Final Verdict
Provide Overall potential, Difficulty, Time to MVP, Estimated validation speed, and Overall recommendation. Use calibrated language and a clear next decision.

Before finalizing, check: would a founder actually use this report to build and validate a startup? If not, replace vague advice with specific next actions.
"""
        )
        st.session_state.playbook_data = response.text
        st.session_state.app_state = "results"
        st.rerun()
    except GeminiRetryExhaustedError:
        loading_slot.empty()
        st.error("""🚦

IdeaHive AI is currently experiencing unusually high demand.

We automatically tried several times but Google's AI service is temporarily unavailable.

Please wait about one minute and try again.

Thank you for your patience.""")
        st.session_state.app_state = "idle"
    except Exception as e:
        loading_slot.empty()
        logger.exception("Gemini request stopped without retry: %s", e)
        st.error("IdeaHive AI could not process this request right now. Please check your input and try again.")
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
