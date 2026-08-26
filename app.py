import truststore

# Must be initialized before importing modules that make HTTPS calls.
truststore.inject_into_ssl()

import streamlit as st

from src.pipelines.pipelines import run_research_pipeline


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResearcherAgent",
    page_icon="🔎",
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

if "pipeline_message" not in st.session_state:
    st.session_state.pipeline_message = ""


# ============================================================
# THEME COLORS
# ============================================================

dark = st.session_state.dark_mode

if dark:
    BG = "#07111f"
    BG_SECONDARY = "#0b1730"
    CARD = "#101d32"
    CARD_HOVER = "#142640"

    TEXT = "#f8fafc"
    MUTED = "#93a4bd"
    BORDER = "#263a57"

    INPUT_BG = "#101b2d"

    ACCENT = "#56c8ff"
    ACCENT_2 = "#7b63f6"

    SUCCESS = "#47c990"

    # Quick suggestion buttons
    QUICK_BG = "#2b3442"
    QUICK_HOVER = "#374151"
    QUICK_TEXT = "#f1f5f9"

else:
    BG = "#f5f7fb"
    BG_SECONDARY = "#eef4ff"
    CARD = "#ffffff"
    CARD_HOVER = "#f7faff"

    TEXT = "#111827"
    MUTED = "#64748b"
    BORDER = "#dbe4ef"

    INPUT_BG = "#ffffff"

    ACCENT = "#2196f3"
    ACCENT_2 = "#7657e8"

    SUCCESS = "#15966c"

    # Quick suggestion buttons
    QUICK_BG = "#e5e7eb"
    QUICK_HOVER = "#d1d5db"
    QUICK_TEXT = "#1f2937"


# ============================================================
# CUSTOM CSS
#
# IMPORTANT:
# Only CSS is injected here.
# We do NOT use custom HTML <div> blocks for the UI.
# ============================================================

st.markdown(
    f"""
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {{
        background:
            radial-gradient(
                circle at 5% 15%,
                rgba(22, 130, 190, 0.18),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 55%,
                rgba(100, 78, 200, 0.12),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                {BG} 0%,
                {BG_SECONDARY} 100%
            );

        color: {TEXT};
        min-height: 100vh;
    }}

    .main .block-container {{
        max-width: 1400px;
        padding-top: 1rem;
        padding-bottom: 4rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }}


    /* ======================================================
       HIDE SIDEBAR / MENU / FOOTER
       ====================================================== */

    section[data-testid="stSidebar"] {{
        display: none;
    }}

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    header[data-testid="stHeader"] {{
        background: transparent;
    }}


    /* ======================================================
       TOP BRAND
       ====================================================== */

    .brand-text {{
        font-size: 1rem !important;
        font-weight: 700 !important;
        color: {TEXT} !important;
        margin-bottom: 0 !important;
    }}

    .brand-caption {{
        color: {MUTED} !important;
        font-size: 0.72rem !important;
    }}


    /* ======================================================
       HERO
       ====================================================== */

    .hero-small {{
        text-align: center;

        color: {ACCENT} !important;

        font-size: 0.72rem !important;
        font-weight: 800 !important;

        letter-spacing: 0.25em !important;

        margin-top: 1.5rem !important;
        margin-bottom: 0.8rem !important;
    }}

    .hero-title {{
        text-align: center !important;

        font-size: clamp(
            3.8rem,
            7vw,
            6.5rem
        ) !important;

        line-height: 0.95 !important;

        font-weight: 850 !important;

        letter-spacing: -0.055em !important;

        margin-top: 0 !important;
        margin-bottom: 0.8rem !important;

        background:
            linear-gradient(
                100deg,
                #38c8ff 5%,
                #6fa4ff 45%,
                #8a63f4 100%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    .hero-description {{
        text-align: center !important;

        max-width: 760px;

        margin-left: auto !important;
        margin-right: auto !important;

        color: {MUTED} !important;

        font-size: 1rem !important;
        line-height: 1.7 !important;
    }}


    /* ======================================================
       SECTION TITLES
       ====================================================== */

    .section-label {{
        color: {ACCENT} !important;

        font-size: 0.72rem !important;

        font-weight: 800 !important;

        letter-spacing: 0.18em !important;

        text-transform: uppercase !important;
    }}

    .section-heading {{
        color: {TEXT} !important;

        font-size: 1.5rem !important;

        font-weight: 750 !important;

        margin-bottom: 0 !important;
    }}

    .section-description {{
        color: {MUTED} !important;

        font-size: 0.84rem !important;

        line-height: 1.5 !important;
    }}


    /* ======================================================
       INPUT
       ====================================================== */

    div[data-baseweb="input"] {{
        background: {INPUT_BG} !important;

        border: 1px solid {BORDER} !important;

        border-radius: 14px !important;
    }}

    div[data-baseweb="input"]:focus-within {{
        border-color: {ACCENT} !important;

        box-shadow:
            0 0 0 1px {ACCENT} !important;
    }}

    div[data-baseweb="input"] input {{
        color: {TEXT} !important;

        font-size: 1rem !important;
    }}

    div[data-baseweb="input"] input::placeholder {{
        color: {MUTED} !important;
    }}


    /* ======================================================
       PRIMARY BUTTON
       ====================================================== */

    .stFormSubmitButton > button {{
        min-height: 50px !important;

        border-radius: 13px !important;

        border: none !important;

        background:
            linear-gradient(
                100deg,
                {ACCENT},
                #6585ff,
                {ACCENT_2}
            ) !important;

        color: white !important;

        font-weight: 750 !important;

        font-size: 0.95rem !important;

        box-shadow:
            0 10px 25px
            rgba(84, 137, 241, 0.23) !important;
    }}

    .stFormSubmitButton > button:hover {{
        transform: translateY(-1px);

        box-shadow:
            0 14px 30px
            rgba(84, 137, 241, 0.30) !important;
    }}


    /* ======================================================
       QUICK TOPIC BUTTONS
       ====================================================== */

    div[data-testid="stButton"] > button {{
        min-height: 40px !important;

        background: {QUICK_BG} !important;

        color: {QUICK_TEXT} !important;

        border: 1px solid {BORDER} !important;

        border-radius: 10px !important;

        box-shadow: none !important;

        font-size: 0.77rem !important;

        font-weight: 600 !important;

        transition:
            background 0.15s ease,
            border-color 0.15s ease,
            transform 0.15s ease !important;
    }}

    div[data-testid="stButton"] > button:hover {{
        background: {QUICK_HOVER} !important;

        color: {QUICK_TEXT} !important;

        border-color: {ACCENT} !important;

        transform: translateY(-1px);
    }}

    /* ======================================================
       PIPELINE CARDS
       ====================================================== */

    .pipeline-card {{
        background: {CARD};

        border: 1px solid {BORDER};

        border-radius: 16px;

        padding: 0.95rem 1.1rem;

        margin-bottom: 0.7rem;
    }}

    .pipeline-active {{
        border-color: {ACCENT} !important;

        box-shadow:
            0 0 0 1px
            rgba(86, 200, 255, 0.12),
            0 10px 28px
            rgba(38, 135, 210, 0.10);
    }}

    .pipeline-done {{
        border-color: {SUCCESS} !important;
    }}

    .pipeline-number {{
        color: {ACCENT};

        font-size: 0.68rem;

        font-weight: 800;

        letter-spacing: 0.12em;
    }}

    .pipeline-name {{
        color: {TEXT};

        font-size: 0.95rem;

        font-weight: 750;
    }}

    .pipeline-description {{
        color: {MUTED};

        font-size: 0.74rem;
    }}

    .pipeline-waiting {{
        color: {MUTED};

        font-size: 0.62rem;

        font-weight: 800;

        letter-spacing: 0.12em;
    }}

    .pipeline-running {{
        color: {ACCENT};

        font-size: 0.62rem;

        font-weight: 800;

        letter-spacing: 0.12em;
    }}

    .pipeline-complete {{
        color: {SUCCESS};

        font-size: 0.62rem;

        font-weight: 800;

        letter-spacing: 0.12em;
    }}


    /* ======================================================
       RESULT CONTAINERS
       ====================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: {BORDER} !important;

        border-radius: 16px !important;

        background: {CARD} !important;
    }}


    /* ======================================================
       TABS
       ====================================================== */

    button[data-baseweb="tab"] {{
        color: {MUTED} !important;

        font-weight: 650 !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {ACCENT} !important;
    }}


    /* ======================================================
       DOWNLOAD BUTTON
       ====================================================== */

    div[data-testid="stDownloadButton"] button {{
        border-radius: 10px !important;

        border: 1px solid {BORDER} !important;

        background: {CARD} !important;

        color: {TEXT} !important;
    }}


    /* ======================================================
       PROGRESS BAR
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
            padding-left: 1.2rem;
            padding-right: 1.2rem;
        }}

        .hero-title {{
            font-size: 4rem !important;
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

    brand_col_1, brand_col_2 = st.columns(
        [0.5, 6],
        vertical_alignment="center",
    )

    with brand_col_1:
        st.markdown(
            "🔎",
            text_alignment="center",
        )

    with brand_col_2:
        st.markdown(
            '<p class="brand-text">ResearcherAgent</p>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<p class="brand-caption">Multi-agent research workspace</p>',
            unsafe_allow_html=True,
        )


with top_right:

    new_theme = st.toggle(
        "Dark mode",
        value=st.session_state.dark_mode,
        label_visibility="collapsed",
        help="Toggle dark / light mode",
    )

    if new_theme != st.session_state.dark_mode:
        st.session_state.dark_mode = new_theme
        st.rerun()


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<p class="hero-small">MULTI-AGENT AI SYSTEM</p>',
    unsafe_allow_html=True,
)

st.markdown(
    '<h1 class="hero-title">ResearcherAgent</h1>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p class="hero-description">
        Search the web, analyze reliable sources, generate
        a structured research report, and review the result
        with AI-powered reasoning.
    </p>
    """,
    unsafe_allow_html=True,
)

st.divider()


# ============================================================
# MAIN WORKSPACE
# ============================================================

left_col, right_col = st.columns(
    [1.15, 0.85],
    gap="large",
)


# ============================================================
# LEFT: RESEARCH INPUT
# ============================================================

with left_col:

    st.markdown(
        '<p class="section-label">RESEARCH TOPIC</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="section-heading">What should we research?</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p class="section-description">
            Ask a focused question or describe a topic you want
            the research pipeline to investigate.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Input form
    # --------------------------------------------------------

    with st.form(
        "research_form",
        clear_on_submit=False,
    ):

        topic = st.text_input(
            "Research Topic",
            value=st.session_state.topic,
            placeholder=(
                "e.g. Roadmap for AGI development "
                "in next 5 years"
            ),
            label_visibility="collapsed",
        )

        st.write("")

        submitted = st.form_submit_button(
            "⚡  Run Research Pipeline",
            use_container_width=True,
        )

    # --------------------------------------------------------
    # Quick prompts
    # --------------------------------------------------------

    st.caption("TRY →")

    quick_topics = [
        "Future of LLM in Tech Industry",
        "All Latest AI Agents in 2026",
        "Roadmap for AGI development in next 5 years",
    ]

    quick_container = st.container()

with quick_container:

    for index, quick_topic in enumerate(quick_topics):

        clicked = st.button(
            quick_topic,
            key=f"quick_topic_{index}",
        )

        if clicked:
            st.session_state.topic = quick_topic
            st.rerun()


# ============================================================
# RIGHT: PIPELINE
# ============================================================

with right_col:

    pipeline_title_col, pipeline_badge_col = st.columns(
        [4, 1],
        vertical_alignment="center",
    )

    with pipeline_title_col:

        st.markdown(
            '<p class="section-heading">Pipeline</p>',
            unsafe_allow_html=True,
        )

    with pipeline_badge_col:

        st.caption("LIVE")


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
            return "active"

        return "waiting"


    def render_pipeline_step(
        number: int,
        name: str,
        description: str,
        status: str,
    ):

        if status == "active":

            status_text = "RUNNING"
            status_class = "pipeline-running"
            card_class = "pipeline-active"

        elif status == "done":

            status_text = "DONE"
            status_class = "pipeline-complete"
            card_class = "pipeline-done"

        else:

            status_text = "WAITING"
            status_class = "pipeline-waiting"
            card_class = ""

        with st.container(
            border=True,
        ):

            title_col, status_col = st.columns(
                [4, 1],
                vertical_alignment="center",
            )

            with title_col:

                number_col, name_col = st.columns(
                    [0.5, 4],
                    vertical_alignment="center",
                )

                with number_col:

                    st.markdown(
                        f'<span class="pipeline-number">'
                        f'{number:02d}'
                        f'</span>',
                        unsafe_allow_html=True,
                    )

                with name_col:

                    st.markdown(
                        f'<span class="pipeline-name">'
                        f'{name}'
                        f'</span>',
                        unsafe_allow_html=True,
                    )

            with status_col:

                st.markdown(
                    f'<span class="{status_class}">'
                    f'{status_text}'
                    f'</span>',
                    unsafe_allow_html=True,
                )

            st.markdown(
                f'<span class="pipeline-description">'
                f'{description}'
                f'</span>',
                unsafe_allow_html=True,
            )


    current_percent = st.session_state.pipeline_percent

    render_pipeline_step(
        1,
        "Web Search",
        "Find relevant and recent sources",
        get_step_status(1, current_percent),
    )

    render_pipeline_step(
        2,
        "Source Analysis",
        "Scrape and extract useful content",
        get_step_status(2, current_percent),
    )

    render_pipeline_step(
        3,
        "Writer",
        "Generate the research report",
        get_step_status(3, current_percent),
    )

    render_pipeline_step(
        4,
        "Critic",
        "Review and score the report",
        get_step_status(4, current_percent),
    )


# ============================================================
# RUN RESEARCH
# ============================================================

if submitted:

    if not topic.strip():

        st.warning(
            "Please enter a research topic."
        )

    else:

        st.session_state.topic = topic
        st.session_state.pipeline_percent = 10

        status_container = st.empty()

        progress_bar = st.progress(
            0,
            text="Starting research...",
        )


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

            # Streamlit reruns the script naturally, but the
            # progress state is preserved in session_state.


        try:

            result = run_research_pipeline(
                topic=topic,
                progress_callback=update_ui,
            )

            st.session_state.research_state = result

            st.session_state.pipeline_percent = 100

            progress_bar.progress(
                100,
                text="Research completed successfully.",
            )

            status_container.success(
                "Research completed successfully."
            )

            st.rerun()

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

    st.divider()

    st.markdown(
        '<p class="section-heading">Research Results</p>',
        unsafe_allow_html=True,
    )

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

            st.markdown(report)

        st.download_button(
            "⬇ Download Report",
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
            [],
        )

        if not search_results:

            st.info("No sources found.")

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

        scraped_sources = state.get(
            "scraped_content",
            [],
        )

        if not scraped_sources:

            st.info(
                "No scraped content available."
            )

        else:

            for index, source in enumerate(
                scraped_sources,
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
                feedback
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ResearcherAgent · LangChain · Tavily · Ollama"
)