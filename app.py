import truststore
import textwrap

# ============================================================
# HTTPS / CORPORATE NETWORK
# ============================================================

truststore.inject_into_ssl()

import streamlit as st

from src.pipelines.pipelines import run_research_pipeline


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SESSION STATE
# ============================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if "research_state" not in st.session_state:
    st.session_state.research_state = None

if "topic" not in st.session_state:
    st.session_state.topic = ""

if "pipeline_percent" not in st.session_state:
    st.session_state.pipeline_percent = 0


# ============================================================
# THEME COLORS
# ============================================================

dark = st.session_state.dark_mode

if dark:

    # --------------------------------------------------------
    # DARK THEME
    # --------------------------------------------------------

    BG = "#07111f"
    BG_SECONDARY = "#0a1729"

    CARD = "rgba(255,255,255,0.035)"
    CARD_ACTIVE = "rgba(56,189,248,0.065)"
    CARD_DONE = "rgba(34,197,94,0.045)"
    CARD_SOLID = "#101d32"

    TEXT = "#f8fbff"
    MUTED = "#aebed3"

    BORDER = "rgba(255,255,255,0.10)"
    BORDER_ACTIVE = "rgba(56,189,248,0.45)"
    BORDER_DONE = "rgba(34,197,94,0.30)"

    INPUT_BG = "#111f33"
    INPUT_BORDER = "#36516f"
    INPUT_BORDER_HOVER = "#4b6d92"

    INPUT_TEXT = "#f8fbff"
    INPUT_PLACEHOLDER = "#7f91a8"

    ACCENT = "#38bdf8"
    ACCENT_2 = "#8b5cf6"

    SUCCESS = "#22c55e"

    QUICK_BG = "#303a49"
    QUICK_HOVER = "#3b4758"
    QUICK_TEXT = "#e5edf7"

    FORM_BG = "rgba(255,255,255,0.018)"
    FORM_BORDER = "rgba(255,255,255,0.10)"

    # Results
    RESULT_TEXT = "#f8fbff"
    RESULT_MUTED = "#b7c6d9"
    TAB_TEXT = "#b7c6d9"
    TAB_ACTIVE = "#38bdf8"

else:

    # --------------------------------------------------------
    # LIGHT THEME
    # --------------------------------------------------------

    BG = "#f5f7fb"
    BG_SECONDARY = "#eef4ff"

    CARD = "rgba(255,255,255,0.88)"
    CARD_ACTIVE = "rgba(2,132,199,0.055)"
    CARD_DONE = "rgba(22,163,74,0.045)"
    CARD_SOLID = "#ffffff"

    TEXT = "#111827"
    MUTED = "#64748b"

    BORDER = "rgba(100,116,139,0.22)"
    BORDER_ACTIVE = "rgba(2,132,199,0.42)"
    BORDER_DONE = "rgba(22,163,74,0.28)"

    INPUT_BG = "#ffffff"
    INPUT_BORDER = "#b7c5d6"
    INPUT_BORDER_HOVER = "#8ca4be"

    INPUT_TEXT = "#111827"
    INPUT_PLACEHOLDER = "#64748b"

    ACCENT = "#0284c7"
    ACCENT_2 = "#7c3aed"

    SUCCESS = "#16a34a"

    QUICK_BG = "#e5e7eb"
    QUICK_HOVER = "#d1d5db"
    QUICK_TEXT = "#1f2937"

    FORM_BG = "rgba(255,255,255,0.72)"
    FORM_BORDER = "rgba(100,116,139,0.28)"

    # Results
    RESULT_TEXT = "#111827"
    RESULT_MUTED = "#475569"
    TAB_TEXT = "#64748b"
    TAB_ACTIVE = "#0284c7"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    html,
    body,
    [class*="css"] {{
        font-family:
            "Inter",
            "DM Sans",
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(
                circle at top left,
                rgba(0,191,255,0.14),
                transparent 32%
            ),
            radial-gradient(
                circle at bottom right,
                rgba(124,58,237,0.12),
                transparent 30%
            ),
            linear-gradient(
                180deg,
                {BG} 0%,
                {BG_SECONDARY} 100%
            );

        color: {TEXT};
        min-height: 100vh;
    }}

    .main .block-container {{
        max-width: 1280px;

        padding-top: 1.2rem;
        padding-bottom: 4rem;

        padding-left: 3rem;
        padding-right: 3rem;
    }}


    /* ======================================================
       STREAMLIT CHROME
       ====================================================== */

    #MainMenu,
    footer {{
        visibility: hidden;
    }}

    header[data-testid="stHeader"] {{
        background: transparent;
    }}

    section[data-testid="stSidebar"] {{
        display: none;
    }}


    /* ======================================================
       TOP BRAND
       ====================================================== */

    .brand-title {{
        font-size: 1rem !important;
        font-weight: 700 !important;

        color: {TEXT} !important;

        margin: 0 !important;
        padding: 0 !important;

        letter-spacing: -0.015em !important;
    }}

    .brand-caption {{
        font-size: 0.68rem !important;

        color: {MUTED} !important;

        margin: 2px 0 0 0 !important;
        padding: 0 !important;
    }}

    .brand-icon {{
        font-size: 1.15rem !important;
    }}


    /* ======================================================
       HERO
       ====================================================== */

    .hero-eyebrow {{
        text-align: center;

        font-family:
            "SFMono-Regular",
            "Roboto Mono",
            monospace;

        font-size: 0.66rem;

        font-weight: 600;

        letter-spacing: 0.24em;

        text-transform: uppercase;

        color: {ACCENT};

        margin-top: 2.4rem;
        margin-bottom: 0.95rem;
    }}

    .hero-title {{
        text-align: center;

        font-size:
            clamp(
                3rem,
                6vw,
                5.8rem
            );

        line-height: 0.98;

        font-weight: 700;

        letter-spacing: -0.045em;

        margin: 0;

        color: {TEXT};
    }}

    .hero-research {{
        color: {TEXT};
    }}

    .hero-agent {{
        background:
            linear-gradient(
                135deg,
                {ACCENT},
                #5d8fff,
                {ACCENT_2}
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    .hero-sub {{
        text-align: center;

        max-width: 650px;

        margin:
            1.1rem auto
            0 auto;

        color: {MUTED};

        font-size: 0.98rem;

        font-weight: 400;

        line-height: 1.65;
    }}

    .hero-divider {{
        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(56,189,248,0.30),
                transparent
            );

        margin:
            2.3rem 0
            2.6rem;
    }}


    /* ======================================================
       SECTION LABELS
       ====================================================== */

    .section-label {{
        font-family:
            "SFMono-Regular",
            "Roboto Mono",
            monospace;

        font-size: 0.66rem;

        font-weight: 600;

        letter-spacing: 0.20em;

        text-transform: uppercase;

        color: {ACCENT};

        margin-bottom: 0.55rem;
    }}

    .section-heading {{
        font-size: 1.35rem;

        font-weight: 700;

        letter-spacing: -0.025em;

        color: {TEXT};

        margin:
            0 0
            0.45rem 0;
    }}

    .section-description {{
        color: {MUTED};

        font-size: 0.82rem;

        line-height: 1.55;

        margin-bottom: 1.2rem;
    }}


    /* ======================================================
       RESEARCH FORM
       ====================================================== */

    div[data-testid="stForm"] {{
        background:
            {FORM_BG} !important;

        border:
            1px solid
            {FORM_BORDER} !important;

        border-radius:
            16px !important;

        padding:
            1.1rem 1.15rem
            1.2rem 1.15rem !important;

        box-shadow:
            0 10px 35px
            rgba(0,0,0,0.08);

        backdrop-filter:
            blur(10px);
    }}


    /* ======================================================
       RESEARCH INPUT LABEL
       ====================================================== */

    div[data-testid="stTextInput"] label {{
        color:
            {ACCENT} !important;

        font-family:
            "SFMono-Regular",
            "Roboto Mono",
            monospace !important;

        font-size:
            0.66rem !important;

        font-weight:
            600 !important;

        letter-spacing:
            0.15em !important;

        text-transform:
            uppercase !important;
    }}


    /* ======================================================
       RESEARCH INPUT
       ====================================================== */

    div[data-testid="stTextInput"]
    div[data-baseweb="input"] {{

        background:
            {INPUT_BG} !important;

        border:
            1.5px solid
            {INPUT_BORDER} !important;

        border-radius:
            12px !important;

        box-shadow:
            inset 0 1px 2px
            rgba(0,0,0,0.06) !important;

        transition:
            border-color 0.18s ease,
            box-shadow 0.18s ease !important;
    }}

    div[data-testid="stTextInput"]
    div[data-baseweb="input"]:hover {{
        border-color:
            {INPUT_BORDER_HOVER} !important;
    }}

    div[data-testid="stTextInput"]
    div[data-baseweb="input"]:focus-within {{
        border-color:
            {ACCENT} !important;

        box-shadow:
            0 0 0 3px
                rgba(56,189,248,0.14),
            inset 0 1px 2px
                rgba(0,0,0,0.04) !important;
    }}

    div[data-testid="stTextInput"] input[type="text"] {{

        background:
            {INPUT_BG} !important;

        color:
            {INPUT_TEXT} !important;

        -webkit-text-fill-color:
            {INPUT_TEXT} !important;

        caret-color:
            {ACCENT} !important;

        font-family:
            "Inter",
            "DM Sans",
            sans-serif !important;

        font-size:
            0.95rem !important;

        font-weight:
            400 !important;

        min-height:
            46px !important;

        padding:
            0.75rem 1rem !important;

        opacity:
            1 !important;
    }}

    div[data-testid="stTextInput"]
    input[type="text"]::placeholder {{
        color:
            {INPUT_PLACEHOLDER} !important;

        -webkit-text-fill-color:
            {INPUT_PLACEHOLDER} !important;

        opacity:
            1 !important;
    }}


    /* ======================================================
       PRIMARY RUN BUTTON
       ====================================================== */

    .stFormSubmitButton > button {{

        width:
            100% !important;

        min-height:
            48px !important;

        border:
            none !important;

        border-radius:
            12px !important;

        background:
            linear-gradient(
                135deg,
                {ACCENT},
                #6487ff,
                {ACCENT_2}
            ) !important;

        color:
            white !important;

        font-size:
            0.90rem !important;

        font-weight:
            700 !important;

        letter-spacing:
            0.01em !important;

        box-shadow:
            0 8px 26px
            rgba(56,189,248,0.18) !important;

        transition:
            all 0.18s ease !important;
    }}

    .stFormSubmitButton > button:hover {{
        transform:
            translateY(-1px) !important;

        box-shadow:
            0 12px 32px
            rgba(56,189,248,0.25) !important;
    }}


    /* ======================================================
       CLEAR BUTTON
       ====================================================== */

    .clear-button-container {{
        margin-top:
            0.55rem;
    }}

    .clear-button-container button {{
        width:
            auto !important;

        min-height:
            34px !important;

        padding:
            0.25rem
            0.85rem !important;

        border-radius:
            8px !important;

        border:
            1px solid
            {BORDER} !important;

        background:
            transparent !important;

        color:
            {MUTED} !important;

        font-size:
            0.72rem !important;

        font-weight:
            500 !important;

        box-shadow:
            none !important;
    }}

    .clear-button-container button:hover {{
        background:
            {QUICK_BG} !important;

        color:
            {TEXT} !important;

        border-color:
            {INPUT_BORDER_HOVER} !important;
    }}


    /* ======================================================
       QUICK TOPICS
       ====================================================== */

    .try-label {{
        font-family:
            "SFMono-Regular",
            "Roboto Mono",
            monospace;

        font-size:
            0.65rem;

        letter-spacing:
            0.12em;

        color:
            {MUTED};

        margin:
            1rem 0
            0.55rem;
    }}

    div[data-testid="stButton"] > button {{

        min-height:
            38px !important;

        padding:
            0.45rem
            0.8rem !important;

        border-radius:
            9px !important;

        background:
            {QUICK_BG} !important;

        color:
            {QUICK_TEXT} !important;

        border:
            1px solid
            {BORDER} !important;

        box-shadow:
            none !important;

        font-size:
            0.74rem !important;

        font-weight:
            500 !important;

        transition:
            all 0.15s ease !important;
    }}

    div[data-testid="stButton"] > button:hover {{
        background:
            {QUICK_HOVER} !important;

        color:
            {QUICK_TEXT} !important;

        border-color:
            {ACCENT} !important;

        transform:
            translateY(-1px) !important;
    }}


    /* ======================================================
       PIPELINE TITLE
       ====================================================== */

    .pipeline-title {{
        font-size:
            1.35rem;

        font-weight:
            700;

        letter-spacing:
            -0.025em;

        color:
            {TEXT};

        margin:
            0;
    }}

    .pipeline-live {{
        color:
            {MUTED};

        font-family:
            "SFMono-Regular",
            "Roboto Mono",
            monospace;

        font-size:
            0.62rem;

        letter-spacing:
            0.10em;

        text-transform:
            uppercase;

        text-align:
            right;
    }}


    /* ======================================================
       PIPELINE CARDS
       ====================================================== */

    .pipeline-wrapper {{
        width:
            100%;
    }}

    .pipeline-card {{

        position:
            relative;

        width:
            100%;

        box-sizing:
            border-box;

        border-radius:
            18px;

        border:
            1px solid
            {BORDER};

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.045),
                rgba(255,255,255,0.018)
            );

        padding:
            1.25rem
            1.35rem;

        margin-bottom:
            0.85rem;

        overflow:
            hidden;

        backdrop-filter:
            blur(14px);

        -webkit-backdrop-filter:
            blur(14px);

        box-shadow:
            inset 0 1px 0
                rgba(255,255,255,0.035),
            inset 0 0 30px
                rgba(255,255,255,0.012),
            0 12px 30px
                rgba(0,0,0,0.12);

        transition:
            all 0.20s ease;
    }}

    .pipeline-card:hover {{

        transform:
            translateY(-2px);

        border-color:
            rgba(56,189,248,0.22);

        box-shadow:
            inset 0 1px 0
                rgba(255,255,255,0.045),
            0 16px 35px
                rgba(0,0,0,0.16);
    }}

    .pipeline-card.active {{

        background:
            linear-gradient(
                135deg,
                rgba(56,189,248,0.085),
                rgba(59,130,246,0.045),
                rgba(124,58,237,0.035)
            );

        border-color:
            {BORDER_ACTIVE};

        box-shadow:
            inset 0 1px 0
                rgba(255,255,255,0.045),
            inset 0 0 36px
                rgba(56,189,248,0.035),
            0 0 0 1px
                rgba(56,189,248,0.06),
            0 14px 34px
                rgba(8,145,178,0.13);
    }}

    .pipeline-card.active:hover {{
        border-color:
            rgba(56,189,248,0.60);

        box-shadow:
            inset 0 1px 0
                rgba(255,255,255,0.05),
            0 0 0 1px
                rgba(56,189,248,0.08),
            0 18px 40px
                rgba(8,145,178,0.18);
    }}

    .pipeline-card.done {{

        background:
            linear-gradient(
                135deg,
                rgba(34,197,94,0.055),
                rgba(255,255,255,0.018)
            );

        border-color:
            {BORDER_DONE};

        box-shadow:
            inset 0 1px 0
                rgba(255,255,255,0.035),
            inset 0 0 28px
                rgba(34,197,94,0.018),
            0 10px 26px
                rgba(0,0,0,0.10);
    }}

    .pipeline-card::before {{

        content:
            "";

        position:
            absolute;

        left:
            0;

        top:
            0;

        bottom:
            0;

        width:
            3px;

        background:
            rgba(255,255,255,0.035);

        border-radius:
            18px 0 0 18px;
    }}

    .pipeline-card.active::before {{

        width:
            4px;

        background:
            linear-gradient(
                180deg,
                {ACCENT},
                #4f9cff,
                {ACCENT_2}
            );

        box-shadow:
            0 0 14px
            rgba(56,189,248,0.55);
    }}

    .pipeline-card.done::before {{

        width:
            4px;

        background:
            linear-gradient(
                180deg,
                #22c55e,
                #10b981
            );

        box-shadow:
            0 0 12px
            rgba(34,197,94,0.30);
    }}

    .pipeline-header {{
        display:
            flex;

        align-items:
            center;

        gap:
            0.75rem;

        width:
            100%;
    }}

    .pipeline-number {{
        flex:
            0 0 auto;

        font-family:
            "SFMono-Regular",
            "Roboto Mono",
            monospace;

        font-size:
            0.67rem;

        font-weight:
            600;

        letter-spacing:
            0.12em;

        color:
            {ACCENT};

        min-width:
            2rem;
    }}

    .pipeline-name {{
        font-size:
            0.96rem;

        font-weight:
            700;

        color:
            {TEXT};

        letter-spacing:
            -0.012em;
    }}

    .pipeline-status {{
        margin-left:
            auto;

        flex:
            0 0 auto;

        font-family:
            "SFMono-Regular",
            "Roboto Mono",
            monospace;

        font-size:
            0.59rem;

        font-weight:
            600;

        letter-spacing:
            0.09em;

        white-space:
            nowrap;
    }}

    .status-waiting {{
        color:
            #718198;
    }}

    .status-running {{
        color:
            {ACCENT};

        text-shadow:
            0 0 10px
            rgba(56,189,248,0.25);
    }}

    .status-done {{
        color:
            {SUCCESS};

        text-shadow:
            0 0 10px
            rgba(34,197,94,0.18);
    }}

    .pipeline-description {{
        margin-left:
            2.75rem;

        margin-top:
            0.42rem;

        color:
            {MUTED};

        font-size:
            0.74rem;

        line-height:
            1.45;
    }}


    /* ======================================================
       RESULTS - MAIN TEXT
       ====================================================== */

    /*
       Streamlit's Markdown renderer inherits some of its
       colors from the browser/theme. We explicitly override
       them so the report is readable in both themes.
    */

    [data-testid="stMarkdownContainer"] {{
        color:
            {RESULT_TEXT} !important;
    }}

    [data-testid="stMarkdownContainer"] p {{
        color:
            {RESULT_TEXT} !important;

        line-height:
            1.7 !important;
    }}

    [data-testid="stMarkdownContainer"] li {{
        color:
            {RESULT_TEXT} !important;

        line-height:
            1.65 !important;
    }}

    [data-testid="stMarkdownContainer"] strong {{
        color:
            {RESULT_TEXT} !important;
    }}

    [data-testid="stMarkdownContainer"] em {{
        color:
            {RESULT_TEXT} !important;
    }}

    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {{
        color:
            {RESULT_TEXT} !important;
    }}

    [data-testid="stMarkdownContainer"] a {{
        color:
            {ACCENT} !important;
    }}

    [data-testid="stMarkdownContainer"] code {{
        color:
            {RESULT_TEXT} !important;
    }}


    /* ======================================================
       RESULT CONTAINERS
       ====================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-color:
            {BORDER} !important;

        border-radius:
            16px !important;

        background:
            {CARD} !important;
    }}


    /* ======================================================
       RESULT PANEL LABEL
       ====================================================== */

    .panel-label {{
        font-family:
            "SFMono-Regular",
            "Roboto Mono",
            monospace;

        font-size:
            0.68rem;

        letter-spacing:
            0.2em;

        text-transform:
            uppercase;

        padding-bottom:
            0.7rem;

        margin-bottom:
            1rem;
    }}

    .panel-label.blue {{
        color:
            {ACCENT};

        border-bottom:
            1px solid
            rgba(56,189,248,0.15);
    }}

    .panel-label.green {{
        color:
            {SUCCESS};

        border-bottom:
            1px solid
            rgba(34,197,94,0.15);
    }}


    /* ======================================================
       RESULT TABS
       ====================================================== */

    .stTabs [data-baseweb="tab-list"] {{
        gap:
            1.5rem !important;

        border-bottom:
            1px solid
            {BORDER} !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        color:
            {TAB_TEXT} !important;

        font-weight:
            600 !important;

        font-size:
            0.90rem !important;

        padding:
            0.55rem 0.15rem !important;
    }}

    .stTabs [data-baseweb="tab"] > div {{
        color:
            {TAB_TEXT} !important;
    }}

    .stTabs [data-baseweb="tab"] p {{
        color:
            {TAB_TEXT} !important;
    }}

    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        color:
            {TAB_ACTIVE} !important;
    }}

    .stTabs [data-baseweb="tab"][aria-selected="true"] > div,
    .stTabs [data-baseweb="tab"][aria-selected="true"] p {{
        color:
            {TAB_ACTIVE} !important;
    }}

    .stTabs [data-baseweb="tab-highlight"] {{
        background:
            {TAB_ACTIVE} !important;

        height:
            3px !important;

        border-radius:
            3px !important;
    }}

    .stTabs [data-baseweb="tab-border"] {{
        background:
            {BORDER} !important;
    }}


    /* ======================================================
       EXPANDERS
       ====================================================== */

    details {{
        background:
            {CARD} !important;

        border:
            1px solid
            {BORDER} !important;

        border-radius:
            12px !important;
    }}

    details summary {{
        color:
            {RESULT_TEXT} !important;
    }}


    /* ======================================================
       DOWNLOAD BUTTON
       ====================================================== */

    div[data-testid="stDownloadButton"] button {{
        border:
            1px solid
            {BORDER} !important;

        border-radius:
            10px !important;

        background:
            {CARD_SOLID} !important;

        color:
            {TEXT} !important;

        font-weight:
            600 !important;
    }}


    /* ======================================================
       INFO / STATUS
       ====================================================== */

    div[data-testid="stAlert"] {{
        border-radius:
            12px !important;
    }}


    /* ======================================================
       PROGRESS
       ====================================================== */

    div[data-testid="stProgressBar"] > div > div {{
        background:
            linear-gradient(
                90deg,
                {ACCENT},
                {ACCENT_2}
            ) !important;
    }}


    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 900px) {{

        .main .block-container {{
            padding-left:
                1.2rem;

            padding-right:
                1.2rem;
        }}

        .hero-title {{
            font-size:
                3.4rem;
        }}

        .pipeline-card {{
            padding:
                1rem;
        }}

        .pipeline-description {{
            margin-left:
                2.5rem;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap:
                0.7rem !important;
        }}
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# TOP BAR
# ============================================================

top_left, top_right = st.columns(
    [8, 1],
    vertical_alignment="center",
)

with top_left:

    brand_icon_col, brand_text_col = st.columns(
        [0.35, 5],
        vertical_alignment="center",
    )

    with brand_icon_col:

        st.markdown(
            '<div class="brand-icon">🔬</div>',
            unsafe_allow_html=True,
        )

    with brand_text_col:

        st.markdown(
            '<div class="brand-title">Research Agent</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="brand-caption">'
            'Multi-agent research workspace'
            '</div>',
            unsafe_allow_html=True,
        )


with top_right:

    theme_toggle = st.toggle(
        "Dark mode",
        value=st.session_state.dark_mode,
        label_visibility="collapsed",
        help="Toggle dark / light theme",
    )

    if theme_toggle != st.session_state.dark_mode:

        st.session_state.dark_mode = theme_toggle

        st.rerun()


# ============================================================
# HERO
# ============================================================

st.html(
    textwrap.dedent(
        """
        <div class="hero-eyebrow">
            MULTI-AGENT AI SYSTEM
        </div>

        <div class="hero-title">
            <span class="hero-research">Research</span>
            <span class="hero-agent"> Agent</span>
        </div>

        <div class="hero-sub">
            Search the web, analyze reliable sources, generate
            a structured research report, and review the result
            with AI-powered reasoning.
        </div>
        """
    ).strip()
)

st.html(
    '<div class="hero-divider"></div>'
)


# ============================================================
# MAIN WORKSPACE
# ============================================================

left_col, right_col = st.columns(
    [5, 4],
    gap="large",
)


# ============================================================
# LEFT - RESEARCH INPUT
# ============================================================

with left_col:

    st.markdown(
        '<div class="section-label">RESEARCH TOPIC</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-heading">'
        'What should we research?'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'Ask a focused question or describe a topic you want '
        'the research pipeline to investigate.'
        '</div>',
        unsafe_allow_html=True,
    )


    # ========================================================
    # RESEARCH FORM
    # ========================================================

    with st.form(
        "research_form",
        clear_on_submit=False,
    ):

        topic_form = st.text_input(
            "Research Topic",
            value=st.session_state.topic,
            placeholder=(
                "e.g. Roadmap for AGI development "
                "in next 5 years"
            ),
        )

        submitted = st.form_submit_button(
            "⚡  Run Research Pipeline",
            use_container_width=True,
        )


    # ========================================================
    # CLEAR BUTTON
    # ========================================================

    clear_col_1, clear_col_2 = st.columns(
        [1, 5]
    )

    with clear_col_1:

        st.markdown(
            '<div class="clear-button-container">',
            unsafe_allow_html=True,
        )

        clear_clicked = st.button(
            "✕ Clear",
            key="clear_research",
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )

    if clear_clicked:

        st.session_state.topic = ""
        st.session_state.research_state = None
        st.session_state.pipeline_percent = 0

        st.rerun()


    # ========================================================
    # QUICK TOPICS
    # ========================================================

    st.markdown(
        '<div class="try-label">TRY →</div>',
        unsafe_allow_html=True,
    )

    quick_topics = [
        "Future of LLM in Tech Industry",
        "All Latest AI Agents in 2026",
        "Roadmap for AGI development in next 5 years",
    ]

    for index, quick_topic in enumerate(quick_topics):

        clicked = st.button(
            quick_topic,
            key=f"quick_topic_{index}",
        )

        if clicked:

            st.session_state.topic = quick_topic

            st.rerun()


# ============================================================
# RIGHT - PIPELINE
# ============================================================

with right_col:

    title_col, badge_col = st.columns(
        [4, 1],
        vertical_alignment="center",
    )

    with title_col:

        st.markdown(
            '<div class="pipeline-title">Pipeline</div>',
            unsafe_allow_html=True,
        )

    with badge_col:

        st.markdown(
            '<div class="pipeline-live">LIVE</div>',
            unsafe_allow_html=True,
        )

    pipeline_placeholder = st.empty()


    # ========================================================
    # STATUS HELPER
    # ========================================================

    def get_step_status(
        step_number: int,
        percent: int,
    ) -> str:

        ranges = {
            1: (0, 30),
            2: (30, 65),
            3: (65, 80),
            4: (80, 101),
        }

        low, high = ranges[step_number]

        if percent >= high:
            return "done"

        if low <= percent < high:
            return "running"

        return "waiting"


    # ========================================================
    # PIPELINE RENDERER
    # ========================================================

    def render_pipeline(
        percent: int,
    ):

        steps = [
            (
                "01",
                "Web Search",
                "Find relevant and recent sources",
            ),
            (
                "02",
                "Source Analysis",
                "Scrape and extract useful content",
            ),
            (
                "03",
                "Writer",
                "Generate the research report",
            ),
            (
                "04",
                "Critic",
                "Review and score the report",
            ),
        ]

        pipeline_html = """
        <div class="pipeline-wrapper">
        """

        for index, (
            number,
            name,
            description,
        ) in enumerate(
            steps,
            start=1,
        ):

            status = get_step_status(
                index,
                percent,
            )

            if status == "running":

                status_text = "● RUNNING"
                status_class = "status-running"
                card_class = "active"

            elif status == "done":

                status_text = "✓ DONE"
                status_class = "status-done"
                card_class = "done"

            else:

                status_text = "WAITING"
                status_class = "status-waiting"
                card_class = ""

            pipeline_html += f"""
            <div class="pipeline-card {card_class}">

                <div class="pipeline-header">

                    <div class="pipeline-number">
                        {number}
                    </div>

                    <div class="pipeline-name">
                        {name}
                    </div>

                    <div class="pipeline-status {status_class}">
                        {status_text}
                    </div>

                </div>

                <div class="pipeline-description">
                    {description}
                </div>

            </div>
            """

        pipeline_html += """
        </div>
        """

        with pipeline_placeholder:

            st.html(
                textwrap.dedent(
                    pipeline_html
                ).strip()
            )


    render_pipeline(
        st.session_state.pipeline_percent
    )


# ============================================================
# EXECUTE PIPELINE
# ============================================================

if submitted:

    topic_value = topic_form.strip()

    if not topic_value:

        st.warning(
            "Please enter a research topic."
        )

    else:

        st.session_state.topic = topic_value
        st.session_state.pipeline_percent = 10

        status_container = st.empty()

        progress_bar = st.progress(
            0,
            text="Starting research...",
        )


        # ====================================================
        # PROGRESS CALLBACK
        # ====================================================

        def update_ui(
            message: str,
            percent: int,
        ):

            st.session_state.pipeline_percent = percent

            status_container.info(
                message
            )

            progress_bar.progress(
                percent,
                text=message,
            )

            render_pipeline(
                percent
            )


        # ====================================================
        # RUN PIPELINE
        # ====================================================

        try:

            result = run_research_pipeline(
                topic=topic_value,
                progress_callback=update_ui,
            )

            st.session_state.research_state = result
            st.session_state.pipeline_percent = 100

            render_pipeline(100)

            progress_bar.progress(
                100,
                text="Research completed successfully.",
            )

            status_container.success(
                "Research completed successfully."
            )

        except Exception as e:

            status_container.error(
                "Research pipeline failed."
            )

            st.exception(e)


# ============================================================
# RESULTS
# ============================================================

if st.session_state.research_state:

    state = st.session_state.research_state

    st.html(
        '<div class="hero-divider"></div>'
    )

    st.markdown(
        '<div class="section-heading">Results</div>',
        unsafe_allow_html=True,
    )


    # ========================================================
    # TABS
    # ========================================================

    tab_report, tab_sources, tab_scraped, tab_critic = st.tabs(
        [
            "📄 Report",
            "🔗 Sources",
            "🌐 Scraped Content",
            "🧠 Critic",
        ]
    )


    # ========================================================
    # REPORT
    # ========================================================

    with tab_report:

        report = state.get(
            "report",
            "No report available.",
        )

        with st.container(
            border=True,
        ):

            st.markdown(
                '<div class="panel-label blue">'
                '📝 FINAL RESEARCH REPORT'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                report
            )

        st.download_button(
            label="⬇ Download Report (.md)",
            data=report,
            file_name="research_report.md",
            mime="text/markdown",
        )


    # ========================================================
    # SOURCES
    # ========================================================

    with tab_sources:

        search_results = state.get(
            "search_results",
            "",
        )

        if not search_results:

            st.info(
                "No sources available."
            )

        elif isinstance(
            search_results,
            str,
        ):

            with st.container(
                border=True,
            ):

                st.markdown(
                    search_results
                )

        else:

            for index, source in enumerate(
                search_results,
                start=1,
            ):

                title = source.get(
                    "title",
                    "Untitled source",
                )

                url = source.get(
                    "url",
                    "",
                )

                content = source.get(
                    "content",
                    "",
                )

                with st.container(
                    border=True,
                ):

                    st.markdown(
                        f"### {index}. {title}"
                    )

                    if url:

                        st.caption(
                            url
                        )

                    st.write(
                        content
                    )


    # ========================================================
    # SCRAPED CONTENT
    # ========================================================

    with tab_scraped:

        scraped_content = state.get(
            "scraped_content",
            "",
        )

        if not scraped_content:

            st.info(
                "No scraped content available."
            )

        elif isinstance(
            scraped_content,
            str,
        ):

            with st.container(
                border=True,
            ):

                st.markdown(
                    scraped_content
                )

        else:

            for index, source in enumerate(
                scraped_content,
                start=1,
            ):

                title = source.get(
                    "title",
                    f"Source {index}",
                )

                url = source.get(
                    "url",
                    "",
                )

                content = source.get(
                    "scraped_content",
                    "",
                )

                with st.expander(
                    f"{index}. {title}",
                    expanded=False,
                ):

                    if url:

                        st.caption(
                            url
                        )

                    st.write(
                        content
                    )


    # ========================================================
    # CRITIC
    # ========================================================

    with tab_critic:

        feedback = state.get(
            "feedback",
            "No critic feedback available.",
        )

        with st.container(
            border=True,
        ):

            st.markdown(
                '<div class="panel-label green">'
                '🧐 CRITIC FEEDBACK'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                feedback
            )


# ============================================================
# FOOTER
# ============================================================

st.html(
    '<div class="hero-divider"></div>'
)

st.markdown(
    """
    <div style="
        text-align:center;
        color:#7f93ad;
        font-size:0.68rem;
        letter-spacing:0.08em;
        margin-top:1.5rem;
        padding-bottom:1rem;
    ">
        Research Agent · LangChain · Tavily · Ollama
    </div>
    """,
    unsafe_allow_html=True,
)