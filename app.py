import truststore

# ============================================================
# IMPORTANT FOR CORPORATE MAC / LOWE'S SSL INSPECTION
# Must happen before importing modules that create HTTP clients.
# ============================================================

truststore.inject_into_ssl()


import streamlit as st

from src.pipelines.pipelines import run_research_pipeline


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Main page ---------- */

    .stApp {
        background-color: #f7f9fc;
    }

    .main {
        padding-top: 1rem;
    }


    /* ---------- Header ---------- */

    .hero {
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 16px;
        background: linear-gradient(
            135deg,
            #111827 0%,
            #1f2937 100%
        );
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        font-size: 2.4rem;
        margin-bottom: 0.4rem;
        font-weight: 700;
    }

    .hero p {
        color: #d1d5db;
        font-size: 1.05rem;
        margin-bottom: 0;
    }


    /* ---------- Cards ---------- */

    .metric-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        text-align: center;
    }

    .metric-title {
        color: #6b7280;
        font-size: 0.85rem;
        margin-bottom: 0.4rem;
    }

    .metric-value {
        color: #111827;
        font-size: 1.25rem;
        font-weight: 700;
    }


    /* ---------- Section headings ---------- */

    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #111827;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }


    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }


    /* ---------- Text area ---------- */

    textarea {
        border-radius: 10px !important;
    }


    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
    }


    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: #9ca3af;
        padding: 2rem 0 1rem 0;
        font-size: 0.85rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "research_state" not in st.session_state:
    st.session_state.research_state = None

if "topic" not in st.session_state:
    st.session_state.topic = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🔎 AI Research Agent")

    st.markdown(
        """
        <p style="color:#9ca3af;">
        Multi-agent research assistant powered by LangChain.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### Workflow")

    st.markdown(
        """
        **1. Search Agent**

        Finds recent and relevant information.

        **2. Reader Agent**

        Selects a useful source and extracts deeper content.

        **3. Writer**

        Synthesizes the research into a report.

        **4. Critic**

        Reviews the generated report and provides feedback.
        """
    )

    st.divider()

    st.markdown("### What can you research?")

    st.markdown(
        """
        - AI and technology
        - Software engineering
        - Market trends
        - Business topics
        - Scientific research
        - Industry developments
        """
    )

    st.divider()

    if st.button(
        "🗑️ Clear Results",
        use_container_width=True,
    ):
        st.session_state.research_state = None
        st.session_state.topic = ""
        st.rerun()


# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>🔎 AI Research Agent</h1>
        <p>
            Search the web, read relevant sources, synthesize findings,
            and critically review the final research report.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SEARCH INPUT
# ============================================================

st.markdown(
    '<div class="section-title">What would you like to research?</div>',
    unsafe_allow_html=True,
)


with st.form("research_form"):

    topic = st.text_input(
        "Research topic",
        value=st.session_state.topic,
        placeholder="Example: How is generative AI changing software engineering in 2026?",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([5, 1])

    with col1:
        st.caption(
            "Tip: Be specific. A focused question usually produces better research."
        )

    with col2:
        submitted = st.form_submit_button(
            "🚀 Research",
            use_container_width=True,
        )


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================

if not st.session_state.research_state:

    st.markdown(
        '<div class="section-title">Try an example</div>',
        unsafe_allow_html=True,
    )

    example_cols = st.columns(3)

    examples = [
        "Latest developments in agentic AI",
        "How AI is changing software engineering",
        "Latest advancements in AI coding agents",
    ]

    for i, example in enumerate(examples):

        with example_cols[i]:
            if st.button(
                example,
                use_container_width=True,
            ):
                st.session_state.topic = example
                st.rerun()


# ============================================================
# EXECUTE RESEARCH
# ============================================================

if submitted:

    if not topic.strip():

        st.warning(
            "Please enter a research topic before starting."
        )

    else:

        st.session_state.topic = topic

        progress_bar = st.progress(0)

        status_container = st.empty()

        def update_ui(message: str, percent: int):

            status_container.info(
                f"🔄 {message}"
            )

            progress_bar.progress(percent)

        try:

            with st.spinner("Running the research pipeline..."):

                result = run_research_pipeline(
                    topic=topic,
                    progress_callback=update_ui,
                )

            st.session_state.research_state = result

            status_container.success(
                "✅ Research completed successfully."
            )

            progress_bar.progress(100)

        except Exception as e:

            status_container.error(
                "❌ Research pipeline failed."
            )

            st.exception(e)


# ============================================================
# DISPLAY RESULTS
# ============================================================

if st.session_state.research_state:

    state = st.session_state.research_state

    st.divider()

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Research Overview</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Search</div>
                <div class="metric-value">Completed</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Reader</div>
                <div class="metric-value">Completed</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Writer</div>
                <div class="metric-value">Completed</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Critic</div>
                <div class="metric-value">Completed</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    st.write("")


    # --------------------------------------------------------
    # TABS
    # --------------------------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📄 Final Report",
            "🔍 Search Research",
            "🌐 Scraped Content",
            "🧠 Critic Feedback",
        ]
    )


    # ========================================================
    # TAB 1 - FINAL REPORT
    # ========================================================

    with tab1:

        st.markdown(
            '<div class="section-title">Research Report</div>',
            unsafe_allow_html=True,
        )

        report = state.get(
            "report",
            "No report generated.",
        )

        st.markdown(report)

        st.divider()

        st.download_button(
            label="⬇️ Download Report",
            data=report,
            file_name="ai_research_report.txt",
            mime="text/plain",
            use_container_width=False,
        )


    # ========================================================
    # TAB 2 - SEARCH RESULTS
    # ========================================================

    with tab2:

        st.markdown(
            '<div class="section-title">Search Results</div>',
            unsafe_allow_html=True,
        )

        search_results = state.get(
            "search_results",
            "No search results available.",
        )

        st.text_area(
            "Raw search output",
            value=search_results,
            height=500,
            label_visibility="collapsed",
        )


    # ========================================================
    # TAB 3 - SCRAPED CONTENT
    # ========================================================

    with tab3:

        st.markdown(
            '<div class="section-title">Scraped Source Content</div>',
            unsafe_allow_html=True,
        )

        scraped_content = state.get(
            "scraped_content",
            "No scraped content available.",
        )

        st.text_area(
            "Scraped content",
            value=scraped_content,
            height=500,
            label_visibility="collapsed",
        )


    # ========================================================
    # TAB 4 - CRITIC
    # ========================================================

    with tab4:

        st.markdown(
            '<div class="section-title">Critic Feedback</div>',
            unsafe_allow_html=True,
        )

        feedback = state.get(
            "feedback",
            "No critic feedback available.",
        )

        st.markdown(feedback)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Built with Streamlit + LangChain + LangGraph + Tavily
    </div>
    """,
    unsafe_allow_html=True,
)