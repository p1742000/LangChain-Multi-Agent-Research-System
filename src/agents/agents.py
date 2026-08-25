from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.config.llm import get_llm


# ============================================================
# MODEL
# ============================================================

llm = get_llm()


# ============================================================
# WRITER
# ============================================================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert research writer.

        Your job is to produce a clear, well-structured,
        factual and professional research report.

        Use only the research material provided to you.
        Do not invent facts, statistics, URLs or sources.
        """
    ),
    (
        "human",
        """
        Write a detailed research report on the topic below.

        Topic:
        {topic}

        Research gathered:
        {research}

        Structure the report as:

        1. Introduction
        2. Key Findings
        3. Important Trends / Insights
        4. Conclusion
        5. Sources

        Under Sources, include the URLs provided in the research.

        Make the report detailed, factual and professional.
        """
    )
])

writer_chain = writer_prompt | llm | StrOutputParser()


# ============================================================
# CRITIC
# ============================================================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a strict but constructive research critic.

        Evaluate the report for:
        - factual consistency
        - completeness
        - clarity
        - structure
        - source usage
        - unsupported claims
        """
    ),
    (
        "human",
        """
        Review the research report below.

        Report:
        {report}

        Respond in exactly this format:

        Score: X/10

        Strengths:
        - ...
        - ...

        Areas to Improve:
        - ...
        - ...

        One line verdict:
        ...
        """
    )
])

critic_chain = critic_prompt | llm | StrOutputParser()