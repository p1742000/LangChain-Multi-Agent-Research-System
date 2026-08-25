from src.agents.agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)


def run_research_pipeline(topic: str, progress_callback=None) -> dict:
    """
    Runs the complete research pipeline.

    Pipeline:
        1. Search Agent
        2. Reader Agent
        3. Writer
        4. Critic

    progress_callback(message, progress_percent)
    is optional and is used by the Streamlit UI.
    """

    state = {}

    def update_progress(message: str, percent: int):
        if progress_callback:
            progress_callback(message, percent)

    # ==================================================
    # STEP 1 - SEARCH AGENT
    # ==================================================

    update_progress(
        "Searching the web for recent and reliable information...",
        10,
    )

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find recent, reliable and detailed information about: {topic}"
            )
        ]
    })

    state["search_results"] = search_result["messages"][-1].content

    update_progress(
        "Search completed. Relevant information collected.",
        30,
    )

    # ==================================================
    # STEP 2 - READER AGENT
    # ==================================================

    update_progress(
        "Reader Agent is selecting and scraping the most relevant resource...",
        40,
    )

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n"
                f"{state['search_results'][:800]}"
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    update_progress(
        "Website content successfully scraped.",
        55,
    )

    # ==================================================
    # STEP 3 - WRITER
    # ==================================================

    update_progress(
        "Writer Agent is synthesizing the research into a report...",
        65,
    )

    # IMPORTANT:
    # This must be ONE STRING, not a tuple.
    researched_combined = (
        f"SEARCHED RESULTS:\n"
        f"{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n"
        f"{state['scraped_content']}\n"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": researched_combined,
    })

    update_progress(
        "Draft report generated.",
        80,
    )

    # ==================================================
    # STEP 4 - CRITIC
    # ==================================================

    update_progress(
        "Critic Agent is reviewing the generated report...",
        88,
    )

    state["feedback"] = critic_chain.invoke({
        "report": state["report"],
    })

    update_progress(
        "Research completed successfully.",
        100,
    )

    return state