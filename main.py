from src.tools.tools import web_search, scrape_url
from src.pipelines.pipelines import run_research_pipeline
import truststore
# Use macOS system certificate store.
# Required on corporate network because HTTPS is SSL-inspected.
truststore.inject_into_ssl()

# result = web_search("give me the latest news AI research")
# result = scrape_url("https://guides.library.georgetown.edu/ai/news")

# result = web_search.invoke("give me the latest news AI research")
# print(result)

topic = "The impact of AI in job market in 2026"
run_research_pipeline(topic)
