from src.tools.tools import web_search, scrape_url
from src.agents.agents import writer_chain, critic_chain


def run_research_pipeline(topic: str, progress_callback=None) -> dict:

    state = {}

    def update_progress(message: str, percent: int):
        if progress_callback:
            progress_callback(message, percent)

    # ============================================================
    # STEP 1 - WEB SEARCH
    # No LLM call
    # ============================================================

    update_progress(
        "Searching the web for recent and reliable information...",
        10,
    )

    search_results = web_search.invoke({
        "query": topic
    })

    state["search_results"] = search_results

    update_progress(
        f"Found {len(search_results)} relevant sources.",
        25,
    )

    # ============================================================
    # STEP 2 - SCRAPE TOP SOURCES
    # No LLM call
    # ============================================================

    update_progress(
        "Scraping the most relevant sources...",
        35,
    )

    scraped_sources = []

    # Use top 3 sources
    for index, result in enumerate(search_results[:3], start=1):

        url = result["url"]
        title = result["title"]

        update_progress(
            f"Scraping source {index}/3: {title}",
            35 + (index * 8),
        )

        content = scrape_url.invoke({
            "url": url
        })

        scraped_sources.append({
            "title": title,
            "url": url,
            "search_content": result["content"],
            "scraped_content": content,
        })

    state["scraped_content"] = scraped_sources

    # ============================================================
    # STEP 3 - BUILD RESEARCH CONTEXT
    # No LLM call
    # ============================================================

    update_progress(
        "Combining research from all sources...",
        65,
    )

    research_parts = []

    for source in scraped_sources:

        research_parts.append(
            f"""
SOURCE TITLE:
{source['title']}

SOURCE URL:
{source['url']}

SEARCH SNIPPET:
{source['search_content']}

SCRAPED CONTENT:
{source['scraped_content']}
"""
        )

    researched_combined = "\n\n====================\n\n".join(
        research_parts
    )

    state["research_context"] = researched_combined

    # ============================================================
    # STEP 4 - WRITER
    # LLM CALL #1
    # ============================================================

    update_progress(
        "Writer is synthesizing the research into a report...",
        75,
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": researched_combined,
    })

    # ============================================================
    # STEP 5 - CRITIC
    # LLM CALL #2
    # ============================================================

    update_progress(
        "Critic is reviewing the generated report...",
        90,
    )

    state["feedback"] = critic_chain.invoke({
        "report": state["report"],
    })

    update_progress(
        "Research completed successfully.",
        100,
    )

    return state