import streamlit as st
import requests
import json
import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_groq(question, selected_cards):
    all_cards = fetch_all_cards()
    user_cards = [c for c in all_cards if c["card_name"] in selected_cards]
    context = json.dumps(user_cards, indent=2)
    prompt = f"""
You are an Indian credit card expert.
User has these cards: {context}
User question: {question}
Give a specific, actionable answer in 3-4 lines.
Tell them exactly which card to use and why.
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()
st.set_page_config(
    page_title="CardIQ — Smart Credit Card Advisor",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #080810;
    font-family: 'DM Sans', sans-serif;
    color: #E8E8F0;
}

/* Hide streamlit chrome */
#MainMenu, footer, header, .stDeployButton { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1200px !important; }

/* Animated background grid */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
}

/* Hero */
.hero-wrap {
    text-align: center;
    padding: 3rem 0 2.5rem;
    position: relative;
}
.hero-eyebrow {
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #6366F1;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.2);
    padding: 6px 16px;
    border-radius: 100px;
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(42px, 6vw, 72px);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -2px;
    color: #F0F0FF;
    margin-bottom: 16px;
}
.hero-title span {
    background: linear-gradient(135deg, #6366F1 0%, #A78BFA 50%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 17px;
    color: #6B6B8A;
    font-weight: 300;
    letter-spacing: 0.2px;
}

/* Stat pills */
.stat-row {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 28px;
    flex-wrap: wrap;
}
.stat-pill {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 100px;
    padding: 8px 20px;
    font-size: 13px;
    color: #9090B0;
}
.stat-pill strong { color: #E8E8F0; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    padding: 4px !important;
    gap: 2px !important;
    margin-bottom: 32px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6B6B8A !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(99,102,241,0.15) !important;
    color: #A78BFA !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* Section label */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #F0F0FF;
    margin-bottom: 6px;
}
.section-sub {
    font-size: 14px;
    color: #6B6B8A;
    margin-bottom: 24px;
}

/* Filter toggles */
.stToggle > label {
    color: #9090B0 !important;
    font-size: 13px !important;
}

/* Multiselect */
.stMultiSelect [data-baseweb="select"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
}
.stMultiSelect [data-baseweb="select"]:focus-within {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}
.stMultiSelect span[data-baseweb="tag"] {
    background: rgba(99,102,241,0.2) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 8px !important;
    color: #A78BFA !important;
}

/* Selected cards summary */
.wallet-summary {
    background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(167,139,250,0.05));
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px;
    padding: 20px 24px;
    margin: 20px 0;
    display: flex;
    align-items: center;
    gap: 16px;
}

/* CTA Button */
.stButton > button {
    background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 32px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 24px rgba(99,102,241,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.4) !important;
}

/* Card benefit block */
.benefit-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.benefit-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #6366F1, #A78BFA, #EC4899);
}
.benefit-card:hover {
    border-color: rgba(99,102,241,0.2);
}
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 6px;
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #F0F0FF;
}
.card-meta {
    font-size: 13px;
    color: #5A5A7A;
    margin-bottom: 24px;
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
}
.card-meta span {
    display: flex;
    align-items: center;
    gap: 5px;
}
.badge {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
    padding: 5px 12px;
    border-radius: 100px;
    text-transform: uppercase;
}
.badge-standard { background: rgba(16,185,129,0.1); color: #10B981; border: 1px solid rgba(16,185,129,0.2); }
.badge-premium { background: rgba(245,158,11,0.1); color: #F59E0B; border: 1px solid rgba(245,158,11,0.2); }
.badge-super { background: rgba(236,72,153,0.1); color: #EC4899; border: 1px solid rgba(236,72,153,0.2); }

.use-section-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.use-section-title.green { color: #10B981; }
.use-section-title.red { color: #F43F5E; }
.use-section-title.gold { color: #F59E0B; }

.chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 400;
    margin: 4px 4px 4px 0;
    line-height: 1.4;
}
.chip-use {
    background: rgba(16,185,129,0.08);
    color: #6EE7B7;
    border: 1px solid rgba(16,185,129,0.15);
}
.chip-avoid {
    background: rgba(244,63,94,0.08);
    color: #FDA4AF;
    border: 1px solid rgba(244,63,94,0.15);
}
.tip-box {
    background: rgba(245,158,11,0.06);
    border: 1px solid rgba(245,158,11,0.15);
    border-radius: 12px;
    padding: 14px 18px;
    margin-top: 20px;
    font-size: 14px;
    color: #FCD34D;
    line-height: 1.6;
}
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin: 20px 0;
}

/* Chat */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 20px;
    max-height: 480px;
    overflow-y: auto;
    padding-right: 8px;
}
.msg-user {
    display: flex;
    justify-content: flex-end;
}
.msg-ai {
    display: flex;
    justify-content: flex-start;
}
.bubble-user {
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    color: white;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 4px 16px rgba(99,102,241,0.3);
}
.bubble-ai {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: #D4D4E8;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    max-width: 75%;
    font-size: 14px;
    line-height: 1.6;
}
.ai-label {
    font-size: 11px;
    color: #6366F1;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.suggested-wrap {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}
.empty-state {
    text-align: center;
    padding: 60px 20px;
    background: rgba(255,255,255,0.02);
    border: 1px dashed rgba(255,255,255,0.08);
    border-radius: 20px;
}
.empty-icon { font-size: 40px; margin-bottom: 16px; }
.empty-title { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 700; color: #4A4A6A; margin-bottom: 8px; }
.empty-sub { font-size: 14px; color: #3A3A5A; }

/* Chat input */
.stChatInput { 
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
}
.stChatInput textarea {
    color: #E8E8F0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# ── Config ───────────────────────────────────────────────────
#API_URL = "http://localhost:8000"

# ── Load cards ───────────────────────────────────────────────
@st.cache_data
def fetch_all_cards():
    try:
        with open("data/cards.json") as f:
            return json.load(f)
    except:
        return []

# ── Session state ─────────────────────────────────────────────
if "selected_cards" not in st.session_state:
    st.session_state.selected_cards = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── Hero ──────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">AI-Powered · India's Cards · Real Savings</div>
    <div class="hero-title">Your wallet,<br><span>finally working for you</span></div>
    <div class="hero-sub">Know exactly which card to swipe — every time, everywhere</div>
    <div class="stat-row">
        <div class="stat-pill"><strong>99</strong> cards tracked</div>
        <div class="stat-pill"><strong>18</strong> Indian banks</div>
        <div class="stat-pill"><strong>AI</strong> powered advice</div>
        <div class="stat-pill"><strong>₹0</strong> cost, forever</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["💳  My Wallet", "📊  Benefits", "🤖  Ask CardIQ"])

# ════════════════════════════════════════════════════════════
# TAB 1 — MY WALLET
# ════════════════════════════════════════════════════════════
with tab1:
    all_cards = fetch_all_cards()

    if not all_cards:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">⚠️</div>
            <div class="empty-title">Cannot connect to API</div>
            <div class="empty-sub">Make sure <code>python api.py</code> is running in another terminal</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-label">Which cards are in your wallet?</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Select all cards you currently own — we\'ll show you how to maximise each one</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            show_premium = st.toggle("👑 Premium cards", value=True)
        with col2:
            show_super = st.toggle("💎 Super Premium", value=True)

        filtered = []
        for c in all_cards:
            tier = c.get("is_premium", False)
            if tier == "Super Premium" and not show_super:
                continue
            if tier is True and not show_premium:
                continue
            filtered.append(c)

        card_names = [c["card_name"] for c in filtered]

        selected = st.multiselect(
            "Search or select your cards:",
            options=card_names,
            default=[c for c in st.session_state.selected_cards if c in card_names],
            placeholder="Type a bank name or card name..."
        )
        st.session_state.selected_cards = selected

        if selected:
            tier_counts = {"Standard": 0, "Premium": 0, "Super Premium": 0}
            for c in all_cards:
                if c["card_name"] in selected:
                    t = c.get("is_premium", False)
                    if t == "Super Premium":
                        tier_counts["Super Premium"] += 1
                    elif t is True:
                        tier_counts["Premium"] += 1
                    else:
                        tier_counts["Standard"] += 1

            st.markdown(f"""
            <div class="wallet-summary">
                <div style="font-size:32px">💳</div>
                <div>
                    <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;color:#F0F0FF">
                        {len(selected)} card{'s' if len(selected)>1 else ''} selected
                    </div>
                    <div style="font-size:13px;color:#6B6B8A;margin-top:4px">
                        {tier_counts['Standard']} Standard &nbsp;·&nbsp;
                        {tier_counts['Premium']} Premium &nbsp;·&nbsp;
                        {tier_counts['Super Premium']} Super Premium
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.button("📊 View My Benefits →", use_container_width=True)
            st.markdown('<div style="text-align:center;font-size:13px;color:#3A3A5A;margin-top:8px">Switch to the Benefits tab to see your personalised savings plan</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state" style="margin-top:20px">
                <div class="empty-icon">👆</div>
                <div class="empty-title">No cards selected yet</div>
                <div class="empty-sub">Search for your card above to get started</div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# TAB 2 — BENEFITS
# ════════════════════════════════════════════════════════════
with tab2:
    if not st.session_state.selected_cards:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">💳</div>
            <div class="empty-title">No cards in your wallet yet</div>
            <div class="empty-sub">Head to the My Wallet tab and select your cards first</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        all_cards_data = fetch_all_cards()
        user_cards = [c for c in all_cards_data if c["card_name"] in st.session_state.selected_cards]

        st.markdown(f'<div class="section-label">Maximise your {len(user_cards)} card{"s" if len(user_cards)>1 else ""}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Every swipe optimised — know when to use each card and when to leave it in your wallet</div>', unsafe_allow_html=True)

        for card in user_cards:
            tier = card.get("is_premium", False)
            if tier == "Super Premium":
                badge = '<span class="badge badge-super">💎 Super Premium</span>'
            elif tier is True:
                badge = '<span class="badge badge-premium">👑 Premium</span>'
            else:
                badge = '<span class="badge badge-standard">✓ Standard</span>'

            use_cases = card.get("use_cases", {})
            when_to_use = use_cases.get("when_to_use", [])
            when_to_avoid = use_cases.get("when_to_avoid", [])
            tip = use_cases.get("max_savings_tip", "")

            if isinstance(when_to_use, str):
                when_to_use = [when_to_use]
            if isinstance(when_to_avoid, str):
                when_to_avoid = [when_to_avoid]

            use_chips = "".join([f'<span class="chip chip-use">✓ {u}</span>' for u in when_to_use])
            avoid_chips = "".join([f'<span class="chip chip-avoid">✕ {a}</span>' for a in when_to_avoid])

            lounge = use_cases.get('lounge_benefit', 'No lounge access')
            annual = use_cases.get('annual_math', 'N/A')    
            hidden = use_cases.get('hidden_costs', 'None')

            html = f"""
<div class="benefit-card">
    <div class="card-header">
        <div class="card-title">💳 {card['card_name']}</div>
        {badge}
    </div>
    <div class="card-meta">
        <span>💰 Annual Fee: ₹{card.get('annual_fee','N/A')}</span>
        <span>🎁 {card.get('reward_type','N/A')}</span>
        <span>🔄 Waiver at {card.get('fee_waiver','N/A')}</span>
    </div>
    <hr class="divider">
    <div class="use-section-title green">✅ USE THIS CARD WHEN</div>
    <div>{use_chips}</div>
    <div style="margin-top:20px">
        <div class="use-section-title red">❌ AVOID FOR</div>
        <div>{avoid_chips}</div>
    </div>
    <div style="margin-top:20px;display:flex;gap:12px;flex-wrap:wrap">
        <div style="flex:1;min-width:200px;background:rgba(99,102,241,0.06);border:1px solid rgba(99,102,241,0.15);border-radius:12px;padding:14px 18px">
            <div style="font-size:11px;font-weight:600;letter-spacing:2px;color:#818CF8;text-transform:uppercase;margin-bottom:8px">✈️ Lounge Access</div>
            <div style="font-size:14px;color:#C7D2FE">{lounge}</div>
        </div>
        <div style="flex:1;min-width:200px;background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.15);border-radius:12px;padding:14px 18px">
            <div style="font-size:11px;font-weight:600;letter-spacing:2px;color:#10B981;text-transform:uppercase;margin-bottom:8px">📊 Annual Math</div>
            <div style="font-size:14px;color:#6EE7B7">{annual}</div>
        </div>
    </div>
    <div style="margin-top:12px;background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.15);border-radius:12px;padding:14px 18px">
        <div style="font-size:11px;font-weight:600;letter-spacing:2px;color:#F87171;text-transform:uppercase;margin-bottom:8px">⚠️ Hidden Costs</div>
        <div style="font-size:14px;color:#FCA5A5">{hidden}</div>
    </div>
    <div class="tip-box">
        💡 <strong>Max Savings Tip:</strong> {tip}
    </div>
</div>
"""
            st.markdown(html, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# TAB 3 — ASK CARDIQ
# ════════════════════════════════════════════════════════════
with tab3:
    if not st.session_state.selected_cards:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🤖</div>
            <div class="empty-title">Select your cards first</div>
            <div class="empty-sub">Head to My Wallet, pick your cards, then come back to chat</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-label">Ask CardIQ anything</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-sub">Answering based on: <strong style="color:#A78BFA">{", ".join(st.session_state.selected_cards)}</strong></div>', unsafe_allow_html=True)

        # Suggested questions as buttons
        st.markdown("**Quick questions to get you started:**")
        cols = st.columns(3)
        suggestions = [
            "🍔 Best card for Swiggy tonight?",
            "⛽ Which card saves most on fuel?",
            "🛒 Best card for Amazon shopping?"
        ]
        for i, (col, q) in enumerate(zip(cols, suggestions)):
            with col:
                if st.button(q, key=f"sug_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    with st.spinner(""):
                      answer = ask_groq(q, st.session_state.selected_cards)
                    st.session_state.chat_history.append({"role": "ai", "content": answer})
                    st.rerun()

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # Chat history
        if st.session_state.chat_history:
            chat_html = '<div class="chat-container">'
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    chat_html += f'<div class="msg-user"><div class="bubble-user">{msg["content"]}</div></div>'
                else:
                    chat_html += f'<div class="msg-ai"><div class="bubble-ai"><div class="ai-label">CardIQ</div>{msg["content"]}</div></div>'
            chat_html += '</div>'
            st.markdown(chat_html, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:40px;color:#3A3A5A;font-size:14px">
                No conversation yet — ask a question above or use a quick suggestion 👆
            </div>
            """, unsafe_allow_html=True)

        # Chat input
        user_input = st.chat_input("Ask anything about your cards — e.g. 'I'm booking flights on MakeMyTrip, which card?'")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner("CardIQ is thinking..."):
                try:
                    res = requests.post(f"{API_URL}/chat", json={
                        "question": user_input,
                        "cards": st.session_state.selected_cards
                    }, timeout=15)
                    answer = res.json().get("answer", "Sorry, something went wrong.")
                except:
                    answer = "Could not reach the API. Make sure api.py is running."
            st.session_state.chat_history.append({"role": "ai", "content": answer})
            st.rerun()

        # Clear chat
        if st.session_state.chat_history:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("🗑️ Clear conversation", use_container_width=False):
                st.session_state.chat_history = []
                st.rerun()